from importlib import import_module
from django.contrib import admin
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse, NoReverseMatch
from django.template.defaultfilters import capfirst

from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from mezzanine import template
from mezzanine.conf import settings
from mezzanine.core.templatetags.mezzanine_tags import admin_app_list
from mezzanine.utils.sites import current_site_id
from mezzanine.utils.urls import admin_url

register = template.Library()


CUSTOM_FIELD_RENDERER = getattr(settings, 'ADVANCED_ADMIN_FIELD_RENDERER',
                                'mezzanine_advanced_admin.renderers.BootstrapFieldRenderer')


@register.simple_tag(takes_context=True)
def render_with_template_if_exist(context, template, fallback):
    text = fallback
    try:
        text = render_to_string(template, context)
    except:
        pass
    return text

@register.simple_tag(takes_context=True)
def language_selector(context):
    """ displays a language selector dropdown in the admin, based on Django "LANGUAGES" context.
        requires:
            * USE_I18N = True / settings.py
            * LANGUAGES specified / settings.py (otherwise all Django locales will be displayed)
            * "set_language" url configured (see https://docs.djangoproject.com/en/dev/topics/i18n/translation/#the-set-language-redirect-view)
    """
    output = ""
    i18 = getattr(settings, 'USE_I18N', False)
    if i18:
        template = "admin/language_selector.html"
        context['i18n_is_set'] = True
        try:
            output = render_to_string(template, context)
        except:
            pass
    return output


@register.filter(name='column_width')
def column_width(value):
    try:
        return 12 // len(list(value))
    except ZeroDivisionError:
        return 12


@register.filter(name='form_fieldset_column_width')
def form_fieldset_column_width(form):
    # def max_line(fieldset):
    #     return max([len(list(line)) for line in fieldset])
    #
    # try:
    #     width = max([max_line(fieldset) for fieldset in form])
    #     return 12 // width
    # except ValueError:
    #     return 12
    return 12


@register.filter(name='fieldset_column_width')
def fieldset_column_width(fieldset):
    try:
        width = max([len(list(line)) for line in fieldset])
        return 12 // width
    except ValueError:
        return 12


@register.simple_tag(takes_context=True)
def render_app_name(context, app, template="/admin_app_name.html"):
    """ Render the application name using the default template name. If it cannot find a
        template matching the given path, fallback to the application name.
    """
    try:
        template = app['app_label'] + template
        text = render_to_string(template, context)
    except:
        text = app['name']
    return text


@register.simple_tag(takes_context=True)
def render_app_label(context, app, fallback=""):
    """ Render the application label.
    """
    try:
        text = app['app_label']
    except KeyError:
        text = fallback
    except TypeError:
        text = app
    return text


@register.simple_tag(takes_context=True)
def render_app_description(context, app, fallback="", template="/admin_app_description.html"):
    """ Render the application description using the default template name. If it cannot find a
        template matching the given path, fallback to the fallback argument.
    """
    try:
        template = app['app_label'] + template
        text = render_to_string(template, context)
    except:
        text = fallback
    return text


@register.simple_tag(takes_context=True, name="dab_field_rendering")
def custom_field_rendering(context, field, *args, **kwargs):
    """ Wrapper for rendering the field via an external renderer """
    if CUSTOM_FIELD_RENDERER:
        mod, cls = CUSTOM_FIELD_RENDERER.rsplit(".", 1)
        field_renderer = getattr(import_module(mod), cls)
        if field_renderer:
            return field_renderer(field, **kwargs).render()
    return field


@register.as_tag
def get_menus_for_page(page=None):
    """
    Get menus labels for page.
    """
    if not page:
        return settings.PAGE_MENU_TEMPLATES
    menus = []
    for menu in settings.PAGE_MENU_TEMPLATES:
        if str(menu[0]) in page.in_menus:
            menus.append(menu[1])
    return menus


@register.simple_tag
def get_content_model_for_page(page):
    """
    Render the page content model label.
    """
    return unicode(page.get_content_model()._meta.verbose_name)


