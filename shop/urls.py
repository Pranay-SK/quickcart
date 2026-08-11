from django.urls import path, include
from . import views
from accounts import views as AccountViews


urlpatterns = [
    path('',AccountViews.shopperdashboard,name='shop'),
    path('profile/',views.shopprofile,name='shopprofile'),
    path('items_list/',views.items_list,name='items_list'),
    path('item-list/category/<int:pk>',views.items_by_category,name='items_by_category'),

    # Category CRUD

    path('item-list/category/add/',views.add_category,name='add_category'),
    path('item-list/category/edit/<int:pk>',views.edit_category,name='edit_category'),
    path('item-list/category/delete/<int:pk>',views.delete_category,name='delete_category'),

    # Item CRUD
    path('item-list/item/add/',views.add_item,name='add_item'),
    path('item-list/item/edit/<int:pk>',views.edit_item,name='edit_item'),
    path('item-list/item/delete/<int:pk>',views.delete_item,name='delete_item'),

    #Opening Hours
    path('opening-hours/',views.opening_hours,name='opening_hours'),
    path('opening-hours/add/', views.add_opening_hours, name='add_opening_hours'),
    path('opening-hours/remove/<int:pk>/', views.remove_opening_hours, name='remove_opening_hours'),

]