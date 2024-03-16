from django.shortcuts import render


def radar(request):
    return render(request, "radar/index.html")
