from django import forms

from .models import Shop
from accounts.validators import allow_only_images_validator

class ShopForm(forms.ModelForm):
    shop_license=forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}),validators=[allow_only_images_validator])
    class Meta:
        model=Shop
        fields=['owner_name', 'shop_license']