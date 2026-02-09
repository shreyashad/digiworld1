from django import template
from core.models import NavigationMenu, FooterColumn

register = template.Library()

@register.inclusion_tag("core/snippets/navigation_menu.html", takes_context=True)
def get_menu(context, slug):
    try:
        menu = NavigationMenu.objects.get(slug=slug)
        return {
            "menu": menu,
            "request": context.get("request"),
        }
    except NavigationMenu.DoesNotExist:
        return {
            "menu": None,
            "request": context.get("request"),
        }


@register.simple_tag
def get_footer_columns():
    """Get all footer columns ordered by their order field"""
    return FooterColumn.objects.all().order_by('order')
