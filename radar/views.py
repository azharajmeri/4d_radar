import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import HttpResponse
from django.shortcuts import render, redirect
from radar.models import SpeedRecord, Display, SpeedLimit, Radar


def radar(request):
    # Retrieve all rows for lanes 1 to 4
    display1 = Display.objects.filter(lane_number=0).first()
    display2 = Display.objects.filter(lane_number=1).first()
    display3 = Display.objects.filter(lane_number=2).first()
    display4 = Display.objects.filter(lane_number=3).first()

    # Initialize form data
    form_data = {
        'display1': {'ip': '', 'port': ''},
        'display2': {'ip': '', 'port': ''},
        'display3': {'ip': '', 'port': ''},
        'display4': {'ip': '', 'port': ''}
    }

    # Populate form data if available
    if display1:
        form_data['display1']['ip'] = display1.ip or ''
        form_data['display1']['port'] = display1.port or ''
    if display2:
        form_data['display2']['ip'] = display2.ip or ''
        form_data['display2']['port'] = display2.port or ''
    if display3:
        form_data['display3']['ip'] = display3.ip or ''
        form_data['display3']['port'] = display3.port or ''
    if display4:
        form_data['display4']['ip'] = display4.ip or ''
        form_data['display4']['port'] = display4.port or ''

    speed_records = SpeedRecord.objects.all().order_by("-created_at")[:10]

    speed_limit_obj = SpeedLimit.objects.first()
    radar_obj = Radar.objects.first()

    return render(request, "radar/index.html",
                  {'form_data': form_data, 'speed_records': speed_records,
                   "speed_limit_obj": speed_limit_obj, "radar_obj": radar_obj})


def save_display_config(request):
    ip1 = request.POST.get('ip1')
    port1 = int(request.POST.get('port1', 0)) if request.POST.get('port1') else None
    lane_number1 = 0

    ip2 = request.POST.get('ip2')
    port2 = int(request.POST.get('port2', 0)) if request.POST.get('port2') else None
    lane_number2 = 1

    ip3 = request.POST.get('ip3')
    port3 = int(request.POST.get('port3', 0)) if request.POST.get('port3') else None
    lane_number3 = 2

    ip4 = request.POST.get('ip4')
    port4 = int(request.POST.get('port4', 0)) if request.POST.get('port4') else None
    lane_number4 = 3

    # Save or update Display objects
    Display.objects.update_or_create(lane_number=lane_number1, defaults={'ip': ip1, 'port': port1})
    Display.objects.update_or_create(lane_number=lane_number2, defaults={'ip': ip2, 'port': port2})
    Display.objects.update_or_create(lane_number=lane_number3, defaults={'ip': ip3, 'port': port3})
    Display.objects.update_or_create(lane_number=lane_number4, defaults={'ip': ip4, 'port': port4})

    return redirect('home')


def save_speed_limit(request):
    speed_limit = request.POST.get('speed-limit')
    speed_limit_obj = SpeedLimit.objects.first()
    if speed_limit_obj:
        # Update the speed limit value
        speed_limit_obj.limit = speed_limit
        speed_limit_obj.save()
    else:
        # Create a new SpeedLimit object if none exists
        SpeedLimit.objects.create(limit=speed_limit)

    return redirect('home')


def save_radar_config(request):
    ip = request.POST.get('radar_ip')
    host_ip = request.POST.get('host_ip')
    radar_obj = Radar.objects.first()
    if radar_obj:
        # Update the Radar value
        radar_obj.ip = ip
        radar_obj.host_ip = host_ip
        radar_obj.save()
    else:
        # Create a new Radar object if none exists
        Radar.objects.create(ip=ip, host_ip=host_ip)

    return redirect('home')


def radar_update(request):
    # Broadcast message to channel group
    channel_layer = get_channel_layer()
    speed_rec = SpeedRecord.objects.get(id=json.loads(request.body)["instance_id"])
    async_to_sync(channel_layer.group_send)(
        "radar",
        {
            "type": "chat_message",
            "message": {
                'speed': speed_rec.speed,
                'time': speed_rec.time.strftime("%H:%M:%S"),
                'laneNumber': speed_rec.lane_number
            }
        }
    )
    return HttpResponse("Notified!")
