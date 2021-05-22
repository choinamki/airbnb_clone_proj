from django.utils import timezone
from django.views.generic import ListView, DetailView, View
from django.shortcuts import render
from . import models, forms


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


class SerachView(View):
    """ SearchView Definition """

    def get(self, request):
        country = request.GET.get('country')

        if country:
            form = forms.SearchForm(request.GET)

            if form.is_valid():

                city = form.cleaned_data.get('city')
                room_type = form.cleaned_data.get('room_type')
                price = form.cleaned_data.get('price')
                guests = form.cleaned_data.get('guests')
                bedrooms = form.cleaned_data.get('bedrooms')
                beds = form.cleaned_data.get('beds')
                baths = form.cleaned_data.get('baths')
                instant_book = form.cleaned_data.get('instant_book')
                superhost = form.cleaned_data.get('superhost')
                amenities = form.cleaned_data.get('amenities')
                facilities = form.cleaned_data.get('facilities')

                # -------------------------- filter ------------------------------------
                filter_args = {}

                if city != 'Anywhere':
                    filter_args['city__startswith'] = city

                filter_args['country'] = country

                if room_type is not None:
                    filter_args['room_type'] = room_type

                if price is not None:
                    filter_args['price_gte'] = price

                if guests is not None:
                    filter_args['guests_gte'] = guests

                if bedrooms is not None:
                    filter_args['beds_gte'] = bedrooms

                if baths is not None:
                    filter_args['baths_gte'] = baths

                if instant_book is True:
                    filter_args['instant_book'] = True

                if superhost is True:
                    filter_args['host__superhost'] = True

                for amenity in amenities:
                    filter_args['amenities'] = amenity

                for facility in facilities:
                    filter_args['facilities'] = facility

                rooms = models.Room.objects.filter(**filter_args)
                return render(request, 'rooms/search.html', {'form': form, 'rooms': rooms})
        else:
            form = forms.SearchForm()
        return render(request, 'rooms/search.html', {'form': form})

