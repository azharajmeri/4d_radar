import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from radar.models import SpeedRecord, Display, SpeedLimit, Radar, TriggerPoint, ConfiguredConnection, Location
from radar.utils import save_configurations


@login_required
def radar(request):
    # Retrieve all rows for lanes 1 to 4
    display1 = Display.objects.filter(lane_number=0).first()
    display2 = Display.objects.filter(lane_number=1).first()
    display3 = Display.objects.filter(lane_number=2).first()
    display4 = Display.objects.filter(lane_number=3).first()

    # Initialize form data
    form_data = {
        'display1': {'ip': '', 'port': '', 'camera_ip': '', 'camera_user': '', 'camera_pass': ''},
        'display2': {'ip': '', 'port': '', 'camera_ip': '', 'camera_user': '', 'camera_pass': ''},
        'display3': {'ip': '', 'port': '', 'camera_ip': '', 'camera_user': '', 'camera_pass': ''},
        'display4': {'ip': '', 'port': '', 'camera_ip': '', 'camera_user': '', 'camera_pass': ''}
    }

    # Populate form data if available
    if display1:
        form_data['display1']['ip'] = display1.ip or ''
        form_data['display1']['port'] = display1.port or ''
        form_data['display1']['camera_ip'] = display1.camera_ip or ''
        form_data['display1']['camera_user'] = display1.camera_user or ''
        form_data['display1']['camera_pass'] = display1.camera_pass or ''

    if display2:
        form_data['display2']['ip'] = display2.ip or ''
        form_data['display2']['port'] = display2.port or ''
        form_data['display2']['camera_ip'] = display2.camera_ip or ''
        form_data['display2']['camera_user'] = display2.camera_user or ''
        form_data['display2']['camera_pass'] = display2.camera_pass or ''

    if display3:
        form_data['display3']['ip'] = display3.ip or ''
        form_data['display3']['port'] = display3.port or ''
        form_data['display3']['camera_ip'] = display3.camera_ip or ''
        form_data['display3']['camera_user'] = display3.camera_user or ''
        form_data['display3']['camera_pass'] = display3.camera_pass or ''

    if display4:
        form_data['display4']['ip'] = display4.ip or ''
        form_data['display4']['port'] = display4.port or ''
        form_data['display4']['camera_ip'] = display4.camera_ip or ''
        form_data['display4']['camera_user'] = display4.camera_user or ''
        form_data['display4']['camera_pass'] = display4.camera_pass or ''

    speed_records = SpeedRecord.objects.all().order_by("-created_at")[:10]

    speed_limit_obj = SpeedLimit.objects.first()
    radar_obj = Radar.objects.first()

    trigger_point_obj = TriggerPoint.objects.first()

    configured_connection_obj = ConfiguredConnection.objects.first()

    location = Location.objects.first()

    return render(request, "radar/index.html",
                  {'form_data': form_data, 'speed_records': speed_records,
                   'speed_limit_obj': speed_limit_obj, 'radar_obj': radar_obj,
                   'trigger_point_obj': trigger_point_obj,
                   'location': location,
                   'connection_status': configured_connection_obj.status if configured_connection_obj else False})


def save_config(request):
    save_configurations(request.POST)
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
                'id': speed_rec.id,
                'frame': speed_rec.frame_number,
                'speed': speed_rec.speed,
                'time': speed_rec.time.strftime("%d-%m-%Y %H:%M:%S"),
                'laneNumber': speed_rec.lane_number
            }
        }
    )
    return HttpResponse("Notified!")
