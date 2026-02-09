from django import template

register = template.Library()


@register.simple_tag
def get_clients():
    """Get all clients/publishers for logo cloud"""
    from whitepapers.models import WhitepaperClient
    return WhitepaperClient.objects.all()


@register.filter
def mul(value, arg):
    """Multiplies the value by the arg"""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return value


@register.filter
def divide(value, arg):
    """Divides the value by the arg"""
    try:
        return float(value) / float(arg)
    except (ValueError, TypeError, ZeroDivisionError):
        return value
