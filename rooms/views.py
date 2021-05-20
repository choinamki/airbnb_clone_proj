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
    guest = int(request.GET.get('guest', 0))
    bedrooms = int(request.GET.get('bedrooms', 0))
    beds = int(request.GET.get('beds', 0))
    baths = int(request.GET.get('baths', 0))
    instant = request.GET.get('instant', False)
    super_host = request.GET.get('super_host', False)

    s_amenities = request.GET.getlist('amenities')
    s_facilities = request.GET.getlist('facilities')

    form = {'city': city, 's_room_type': room_type, 's_country': country,
            'price': price, 'guest': guest, 'bedrooms': bedrooms, 'beds': beds, 'baths': baths,
            's_amenities': s_amenities, 's_facilities': s_facilities, 'instant': instant, 'super_host': super_host}

    choice = {'countries': countries, 'room_types': room_types, 'amenities': amenities, 'facilities': facilities}

    return render(request, 'rooms/search.html', {**form, **choice})
