from django.shortcuts import get_object_or_404, render, redirect
from .forms import ShopForm
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from .models import Shop
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_shopper
from items.models import Category, Product
from items.forms import CategoryForm
from django.template.defaultfilters import slugify


def get_shop(request):
    shop=Shop.objects.get(user=request.user)
    return shop


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

@login_required(login_url='login')
@user_passes_test(check_role_shopper)
def items_list(request):
    shop =  get_shop(request)
    categories = Category.objects.filter(shop=shop).order_by('created_at')
    context = {
        'categories': categories,
        'shop': shop,
    }
    return render(request, 'shop/items_list.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_shopper)
def items_by_category(request, pk=None):
    shop = get_shop(request)
    category = get_object_or_404(Category, pk=pk)
    items = Product.objects.filter(shop=shop, category=category)
    context = {
        'items': items,
        'category': category,
    }
    return render(request, 'shop/items_by_category.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_shopper)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.shop = get_shop(request)
            
            category.save() # here the category id will be generated
            category.slug = slugify(category_name)+'-'+str(category.id) # chicken-15
            category.save()
            messages.success(request, 'Category added successfully!')
            return redirect('items_list')
        else:
            print(form.errors)

    else:
        form = CategoryForm()
    
    shop = get_shop(request)
    context = {
        'form': form,
        'shop': shop,
    }
    return render(request, 'shop/add_category.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_shopper)
def edit_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.shop = get_shop(request)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('items_list')
        else:
            print(form.errors)

    else:
        form = CategoryForm(instance=category)
    
    shop = get_shop(request)
    context = {
        'form': form,
        'category': category,
        'shop': shop,
    }
    return render(request, 'shop/edit_category.html', context)

def delete_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category has been deleted successfully!')
    return redirect('items_list')