from django.contrib import admin

from .models import Cart,Tax

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'Product', 'quantity', 'updated_at')
    # list_filter = ('user', 'Product', 'created_at', 'updated_at')
    # search_fields = ('user__username', 'Product__name')


class TaxAdmin(admin.ModelAdmin):
    list_display = ('tax_type', 'tax_percentage', 'is_active')

admin.site.register(Cart, CartAdmin)
admin.site.register(Tax,TaxAdmin)
