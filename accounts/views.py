from django.http import HttpResponse

from django.shortcuts import redirect, render

from django.contrib import messages,auth

from .forms import UserForm
from .models import User, UserProfile
from shop.forms import ShopForm
from .utils import detectUser, send_verification_email
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from shop.models import Shop
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

             # Send verification email
            
            mail_subject="Please activate your account"
            email_template='accounts/emails/account_verification_email.html'
            send_verification_email(request, user,mail_subject,email_template)
            messages.success(request, 'Your account has been registered sucessfully!')
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

            # Send verification email
            mail_subject="Please activate your account"
            email_template='accounts/emails/account_verification_email.html'
            send_verification_email(request, user,mail_subject,email_template)
            
            messages.success(request, 'Your account has been registered successfully! Please wait for the approval of your shop to get started.')
           

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

def activate(request, uidb64, token):
    # Activate the user by setting the is_active status to True
    try:
        uid= urlsafe_base64_decode(uidb64).decode()
        user=User._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user=None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,'Congratulation! Your account is activated.')
        return redirect('myAccount')
    else:
        messages.error(request,'Invalid activation link')
        return redirect('myAccount')

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
@login_required(login_url='login')
@user_passes_test(check_role_shopper)
def shopperdashboard(request):
    shop = Shop.objects.get(user=request.user)
    context = {
        'shop': shop,
    }
    return render(request, 'accounts/shopperdashboard.html', context)

def forgot_password(request):
    if request.method=='POST':
        email=request.POST['email']

        if User.objects.filter(email=email).exists():
            user=User.objects.get(email__exact=email)

            # Send reset password email
            mail_subject='Reset Your Password'
            email_template='accounts/emails/reset_password_email.html'
            send_verification_email(request,user,mail_subject,email_template)

            messages.success(request,'Password reset link has been sent to your email address.')
            return redirect('login')
        else:
             messages.error(request,'Account does not exist')
             return redirect('forgot_password')

    return render(request,'accounts/forgot_password.html')

def reset_password_validate(request,uidb64,token):
    # validate the user by decoding the token and user pk

    try:
        uid= urlsafe_base64_decode(uidb64).decode()
        user=User._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        messages.info(request,'Please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request,'This link has been expired !')
        return redirect('myAccount')

    

def reset_password(request):
    if request.method=='POST':
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']

        if password==confirm_password:
            pk=request.session.get('uid')
            user=User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active=True
            user.save()
            messages.success(request,'Password reset successful')
            return redirect('login')
        else:
            messages.error(request,'Passwords does not match !')
            return redirect('reset_password')

    return render(request,'accounts/reset_password.html')