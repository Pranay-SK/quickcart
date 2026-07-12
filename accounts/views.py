from django.http import HttpResponse

from django.shortcuts import redirect, render

from django.contrib import messages

from .forms import UserForm
from .models import User, UserProfile
from shop.forms import ShopForm
# Create your views here.

def registerUser(request):
    if request.method=='POST':
        form=UserForm(request.POST)
        if form.is_valid():
            #create the user using the form
            # password=form.cleaned_data.get('password')
            # user=form.save(commit=False)
            # user.set_password(password)
            # user.role=User.CUSTOMER
            # user.save()

            #create the user using create_user method

            first_name=form.cleaned_data.get('first_name')
            last_name=form.cleaned_data.get('last_name')
            username=form.cleaned_data.get('username')
            email=form.cleaned_data.get('email')
            password=form.cleaned_data.get('password')
            user=User.objects.create_user(first_name=first_name, last_name=last_name, username=username,email=email, password=password)
            user.role=User.CUSTOMER
            user.save()
            messages.success(request, 'Your account has been registered successfully')

            return redirect('registerUser')
        else:
            print('Form is not valid')
            print(form.errors)
    else:
        form=UserForm()
    context={
        'form':form,
        }
    return render(request, 'accounts/registerUser.html', context)

def registerShop(request):
    if request.method=='POST':
        # Store the data and create the user
        form=UserForm(request.POST)
        shop_form=ShopForm(request.POST, request.FILES)
        if form.is_valid() and shop_form.is_valid():
            first_name=form.cleaned_data.get('first_name')
            last_name=form.cleaned_data.get('last_name')
            username=form.cleaned_data.get('username')
            email=form.cleaned_data.get('email')
            password=form.cleaned_data.get('password')
            user=User.objects.create_user(first_name=first_name, last_name=last_name, username=username,email=email, password=password)
            user.role=User.SHOPPER
            user.save()
            shop=shop_form.save(commit=False)
            shop.user=user
            user_profile=UserProfile.objects.get(user=user)
            shop.user_profile=user_profile
            shop.save()
            messages.success(request, 'Your account has been registered successfully ! Please wait for the approval of your shop to get started.')

            return redirect('registerShop')
        else:
            print('Form is not valid')
            print(form.errors)
            #print(shop_form.errors)
    else:
        form=UserForm()
        shop_form=ShopForm()

    context={
        'form':form,
        'shop_form':shop_form,
    }

    return render(request, 'accounts/registerShop.html',context)