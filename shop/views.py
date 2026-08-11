from unicodedata import category

from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect

import shop
from .forms import ShopForm, OpeningHourForm
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from .models import Shop, OpeningHour
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_shopper
from items.models import Category, Product
from items.forms import CategoryForm, ProductForm
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
        'shop': shop,
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
@login_required(login_url='login')
@user_passes_test(check_role_shopper)
def delete_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category has been deleted successfully!')
    return redirect('items_list')


@login_required(login_url='login')
@user_passes_test(check_role_shopper)
def add_item(request):
    """Add a new product for the current  shop."""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product_title = form.cleaned_data.get('product_title')
            product = form.save(commit=False)
            product.shop = get_shop(request)
            product.save()  # here the product id will be generated
            # create unique slug using id to avoid conflicts
            if product_title:
                product.slug = slugify(product_title) + '-' + str(product.id)
            else:
                product.slug = str(product.id)
            product.save()
            messages.success(request, 'Product added successfully!')
            return redirect('items_by_category', product.category.id)
        else:
            print(form.errors)

    else:
        form = ProductForm()
        # modify this form
        form.fields['category'].queryset = Category.objects.filter(shop=get_shop(request))
    context = {
        'form': form,
        'shop': get_shop(request),
    }
    return render(request, 'shop/add_item.html', context)



@login_required(login_url='login')
@user_passes_test(check_role_shopper)
def edit_item(request, pk=None):
    item = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            product_title = form.cleaned_data['product_title']
            product = form.save(commit=False)
            product.shop = get_shop(request)
            product.slug = slugify(product_title) + '-' + str(product.id)
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('items_by_category', item.category.id)
        else:
            print(form.errors)

    else:
        form = ProductForm(instance=item)
        form.fields['category'].queryset = Category.objects.filter(shop=get_shop(request))
    shop = get_shop(request)
    # ensure template has access to the item and its category
    category = item.category
    context = {
        'form': form,
        'item': item,
        'category': category,
        'shop': shop,
    }
    return render(request, 'shop/edit_item.html', context)

def delete_item(request, pk=None):
    item = get_object_or_404(Product, pk=pk)
    category_id = item.category.id  # Store the category ID before deletion
    item.delete()
    messages.success(request, 'Product has been deleted successfully!')
    return redirect('items_by_category', category_id)  # Redirect to the category page after deletion


@login_required(login_url='login')
@user_passes_test(check_role_shopper)
def opening_hours(request):
    shop = get_shop(request)
    opening_hours = OpeningHour.objects.filter(shop=shop)
    form = OpeningHourForm()
    context = {
        'shop': shop,
        'form': form,
        'opening_hours': opening_hours,
    }
    return render(request, 'shop/opening_hours.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_shopper)
def add_opening_hours(request):
    # handle the data and save them inside the database
    if request.method == 'POST':
        form = OpeningHourForm(request.POST)
        if form.is_valid():
            hour = form.save(commit=False)
            hour.shop = get_shop(request)
            if hour.is_closed:
                if OpeningHour.objects.filter(shop=hour.shop, day=hour.day, is_closed=True).exists():
                    error_message = f'{hour.get_day_display()} is already marked as closed.'
                    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                        return JsonResponse({'status': 'failed', 'message': error_message})
                    messages.error(request, error_message)
                    return redirect('opening_hours')
                hour.from_hour = ''
                hour.to_hour = ''
            try:
                hour.save()
            except IntegrityError:
                error_message = 'That opening slot already exists for this day.'
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'status': 'failed', 'message': error_message})
                messages.error(request, error_message)
                return redirect('opening_hours')

            if hour.is_closed:
                response = {'status': 'success', 'id': hour.id, 'day': hour.get_day_display(), 'is_closed': 'Closed'}
            else:
                response = {'status': 'success', 'id': hour.id, 'day': hour.get_day_display(), 'from_hour': hour.from_hour, 'to_hour': hour.to_hour}

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse(response)
            return redirect('opening_hours')

        error_message = form.errors.as_text() or 'Please fill all required fields correctly.'
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'failed', 'message': error_message})
        messages.error(request, error_message)
        return redirect('opening_hours')

    return HttpResponse('Invalid request')


@login_required(login_url='login')
@user_passes_test(check_role_shopper)
def remove_opening_hours(request, pk=None):
    hour = get_object_or_404(OpeningHour, pk=pk)
    hour.delete()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'id': pk})
    return redirect('opening_hours')