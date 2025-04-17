import requests
import hashlib
import datetime
import json
from django.conf import settings
from .models import FacebookEventLog

ACCESS_TOKEN = getattr(settings, 'FACEBOOK_CAPI_ACCESS_TOKEN', '')
PIXEL_ID = getattr(settings, 'FACEBOOK_PIXEL_ID', '')
CAPI_URL = f'https://graph.facebook.com/v18.0/{PIXEL_ID}/events'

def hash_data(data):
    if data:
        return hashlib.sha256(data.strip().lower().encode()).hexdigest()
    return None

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def extract_user_data(request):
    return {
        'client_ip_address': get_client_ip(request),
        'client_user_agent': request.META.get('HTTP_USER_AGENT'),
        'fbc': request.COOKIES.get('_fbc'),
        'fbp': request.COOKIES.get('_fbp'),
        'email': hash_data(request.POST.get('email')),
        'phone': hash_data(request.POST.get('phone')),
    }

def send_event(event_name, user_data, custom_data=None, event_source_url=None, test_event_code=None):
    payload = {
        'data': [
            {
                'event_name': event_name,
                'event_time': int(datetime.datetime.now().timestamp()),
                'user_data': user_data,
                'custom_data': custom_data or {},
                'event_source_url': event_source_url,
                'action_source': 'website',
            }
        ],
        'access_token': ACCESS_TOKEN
    }

    if test_event_code:
        payload['test_event_code'] = test_event_code

    headers = {'Content-Type': 'application/json'}
    response = requests.post(CAPI_URL, headers=headers, data=json.dumps(payload))

    FacebookEventLog.objects.create(
        event_name=event_name,
        status_code=response.status_code,
        response_text=response.text,
        source_url=event_source_url,
    )

    return response.status_code, response.text

def fb_page_view(request, url=None):
    return send_event(
        event_name='PageView',
        user_data=extract_user_data(request),
        event_source_url=url or request.build_absolute_uri()
    )

def fb_view_content(request, content_name=None, content_category=None, content_ids=None):
    return send_event(
        event_name='ViewContent',
        user_data=extract_user_data(request),
        custom_data={
            'content_name': content_name,
            'content_category': content_category,
            'content_ids': content_ids or [],
        },
        event_source_url=request.build_absolute_uri()
    )

def fb_lead_form(request):
    return send_event(
        event_name='Lead',
        user_data=extract_user_data(request),
        event_source_url=request.build_absolute_uri()
    )

def track_add_to_cart(request, content_ids=None, value=None, currency='INR'):
    return send_event(
        event_name='AddToCart',
        user_data=extract_user_data(request),
        custom_data={
            'content_ids': content_ids or [],
            'value': value,
            'currency': currency,
        },
        event_source_url=request.build_absolute_uri()
    )

def fb_initiate_checkout(request, content_ids=None, value=None, currency='INR'):
    return send_event(
        event_name='InitiateCheckout',
        user_data=extract_user_data(request),
        custom_data={
            'content_ids': content_ids or [],
            'value': value,
            'currency': currency,
        },
        event_source_url=request.build_absolute_uri()
    )

def fb_purchase(request, content_ids=None, value=None, currency='INR', transaction_id=None):
    return send_event(
        event_name='Purchase',
        user_data=extract_user_data(request),
        custom_data={
            'content_ids': content_ids or [],
            'value': value,
            'currency': currency,
            'transaction_id': transaction_id,
        },
        event_source_url=request.build_absolute_uri()
    )

def fb_custom_event(request, event_name, custom_data=None):
    return send_event(
        event_name=event_name,
        user_data=extract_user_data(request),
        custom_data=custom_data or {},
        event_source_url=request.build_absolute_uri()
    )
