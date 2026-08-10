from django.shortcuts import render
from django.http import HttpResponse

from shop.models import Shop

from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D  # ``D`` is a shortcut for ``Distance``
from django.contrib.gis.db.models.functions import Distance



def get_or_set_current_location(request):
    if 'lat' in request.session:
        lat = request.session['lat']
        lng = request.session['lng']
        return lng, lat
    elif 'lat' in request.GET:
        lat = request.GET.get('lat')
        lng = request.GET.get('lng')
        request.session['lat'] = lat
        request.session['lng'] = lng
        return lng, lat
    else:
        return None

def home(request):
    if get_or_set_current_location(request) is not None:


        pnt = GEOSGeometry('POINT(%s %s)' %(get_or_set_current_location(request)))
        
        shops=  Shop.objects.filter(user_profile__location__distance_lte=(pnt, D(km=100000))).annotate(distance=Distance("user_profile__location",pnt)).order_by("distance")

        for s in shops:
            s.kms=round(s.distance.km,1)

    else:
        shops=Shop.objects.filter(is_approved=True,user__is_active=True)[:8]
    
    #print(shops)
    context={
        'shops':shops,
    }
    return render(request,'home.html',context)