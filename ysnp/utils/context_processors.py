from django.conf import settings

def google_analytics(request):
    ''' Check if Google Analytics ID is defined on settings'''

    analytics_id = getattr(settings, 'GOOGLE_ANALYTICS_ID')
    context = {
        'google_analytics_id': analytics_id,
    }

    return analytics_id and context or {}
