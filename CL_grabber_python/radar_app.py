import datetime
import math
import requests

from capture.image import save_image
from display.program import send_data_to_ip_port
from msmsql_connector import insert_record
from radar.loggers import app_logger
from radar.models import SpeedLimit, SpeedRecord, TriggerPoint, ConfiguredConnection, Location, CounterModel


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
    # print(trackList)
    pass


def generate_transaction_id(address):
    instance = CounterModel.get_instance()
    count = instance.get_count()
    date_str = datetime.datetime.now().strftime("%Y%m%d")
    return f"{address}{date_str}{count}"


def save_to_db(speed, lane_number, frame_number, time, speed_limit):
    location_obj = Location.objects.first()
    if location_obj:
        address = location_obj.address
    else:
        address = "location"

    instance = SpeedRecord.objects.create(speed=speed, lane_number=lane_number,
                                          frame_number=frame_number,
                                          time=datetime.datetime.fromtimestamp(time),
                                          location=address,
                                          transcation_id=generate_transaction_id(address))
    
    image_name = save_image(instance)

    insert_record(instance.id, instance.transcation_id, speed, datetime.datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S'), lane_number, image_name.split("images/")[-1], address)
    
    app_logger.info(f"{instance.transcation_id}, {speed}, {lane_number}, {frame_number}, {datetime.datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')}, {address}")

    # if speed >= speed_limit:
    #     save_image(instance)

    try:
        requests.post("http://127.0.0.1:8000/radar-update/", json={"instance_id": instance.id})
    except Exception as e:
        print(e)
        print("Make sure the server is running!")


def display_on_screen(speed, speed_limit, lane_number):
    speed_digits = len(str(speed))
    if speed_digits == 1:
        speed_digits_str = "44-0"
    elif speed_digits == 2:
        speed_digits_str = "22-0"
    else:
        speed_digits_str = "0-0"

    if speed >= speed_limit:
        send_data_to_ip_port(lane_number, f"|T|{speed_digits_str}|{speed}|8|1|1|0|\r\n", speed, True)
    elif speed >= (speed_limit * 0.9):
        send_data_to_ip_port(lane_number, f"|T|{speed_digits_str}|{speed}|8|4|1|0|\r\n", speed)
    else:
        send_data_to_ip_port(lane_number, f"|T|{speed_digits_str}|{speed}|8|4|1|0|\r\n", speed)


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
    # print(trigger)
    configured_connection_obj = ConfiguredConnection.objects.first()
    if configured_connection_obj:
        if not configured_connection_obj.status:
            return
    else:
        return

    vel_x = trigger['data']['vel_x']
    vel_y = trigger['data']['vel_y']
    lane_number = trigger['data']['laneNumber']
    trigger_point = trigger['data']['x']

    # Calculate speed
    speed = int(math.sqrt(vel_x ** 2 + vel_y ** 2))

    speed_limit_obj = SpeedLimit.objects.first()

    if speed_limit_obj:
        speed_limit = speed_limit_obj.limit
    else:
        speed_limit = 80

    trigger_point_obj = TriggerPoint.objects.first()
    if trigger_point_obj:
        display_trigger = trigger_point_obj.display or 70
        camera_trigger = trigger_point_obj.camera or 30
    else:
        display_trigger = 70
        camera_trigger = 30

    if trigger_point <= display_trigger + 5 and trigger_point >= display_trigger - 5:
        display_on_screen(speed, speed_limit, lane_number)
    elif trigger_point <= camera_trigger + 5 and trigger_point >= camera_trigger - 5:
        time = trigger['data']['timeSeconds']
        frame_number = trigger['data']['frameNumber']
        save_to_db(speed, lane_number, frame_number, time, speed_limit)


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
