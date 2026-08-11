from django.contrib import admin

from shop.models import Shop,OpeningHour

class ShopAdmin(admin.ModelAdmin):
    list_display=['user', 'owner_name', 'is_approved', 'created_at']
    list_display_links=['user', 'owner_name']
    list_editable=['is_approved',]


class OpeningHourAdmin(admin.ModelAdmin):
    list_display = ('shop', 'day', 'from_hour', 'to_hour')

admin.site.register(Shop, ShopAdmin)
admin.site.register(OpeningHour,OpeningHourAdmin)