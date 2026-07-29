from django.contrib import admin
from .models import Category,Product

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'shop', 'updated_at')
    search_fields = ('category_name', 'shop__owner_name')




class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('product_title',)}
    list_display = ('product_title', 'category', 'shop', 'price', 'is_available', 'updated_at')
    search_fields = ('product_title', 'category__category_name', 'shop__owner_name', 'price')
    list_filter = ('is_available',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)