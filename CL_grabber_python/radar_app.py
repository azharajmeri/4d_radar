import datetime
import math

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

import cl_grabber as grabber
from radar.models import SpeedRecord


def onTrackedObjCallback(trackList):
    """
    This method prints tracked objects list

    Parameters
    ----------
    trackList : dictionary
        Tracked object list data.
        Format :
        {'dataType' : 'CL',
         'frameNum' : N,
         'timeStamp': [timeSec, timeUsec]
         'data'     : [{trackedObject1}, {trackedObject2}, etc...]
         }
    
    NOTE : Distance is in meters and velocity is in km/h
    
    Returns
    -------
    None.

    """
    print(trackList)


def onTriggerCallback(trigger):
    """
    This method prints trigger data

    Parameters
    ----------
    trackList : dictionary
        Trigger data.
        Format :
        {'dataType' : 'TRIGGER',
         'data'     : {trigger data}
         }
    
    NOTE : Distance is in meters and velocity is in km/h
    
    Returns
    -------
    None.

    """
    channel_layer = get_channel_layer()

    vel_x = trigger['data']['vel_x']
    vel_y = trigger['data']['vel_y']
    time = trigger['data']['timeSeconds']
    lane_number = trigger['data']['laneNumber']

    # Calculate speed
    speed = math.sqrt(vel_x ** 2 + vel_y ** 2)

    SpeedRecord.objects.create(speed=speed, lane_number=lane_number, time=time)

    # Broadcast message to channel group
    async_to_sync(channel_layer.group_send)(
        "radar",
        {
            "type": "chat_message",
            "message": {
                'speed': speed,
                'time': datetime.datetime.fromtimestamp(time).strftime('%H:%M:%S'),
                'laneNumber': lane_number
            }
        }
    )


def onErrorCallback(error):
    """
    This method will be called when any error occured while receiving data 
    from radar

    Parameters
    ----------
    error : Str
        Error description.

    Returns
    -------
    None.

    """
    print(error)
