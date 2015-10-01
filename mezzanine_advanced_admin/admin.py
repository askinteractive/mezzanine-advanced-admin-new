#encoding: utf-8
from django.contrib import admin
from django.contrib.admin import TabularInline
from mezzanine.forms.admin import FormAdmin
from mezzanine.forms.models import Form, Field
from mezzanine.galleries.admin import GalleryAdmin
from mezzanine.galleries.models import GalleryImage, Gallery

class BaseSortable(object):
    sortable_field_name = "_order"

    def get_fields(self, request, obj=None):
        fields = super(BaseSortable, self).get_fields(request, obj)
        print fields
        try:
            fields.remove(self.sortable_field_name)
        except:
            pass
        if isinstance(self, SortableInline):
            fields.append(self.sortable_field_name)
        return fields

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(BaseSortable, self).get_fieldsets(request, obj)
        for fieldset in fieldsets:
            fields = [f for f in list(fieldset[1]["fields"])
                      if not hasattr(f, "translated_field")]
            try:
                fields.remove(self.sortable_field_name)
            except:
                pass
            fieldset[1]["fields"] = fields
        if isinstance(self, SortableInline):
            fieldsets[-1][1]["fields"].append(self.sortable_field_name)
        return fieldsets

class SortableAdmin(BaseSortable):
    def __init__(self, model, admin_site):
        super(SortableAdmin, self).__init__(model, admin_site)
        list_editable = list(self.list_editable)
        if self.sortable_field_name not in list_editable:
            list_editable.append(self.sortable_field_name)
        self.list_editable = list_editable

    def get_list_display(self, request):
        list_display = list(super(SortableAdmin, self).get_list_display(request))
        if self.sortable_field_name not in list_display:
            list_display.append(self.sortable_field_name)
        return list_display

    class Media:
        js = ["admin/js/changelist-sortable.js"]
        css = {
            'all': ('admin/css/changelist-sortable.css',)
        }

class SortableInline(BaseSortable):
    class Media:
        css = {
            'all': ('admin/css/admin-inlines.css', )
        }


class CollapsibleInline(object):
    start_collapsed = True



###################### FORMS ######################
class AdvancedFieldAdmin(SortableInline, TabularInline):
    """
    Change Mezzanine Tabular for Field inline.
    """
    model = Field
    extra = 0


class AdvancedFormAdmin(FormAdmin):
    """
    Use a custom Tabular inline.
    """
    inlines = [AdvancedFieldAdmin]


admin.site.unregister(Form)
admin.site.register(Form, AdvancedFormAdmin)


###################### GALLERIES ######################
class AdvancedGalleryImageAdmin(SortableInline, TabularInline):
    """
    Change Mezzanine Tabular for GalleryImage inline.
    """
    model = GalleryImage
    extra = 0


class AdvancedGalleryAdmin(GalleryAdmin):
    """
    Use a custom Tabular inline.
    """
    inlines = [AdvancedGalleryImageAdmin]
    sortable_field_name = "_order"


admin.site.unregister(Gallery)
admin.site.register(Gallery, AdvancedGalleryAdmin)

