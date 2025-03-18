from django.shortcuts import render
from scetch.models import Booking, QueueSlot


def adminka_home(request):
    return render(request, 'adminka/adminka_home.html')
