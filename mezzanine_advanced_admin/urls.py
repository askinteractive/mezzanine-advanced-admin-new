#encoding: utf-8
from __future__ import unicode_literals
from django.conf.urls import patterns, url


urlpatterns = patterns("mezzanine_advanced_admin.views",
    url("^page_update_status/$", "admin_page_update_status", name="admin_page_update_status"),
)
