from django.contrib import admin

from shop.models import Shop

class ShopAdmin(admin.ModelAdmin):
    list_display=['user', 'owner_name', 'is_approved', 'created_at']
    list_display_links=['user', 'owner_name']
    list_editable=['is_approved',]

admin.site.register(Shop, ShopAdmin)