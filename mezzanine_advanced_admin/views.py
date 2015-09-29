#encoding: utf-8
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from mezzanine.core.models import CONTENT_STATUS_DRAFT, CONTENT_STATUS_PUBLISHED
from mezzanine.pages.models import Page


@staff_member_required
def admin_page_update_status(request):
    """
    Updates the page status via AJAX from within the admin.
    """
    try:
        page = Page.objects.get(id=request.POST.get("id"))
    except Page.DoesNotExist:
        return HttpResponse("error")
    current_status = page.status
    if current_status == CONTENT_STATUS_DRAFT:
        page.status = CONTENT_STATUS_PUBLISHED
    else:
        page.status = CONTENT_STATUS_DRAFT
    page.save()

    return HttpResponse(page.get_status_display())