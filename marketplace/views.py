from django.db.models import Prefetch
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from items.models import Category, Product
from .models import Cart
from shop.models import Shop
from .context_processors import get_cart_amounts, get_cart_counter

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

    if request.user.is_authenticated:
        cart_items=Cart.objects.filter(user=request.user)
        #cart_count=get_cart_counter(request)
    else:
        cart_items=None
        
    context={
        'shop':shop,
        'categories':categories,
        'cart_items': cart_items,
       # 'cart_count': cart_count,
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
    context = {
        'cart_items': cart_items,
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



