#encoding: utf-8
from django.contrib import admin
from django.contrib.admin import TabularInline
from mezzanine.forms.admin import FormAdmin
from mezzanine.forms.models import Form, Field
from mezzanine.galleries.admin import GalleryAdmin
from mezzanine.galleries.models import GalleryImage, Gallery


class SortableInline(object):
    sortable_field_name = "_order"

    class Media:
        js = (
            'admin/js/jquery.sortable.js',
        )

        css = {
            'all': ('admin/css/admin-inlines.css', )
        }

    def get_fields(self, request, obj=None):
        fields = super(SortableInline, self).get_fields(request, obj)
        try:
            fields.remove(self.sortable_field_name)
        except:
            pass
        fields.append(self.sortable_field_name)
        return fields

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(SortableInline, self).get_fieldsets(request, obj)
        for fieldset in fieldsets:
            fields = [f for f in list(fieldset[1]["fields"])
                      if not hasattr(f, "translated_field")]
            try:
                fields.remove(self.sortable_field_name)
            except:
                pass
            fieldset[1]["fields"] = fields
        fieldsets[-1][1]["fields"].append(self.sortable_field_name)
        return fieldsets


class CollapsibleInline(object):
    start_collapsed = False



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

