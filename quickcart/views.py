from django.shortcuts import render
from django.http import HttpResponse

from shop.models import Shop


def home(request):
    shops=Shop.objects.filter(is_approved=True,user__is_active=True)[:8]
    #print(shops)
    context={
        'shops':shops,
    }
    return render(request,'home.html',context)