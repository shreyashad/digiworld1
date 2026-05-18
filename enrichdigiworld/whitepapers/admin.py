from django.contrib import admin
from wagtail.admin.viewsets.model import ModelViewSet
from wagtail.admin.viewsets.base import ViewSetGroup
from wagtail import hooks
from wagtail.admin.panels import FieldPanel, InlinePanel
from .models import Lead

# Register your models here.



class LeadViewSet(ModelViewSet):
    model = Lead
    icon = "form"
    menu_label = "Whitepaper Leads"
    menu_name = "whitepaper_leads"
    menu_order = 200
    add_to_admin_menu = True
    
    panels = [
        FieldPanel("whitepaper"),
        FieldPanel("email"),
        FieldPanel("full_name"),
        FieldPanel("status"),
        FieldPanel("utm_source"),
        FieldPanel("utm_campaign"),
        FieldPanel("country"),
        FieldPanel("ip_address"),
        
    ]
    list_display = (
        "email",
        "whitepaper",
        "status",
        "submitted_at",
    )
    list_filter = (
        "status",
        "whitepaper",
        "submitted_at",
    )
    search_fields = (
        "email",
        "whitepaper__title",
        "utm_source",
        "utm_campaign",
    )


class WhitepaperGroup(ViewSetGroup):
    menu_label = "Whitepaper Management"
    menu_icon = "folder-open-inverse"
    menu_order = 200
    items = (LeadViewSet,)


@hooks.register("register_admin_viewset")
def register_whitepaper_admin():
    return WhitepaperGroup()