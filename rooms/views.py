from math import ceil
from django.shortcuts import render
from . import models


def all_rooms(request):
    page = int(request.GET.get('page', 1))
    page = page or 1
    page_size = 10
    limit = page_size * page
    offset = limit - page_size
    page_count = ceil(models.Room.objects.count() / page_size)
    rooms_all = models.Room.objects.all()[offset:limit]
    return render(request, 'rooms/home.html',
                  {'rooms': rooms_all, 'page': page, 'page_count': page_count,
                   'page_range': range(1, page_count)})
