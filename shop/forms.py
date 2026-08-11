from datetime import datetime

from django import forms

from .models import Shop,OpeningHour
from accounts.validators import allow_only_images_validator

class ShopForm(forms.ModelForm):
    shop_license=forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}),validators=[allow_only_images_validator])
    class Meta:
        model=Shop
        fields=['owner_name', 'shop_license']


class OpeningHourForm(forms.ModelForm):
    class Meta:
        model = OpeningHour
        fields = ['day', 'from_hour', 'to_hour', 'is_closed']

    def clean(self):
        cleaned_data = super().clean()
        day = cleaned_data.get('day')
        from_hour = cleaned_data.get('from_hour')
        to_hour = cleaned_data.get('to_hour')
        is_closed = cleaned_data.get('is_closed')

        if not day:
            raise forms.ValidationError('Please select a day.')

        if is_closed:
            cleaned_data['from_hour'] = ''
            cleaned_data['to_hour'] = ''
            return cleaned_data

        if not from_hour or not to_hour:
            raise forms.ValidationError('Please select both opening and closing time unless the slot is closed.')

        try:
            start = datetime.strptime(from_hour, '%I:%M %p')
            end = datetime.strptime(to_hour, '%I:%M %p')
        except ValueError:
            raise forms.ValidationError('Invalid time selected.')

        if start >= end:
            raise forms.ValidationError('Opening time must be before closing time.')

        return cleaned_data