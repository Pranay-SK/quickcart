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

]