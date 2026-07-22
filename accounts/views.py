from django.http import HttpResponse

from django.shortcuts import redirect, render

from django.contrib import messages,auth

from .forms import UserForm
from .models import User, UserProfile
from shop.forms import ShopForm
from .utils import detectUser
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
# Create your views here.



# Restrict the shopper from accessing the customer page

def check_role_shopper(user):
    if user.role==1:
       return True
    else:
        raise PermissionDenied
    
# Restrict the customer from accessing the shopper page

def check_role_customer(user):
    if user.role==2:
       return True
    else:
        raise PermissionDenied

def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in.')
        return redirect('dashboard')
    elif request.method=='POST':
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
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in.')
        return redirect('dashboard')
    elif request.method=='POST':
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

def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in.')
        return redirect('myAccount')
    elif request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']

        user=auth.authenticate( email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('myAccount')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request, 'You are logged out.')
    return redirect('login')

@login_required(login_url='login')
def myAccount(request):
    user=request.user
    redirectUrl=detectUser(user)
    return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custdashboard(request):
    return render(request, 'accounts/custdashboard.html')

@login_required(login_url='login')
@user_passes_test(check_role_shopper)
def shopperdashboard(request):
    return render(request, 'accounts/shopperdashboard.html')