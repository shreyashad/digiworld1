from django import template
from home.models import (
    StatsCounter, Service, Testimonial, NetworkLink
)
from whitepapers.models import WhitepaperPage, WhitepaperCategory, WhitepaperClient

register = template.Library()


@register.simple_tag
def get_stats_counters():
    """Get all statistics counters ordered by display order"""
    return StatsCounter.objects.all()


@register.simple_tag
def get_services():
    """Get all services ordered by display order"""
    return Service.objects.all()


@register.simple_tag
def get_testimonials():
    """Get all testimonials ordered by display order"""
    return Testimonial.objects.all()


@register.simple_tag
def get_network_links():
    """Get all network links ordered by display order"""
    return NetworkLink.objects.all()


@register.simple_tag
def get_latest_whitepapers(limit=6):
    """Get latest published whitepapers"""
    return (
        WhitepaperPage.objects
        .live()
        .order_by('-first_published_at')[:limit]
    )


@register.simple_tag
def get_whitepaper_categories():
    """Get all whitepaper categories"""
    return WhitepaperCategory.objects.all()


@register.simple_tag
def get_clients():
    """Get all clients/publishers"""
    return WhitepaperClient.objects.all()


@register.filter
def mul(value, arg):
    """Multiply value by argument"""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return 0
