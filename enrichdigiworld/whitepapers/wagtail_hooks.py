from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail import hooks
from .models import Lead, WhitepaperPage
from wagtail.admin.menu import MenuItem
from django.urls import path, reverse
from django.utils.safestring import mark_safe
from .views import whitepaper_analytics

class LeadViewSet(SnippetViewSet):
    model = Lead
    icon = "user"
    menu_label = "Whitepaper Leads"
    menu_name = "whitepaper_leads"
    menu_order = 200
    add_to_admin_menu = True
    list_display = ("email", "whitepaper", "submitted_at", "status", "country")
    list_filter = ("whitepaper", "status", "country", "submitted_at")
    search_fields = ("email", "full_name", "ip_address")
    list_export = ("email", "whitepaper", "submitted_at", "status", "ip_address", "country", "user_agent", "utm_source", "utm_campaign", "get_dynamic_fields")

    def get_dynamic_fields(self, instance):
        # This is a helper for export to potentially include dynamic fields
        # However, list_export usually expects field names or attributes.
        # For a truly dynamic CSV, we might need a custom export view.
        values = instance.values.all()
        return "; ".join([f"{v.field_name}: {v.value}" for v in values])
    get_dynamic_fields.short_description = "Form Data"

@hooks.register("register_admin_urls")
def register_analytics_url():
    return [
        path("whitepaper-analytics/", whitepaper_analytics, name="whitepaper_analytics"),
    ]

@hooks.register("register_admin_menu_item")
def register_analytics_menu_item():
    return MenuItem(
        "Whitepaper Analytics",
        reverse("whitepaper_analytics"),
        icon_name="pick",
        order=3000
    )