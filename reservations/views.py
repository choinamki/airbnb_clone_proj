import datetime
from django.views.generic import View
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.shortcuts import render
from rooms import models as room_models
from . import models


class CreateError(Exception):
    pass


def create(request, room, year, month, day):
    date_obj = datetime.datetime(year=year, month=month, day=day)
    try:
        room = room_models.Room.objects.get(pk=room)
        models.BookedDay.objects.get(day=date_obj, reservation__room=room)
        raise CreateError()
    except (room_models.Room.DoesNotExist, CreateError):
        messages.error(request, 'Can not Reserve That Room')
        return redirect(reverse('core:home'))
    except models.BookedDay.DoesNotExist:
        reservations = models.Reservation.objects.create(
            guest=request.user,
            room=room,
            check_in=date_obj,
            check_out=date_obj + datetime.timedelta(days=1),
        )
        return redirect(reverse("reservations:detail", kwargs={"pk": reservations.pk}))


class ReservationDetailView(View):
    def get(self):
        pass