@register.inclusion_tag("admin/includes/admin_title.html", takes_context=True)
def admin_title(context):
    title = getattr(settings, "ADVANCED_ADMIN_TITLE", _("%s - Administration" % settings.SITE_TITLE))
    logo_path = getattr(settings, "ADVANCED_ADMIN_LOGO_PATH", None)
    context["title"] = title
    context["logo_path"] = logo_path
    return context

@register.inclusion_tag("admin/includes/menu.html", takes_context=True)
def render_menu(context):
    """
    Adopted from ``django.contrib.admin.sites.AdminSite.index``.
    Returns a list of lists of models grouped and ordered according to
    ``mezzanine.conf.ADMIN_MENU_ORDER``. Called from the
    ``admin_dropdown_menu`` template tag as well as the ``app_list``
    dashboard widget.
    """
    request = context["request"]
    app_dict = {}

    # Model or view --> (group index, group title, item index, item title).
    menu_order = {}
    for (group_index, group) in enumerate(settings.ADMIN_MENU_ORDER):
        if len(group) == 3:
            group_title, items, group_icon = group
        else:
            group_title, items = group
            group_icon = None
        group_title = group_title.title()
        for (item_index, item) in enumerate(items):
            if isinstance(item, (tuple, list)):
                item_title, item = item
            else:
                item_title = None
            menu_order[item] = (group_index, group_title, group_icon,
                                item_index, item_title)

    # Add all registered models, using group and title from menu order.
    for (model, model_admin) in admin.site._registry.items():
        opts = model._meta
        in_menu = not hasattr(model_admin, "in_menu") or model_admin.in_menu()
        if in_menu and request.user.has_module_perms(opts.app_label):
            perms = model_admin.get_model_perms(request)
            admin_url_name = ""
            if perms["change"]:
                admin_url_name = "changelist"
                change_url = admin_url(model, admin_url_name)
            else:
                change_url = None
            if perms["add"]:
                admin_url_name = "add"
                add_url = admin_url(model, admin_url_name)
            else:
                add_url = None
            if admin_url_name:
                model_label = "%s.%s" % (opts.app_label, opts.object_name)
                try:
                    app_index, app_title, app_icon, model_index, model_title = \
                        menu_order[model_label]
                except KeyError:
                    app_index = None
                    app_title = opts.app_config.verbose_name.title()
                    app_icon = None
                    model_index = None
                    model_title = None
                else:
                    del menu_order[model_label]

                if not model_title:
                    model_title = capfirst(model._meta.verbose_name_plural)

                if app_title not in app_dict:
                    app_dict[app_title] = {
                        "index": app_index,
                        "name": app_title,
                        "icon": app_icon,
                        "models": [],
                    }
                app_dict[app_title]["models"].append({
                    "index": model_index,
                    "perms": model_admin.get_model_perms(request),
                    "name": model_title,
                    "admin_url": change_url,
                    "add_url": add_url
                })

    # Menu may also contain view or url pattern names given as (title, name).
    for (item_url, item) in menu_order.items():
        app_index, app_title, app_icon, item_index, item_title = item
        try:
            item_url = reverse(item_url)
        except NoReverseMatch:
            continue
        if app_title not in app_dict:
            app_dict[app_title] = {
                "index": app_index,
                "name": app_title,
                "models": [],
            }
        app_dict[app_title]["models"].append({
            "index": item_index,
            "perms": {"custom": True},
            "name": item_title,
            "admin_url": item_url,
        })

    app_list = list(app_dict.values())
    sort = lambda x: (x["index"] if x["index"] is not None else 999, x["name"])
    for app in app_list:
        app["models"].sort(key=sort)
    app_list.sort(key=sort)

    user = context["request"].user
    context["dropdown_menu_app_list"] = app_list
    if user.is_superuser:
        sites = Site.objects.all()
    else:
        sites = user.sitepermissions.sites.all()
    context["dropdown_menu_sites"] = list(sites)
    context["dropdown_menu_selected_site_id"] = current_site_id()

    return context


@register.filter(name='widget_type')
def widget_type(field):
    """
    Template filter that returns field widget class name (in lower case).
    E.g. if field's widget is TextInput then {{ field|widget_type }} will
    return 'textinput'.
    """
    if hasattr(field, 'field') and hasattr(field.field, 'widget') and field.field.widget:
        return field.field.widget.__class__.__name__.lower()
    return ''