from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from django_countries import countries
from . import models


class HomeView(ListView):
    """ HomeView Definition"""
    model = models.Room
    paginate_by = 10
    ordering = 'created'
    context_object_name = 'rooms'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context['now'] = now
        return context


class RoomDetail(DetailView):
    """ RoomDetailVeiw Definition"""
    model = models.Room
    pk_url_kwarg = 'pk'


def search(request):
    city = request.GET.get('city', 'Anywhere')
    city = str.capitalize(city)
    country = request.GET.get('country', 'kr')
    room_type = int(request.GET.get('room_type', 0))
    room_types = models.RoomType.objects.all()
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()

    price = int(request.GET.get('price', 0))
    guests = int(request.GET.get('guests', 0))
    bedrooms = int(request.GET.get('bedrooms', 0))
    beds = int(request.GET.get('beds', 0))
    baths = int(request.GET.get('baths', 0))
    instant = bool(request.GET.get('instant', False))
    superhost = bool(request.GET.get('superhost', False))

    s_amenities = request.GET.getlist('amenities')
    s_facilities = request.GET.getlist('facilities')

    form = {'city': city, 's_room_type': room_type, 's_country': country,
            'price': price, 'guests': guests, 'bedrooms': bedrooms, 'beds': beds, 'baths': baths,
            's_amenities': s_amenities, 's_facilities': s_facilities, 'instant': instant, 'superhost': superhost}

    choice = {'countries': countries, 'room_types': room_types, 'amenities': amenities, 'facilities': facilities}

    # -------------------------- filter ------------------------------------
    filter_args = {}

    if city != 'Anywhere':
        filter_args['city__startswith'] = city

    filter_args['country'] = country

    if room_type != 0:
        filter_args['room_type__pk'] = room_type

    if price != 0:
        filter_args['price_gte'] = price

    if guests != 0:
        filter_args['guests_gte'] = guests

    if bedrooms != 0:
        filter_args['beds_gte'] = bedrooms

    if baths != 0:
        filter_args['baths_gte'] = baths

    if instant:
        filter_args['instant_book'] = True

    if superhost:
        filter_args['host__superhost'] = True

    if len(s_amenities) > 0:
        for s_amenity in s_amenities:
            filter_args['amenities__pk'] = int(s_amenity)

    if len(s_facilities) > 0:
        for s_facility in s_facilities:
            filter_args['amenities__pk'] = int(s_facility)

    rooms = models.Room.objects.filter(**filter_args)

    return render(request, 'rooms/search.html', {**form, **choice, 'rooms': rooms})
