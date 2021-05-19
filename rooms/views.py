from django.utils import timezone
from django.http import Http404
from django.urls import reverse
from django.views.generic import ListView
from django.shortcuts import render, redirect
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


def room_detail(request, pk):
    try:
        room = models.Room.objects.get(pk=pk)
        return render(request, 'rooms/detail.html', {'room': room})
    except models.Room.DoesNotExist:
        raise    Http404()

