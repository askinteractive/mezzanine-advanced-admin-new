from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from mezzanine.conf import register_setting


register_setting(
    name="ADVANCED_ADMIN_TITLE",
    description=_("The title displayed in the admin header"),
    editable=True,
    default="",
)

register_setting(
    name="ADVANCED_ADMIN_LOGO_PATH",
    description=_("The relative path from STATIC_ROOT for the image displayed in the admin header"),
    editable=True,
    default="",
)

register_setting(
    name="ADVANCED_ADMIN_MENU_ICONS",
    description=_("App icon class for ADMIN_MENU_ORDER. Icon mapping is made by the app name "
                  "See http://fezvrasta.github.io/bootstrap-material-design/bootstrap-elements.html#icon"),
    editable=False,
    default={
        "Content": "mdi-editor-format-align-center",
        "Filebrowser": "mdi-file-folder",
        "Users": "mdi-social-group",
        "Site": "mdi-hardware-laptop",
        "Dashboard": "mdi-action-dashboard"
    }
)