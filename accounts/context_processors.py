from accounts.models import UserProfile
from shop.models import Shop
from django.conf import settings


def get_shop(request):
    try:
        shop = Shop.objects.get(user=request.user)
    except Exception:
        shop = None

    return dict(shop=shop)

def get_user_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except:
        user_profile = None
    return dict(user_profile=user_profile)

def get_google_api(request):
    return {'GOOGLE_API_KEY': getattr(settings, 'GOOGLE_API_KEY', '')}

def get_paypal_client_id(request):
    return {'PAYPAL_CLIENT_ID': settings.PAYPAL_CLIENT_ID}