from __future__ import absolute_import
import re

from django.contrib.auth.forms import ReadOnlyPasswordHashWidget
from django.contrib.admin.widgets import (AdminDateWidget, AdminTimeWidget,
                                          AdminSplitDateTime, RelatedFieldWidgetWrapper)
from django.forms import (FileInput, CheckboxInput, RadioSelect, CheckboxSelectMultiple, ClearableFileInput)

from bootstrap3 import renderers
from django.forms.extras import SelectDateWidget

try:
    from bootstrap3.utils import add_css_class
except ImportError:
    from bootstrap3.html import add_css_class
from bootstrap3.text import text_value


class BootstrapFieldRenderer(renderers.FieldRenderer):
    """
    A django-bootstrap3 field renderer that renders just the field
    """
    # TODO Render Checkbox, Radio, and Date
    def render(self):
        # Hidden input requires no special treatment
        if self.field.is_hidden:
            return text_value(self.field)
        # Render the widget
        self.add_widget_attrs()
        html = self.field.as_widget(attrs=self.widget.attrs)
        # Start post render
        html = self.wrap_widget(html)
        html = self.post_widget_render(html)
        return html

    def wrap_widget(self, html):
        if isinstance(self.widget, (CheckboxInput)):
            checkbox_class = add_css_class('checkbox checkbox-material-blue-700', self.get_size_class())
            html = '<div class="{klass}">{content}<span class="checkbox-material"><span class="check"></span></span></div>'.format(
                klass=checkbox_class,
                content=html,
            )
        return html

    def post_widget_render(self, html):
        if isinstance(self.widget, RadioSelect):
            html = self.list_to_class(html, 'radio')
            html = self.fix_radio_select_input(html)
        elif isinstance(self.widget, CheckboxSelectMultiple):
            html = self.list_to_class(html, 'checkbox')
            html = self.fix_checkbox_select_input(html)
        elif isinstance(self.widget, AdminSplitDateTime):
            html = self.fix_split_datetime(html)
        elif isinstance(self.widget, SelectDateWidget):
            html = self.fix_date_select_input(html)
        elif isinstance(self.widget, ClearableFileInput):
            html = self.fix_clearable_file_input(html)
        return html

    def fix_radio_select_input(self, html):
        def wrap(m):
            return '<input ' + m.group(1) +'/><span class="circle"></span><span class="check"></span>'
        html = re.sub(r'<input (.*)/>', wrap, html)
        return html

    def fix_checkbox_select_input(self, html):
        def wrap(m):
            return '<input ' + m.group(1) +'/><span class="checkbox-material"><span class="check"></span></span>'
        html = re.sub(r'<input (.*)/>', wrap, html)
        return html

    def fix_split_datetime(self, html):
        # Hide the built-in widget
        # html = html.replace('class="datetime"', 'class="datetime material-datepicker"')
        # Create a new one
        # html = '<input type="text" class="form-control material-datepicker">' + html
        print html
        return html

    def list_to_class(self, html, klass):
        classes = add_css_class(klass, self.get_size_class())
        mapping = [
            ('<ul', '<div'),
            ('</ul>', '</div>'),
            ('<li', '<div class="{klass} {klass}-material-blue-700"'.format(klass=classes)),
            ('</li>', '</div>'),
        ]
        for k, v in mapping:
            html = html.replace(k, v)
        return html

    def add_class_attrs(self, widget=None):
        if not widget:
            widget = self.widget

        # for multiwidgets we recursively update classes for each sub-widget
        if isinstance(widget, AdminSplitDateTime):
            for w in widget.widgets:
                self.add_class_attrs(w)
            return

        classes = widget.attrs.get('class', '')
        if isinstance(widget, ReadOnlyPasswordHashWidget):
            classes = add_css_class(classes, 'form-control-static', prepend=True)
        elif isinstance(widget, (AdminDateWidget,
                                 AdminTimeWidget,
                                 RelatedFieldWidgetWrapper)):
            # for some admin widgets we don't want the input to take full horizontal space
            classes = add_css_class(classes, 'form-control form-control-inline material-datepicker', prepend=True)
        elif isinstance(widget, RadioSelect):
            classes = add_css_class(classes, 'radioselect', prepend=True)
        elif not isinstance(widget, (CheckboxInput,
                                     CheckboxSelectMultiple,
                                     FileInput)):
            classes = add_css_class(classes, 'form-control', prepend=True)
            # For these widget types, add the size class here
            classes = add_css_class(classes, self.get_size_class())

        widget.attrs['class'] = classes
