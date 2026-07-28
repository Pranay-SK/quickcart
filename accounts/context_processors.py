from shop.models import Shop
from django.conf import settings


def get_shop(request):
    try:
        shop = Shop.objects.get(user=request.user)
    except Exception:
        shop = None

    return dict(shop=shop)


def get_google_api(request):
    return {'GOOGLE_API_KEY': getattr(settings, 'GOOGLE_API_KEY', '')}