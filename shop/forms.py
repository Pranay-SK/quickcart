from django import forms

from .models import Shop

class ShopForm(forms.ModelForm):
    class Meta:
        model=Shop
        fields=['owner_name', 'shop_license']