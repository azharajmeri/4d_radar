from django.shortcuts import render
from radar.models import SpeedRecord

def radar(request):
    return render(request, "radar/index.html")
