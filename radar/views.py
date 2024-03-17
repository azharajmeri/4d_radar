import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import HttpResponse
from django.shortcuts import render
from radar.models import SpeedRecord


def radar(request):
    return render(request, "radar/index.html")


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
