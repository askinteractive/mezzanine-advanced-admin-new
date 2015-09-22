#encoding: utf-8
from django.contrib import admin
from django.contrib.admin import TabularInline
from django.forms import HiddenInput, CharField
from mezzanine.core.fields import OrderField
from mezzanine.core.models import Orderable
from mezzanine.forms.admin import FormAdmin
from mezzanine.forms.models import Form, Field
from mezzanine.galleries.admin import GalleryAdmin
from mezzanine.galleries.models import GalleryImage, Gallery
from mezzanine_advanced_admin.models import SortableInline


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

