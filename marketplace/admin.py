from django.contrib import admin

from .models import Cart

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'Product', 'quantity', 'updated_at')
    # list_filter = ('user', 'Product', 'created_at', 'updated_at')
    # search_fields = ('user__username', 'Product__name')

admin.site.register(Cart, CartAdmin)
