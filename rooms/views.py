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

    form = {'city': city, 's_room_type': room_type, 's_country': country}

    choice = {'countries': countries, 'room_types': room_types}

    return render(request, 'rooms/search.html', {**form, **choice})
