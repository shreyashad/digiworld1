from django.shortcuts import render
from django.db.models import Count, Min, Max
from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import timedelta
from .models import Lead, WhitepaperPage, WhitepaperView
from wagtail.admin.auth import user_passes_test
from django.urls import reverse 


@user_passes_test(lambda u: u.is_staff)
def whitepaper_analytics(request):
    # Overall Metrics
    total_leads = Lead.objects.count()
    total_views = WhitepaperView.objects.count()
    conversion_rate = (total_leads / total_views * 100) if total_views > 0 else 0

    # Leads over the last 30 days
    last_30_days = timezone.now() - timedelta(days=30)
    lead_trends = (
        Lead.objects.filter(submitted_at__gte=last_30_days)
        .annotate(date=TruncDate('submitted_at'))
        .values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )

    # Top Whitepapers by Lead Count with pre-calculated rates
    top_whitepapers = (
        WhitepaperPage.objects.annotate(
            lead_count=Count('leads', distinct=True),
            view_count=Count('views', distinct=True)
        )
        .filter(lead_count__gt=0)
        .order_by('-lead_count')[:10]
    )
    
    for wp in top_whitepapers:
        wp.conversion_rate = round((wp.lead_count / wp.view_count * 100), 1) if wp.view_count > 0 else 0

    # Top Whitepapers by View Count
    top_views = (
        WhitepaperPage.objects.annotate(view_count=Count('views'))
        .filter(view_count__gt=0)
        .order_by('-view_count')[:5]
    )
    
    try:
        lead_index_url = reverse("wagtailadmin_whitepaper_leads:index")
    except:
        lead_index_url = "#"


    context = {
        'total_leads': total_leads,
        'total_views': total_views,
        'conversion_rate': round(conversion_rate, 2),
        'lead_trends': lead_trends,
        'top_whitepapers': top_whitepapers,
        'top_views': top_views,
        'lead_index_url': lead_index_url,
    }

    return render(request, 'whitepapers/admin/analytics.html', context)