from datetime import date, datetime

from django.db.models import Prefetch
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

from items.models import Category, Product
from .models import Cart
from shop.models import Shop,OpeningHour
from .context_processors import get_cart_amounts, get_cart_counter
from django.db.models import Q

from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D  # ``D`` is a shortcut for ``Distance``
from django.contrib.gis.db.models.functions import Distance

#from decimal import Decimal

def marketplace(request):
    shops=Shop.objects.filter(is_approved=True,user__is_active=True)
    shops_count=shops.count()
    context={
        'shops':shops,
        'shops_count': shops_count,
    }
    return render(request,'marketplace/listings.html',context)

def shop_detail(request,shop_slug):
    shop=get_object_or_404(Shop, shop_slug=shop_slug)
    categories=Category.objects.filter(shop=shop).prefetch_related(
        Prefetch(
            'shopitems',
             queryset=Product.objects.filter(is_available=True),
             )
    )


    opening_hours = OpeningHour.objects.filter(shop=shop).order_by('day','-from_hour')
    
    # check current day's opening hours.
    today_date = date.today()
    today = today_date.isoweekday()
    currnt_opening_hours = OpeningHour.objects.filter(shop=shop, day=today).order_by('from_hour')
    is_open = shop.is_open()
    today_display = 'Closed'
    if is_open:
        now_time = datetime.now().time()
        for hour in currnt_opening_hours:
            if hour.is_closed or not hour.from_hour or not hour.to_hour:
                continue
            start = datetime.strptime(hour.from_hour, "%I:%M %p").time()
            end = datetime.strptime(hour.to_hour, "%I:%M %p").time()
            if start <= now_time < end:
                today_display = f"{hour.from_hour} - {hour.to_hour}"
                break

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        #cart_count=get_cart_counter(request)
    else:
        cart_items = None
        
    context={
        'shop': shop,
        'categories': categories,
        'cart_items': cart_items,
       # 'cart_count': cart_count,
        'opening_hours': opening_hours,
        'currnt_opening_hours': currnt_opening_hours,
        'is_open': is_open,
        'today_display': today_display,
    }
    return render(request,'marketplace/shop_detail.html',context)



def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Check if the product exists
            try:
                product = Product.objects.get(id=product_id)
                # Check if the user has already added that product to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, Product=product)
                    # Increase the cart quantity
                    chkCart.quantity += 1
                    chkCart.save()
                    return JsonResponse({
                        'status': 'Success', 
                        'message': 'Increased the cart quantity', 
                        'cart_counter': get_cart_counter(request), 
                        'qty': chkCart.quantity, 
                        'cart_amount': get_cart_amounts(request)
                                         })
                except:
                    chkCart = Cart.objects.create(user=request.user, Product=product, quantity=1)
                    return JsonResponse({
                        'status': 'Success', 
                        'message': 'Added the product to the cart', 
                        'cart_counter': get_cart_counter(request), 
                        'qty': chkCart.quantity, 
                     'cart_amount': get_cart_amounts(request)
                    })
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This product does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
        
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})


def decrease_cart(request, product_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Check if the product exists
            try:
                product = Product.objects.get(id=product_id)
                # Check if the user has already added that product to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, Product=product)
                    # decrease the cart quantity
                    if chkCart.quantity > 1:
                        chkCart.quantity -= 1
                        chkCart.save()
                        qty = chkCart.quantity
                        cart_id = chkCart.id
                    else:
                        cart_id = chkCart.id
                        chkCart.delete()
                        qty = 0
                    return JsonResponse({
                        'status': 'Success', 
                        'message': 'Cart updated', 
                        'cart_counter': get_cart_counter(request), 
                        'qty': qty, 
                        'cart_id': cart_id,
                        'cart_amount': get_cart_amounts(request)
                    })
                except Cart.DoesNotExist:
                    return JsonResponse({
                        'status': 'Failed', 
                        'message': 'You do not have this product in your cart', 
                    })
            except Product.DoesNotExist:
                return JsonResponse({'status': 'Failed', 'message': 'This product does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})

@login_required(login_url='login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_amounts = get_cart_amounts(request)
    context = {
        'cart_items': cart_items,
        **cart_amounts,
    }
    return render(request, 'marketplace/cart.html', context)


def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                # Check if the cart item exists
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({
                        'status': 'Success', 
                        'message': 'Cart item has been deleted!', 
                        'cart_counter': get_cart_counter(request), 
                       'cart_amount': get_cart_amounts(request)
                        })
            except:
                return JsonResponse({'status': 'Failed', 'message': 'Cart Item does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})


def search(request):
    if not 'address' in request.GET:
        return redirect('marketplace')
    else:
        address = request.GET.get('address', '')
        latitude = request.GET.get('lat', '')
        longitude = request.GET.get('lng', request.GET.get('log', ''))
        radius = request.GET.get('radius', '')
        keyword = request.GET.get('keyword', '')

        # get shop ids that has product has user is looking for
        fetch_shops_by_product=Product.objects.filter(product_title__icontains=keyword,is_available=True).values_list('shop',flat=True)
         # print(fetch_shops_by_product)
        shops=Shop.objects.filter(Q(id__in=fetch_shops_by_product) | Q(owner_name__icontains=keyword,is_approved=True,user__is_active=True))

        if latitude and longitude and radius:
            pnt = GEOSGeometry('POINT(%s %s)' %(longitude,latitude))

            shops=  Shop.objects.filter(Q(id__in=fetch_shops_by_product) | Q(owner_name__icontains=keyword,is_approved=True,user__is_active=True),user_profile__location__distance_lte=(pnt, D(km=radius))).annotate(distance=Distance("user_profile__location",pnt)).order_by("distance")

            for s in shops:
                s.kms=round(s.distance.km,1)

            shop_count = shops.count()
            context = {
                'shops': shops,
                'shops_count': shop_count,
                'source_location': address,
            }

            return render(request,'marketplace/listings.html',context)


