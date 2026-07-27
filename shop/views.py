from django.shortcuts import get_object_or_404, render, redirect
from .forms import ShopForm
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from .models import Shop
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_shopper



@login_required(login_url='login')
@user_passes_test(check_role_shopper)
def shopprofile(request):
    profile=get_object_or_404(UserProfile,user=request.user)
    shop=get_object_or_404(Shop,user=request.user)

    if request.method=='POST':
        profile_form = UserProfileForm(request.POST,request.FILES,instance=profile)
        shop_form=ShopForm(request.POST,request.FILES,instance=shop)
        if profile_form.is_valid() and shop_form.is_valid():
            profile_form.save()
            shop_form.save()
            messages.success(request,'Settings updated.')
            return redirect('shopprofile')
        else:
            print(profile_form.errors)
            print(shop_form.errors)
    else:
        profile_form=UserProfileForm(instance=profile)
        shop_form=ShopForm(instance=shop)


    

    context={
        'profile_form':profile_form,
        'shop_form':shop_form,
        'profile':profile,
        'shop':shop,

    }
    return render(request,'shop/shopprofile.html',context)
