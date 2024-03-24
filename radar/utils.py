from radar.models import Display, SpeedLimit, Radar, TriggerPoint, ConfiguredConnection, Location


def save_configurations(data):
    if data.get("connect-status") == "Connect":
        # SAVE DISPLAY CONFIG
        ip0 = data.get('ip0')
        port0 = int(data.get('port0', 0)) if data.get('port0') else None
        camera_ip0 = data.get('cameraip0', '') if data.get('cameraip0') else None
        camera_username0 = data.get('camerausername0', '') if data.get('camerausername0') else None
        camera_password0 = data.get('camerapass0', '') if data.get('camerapass0') else None
        lane_number0 = 0

        ip1 = data.get('ip1')
        port1 = int(data.get('port1', 0)) if data.get('port1') else None
        camera_ip1 = data.get('cameraip1', '') if data.get('cameraip1') else None
        camera_username1 = data.get('camerausername1', '') if data.get('camerausername1') else None
        camera_password1 = data.get('camerapass1', '') if data.get('camerapass1') else None
        lane_number1 = 1

        ip2 = data.get('ip2')
        port2 = int(data.get('port2', 0)) if data.get('port2') else None
        camera_ip2 = data.get('cameraip2', '') if data.get('cameraip2') else None
        camera_username2 = data.get('camerausername2', '') if data.get('camerausername2') else None
        camera_password2 = data.get('camerapass2', '') if data.get('camerapass2') else None
        lane_number2 = 2

        ip3 = data.get('ip3')
        port3 = int(data.get('port3', 0)) if data.get('port3') else None
        camera_ip3 = data.get('cameraip3', '') if data.get('cameraip3') else None
        camera_username3 = data.get('camerausername3', '') if data.get('camerausername3') else None
        camera_password3 = data.get('camerapass3', '') if data.get('camerapass3') else None
        lane_number3 = 3

        # Save or update Display objects
        Display.objects.update_or_create(lane_number=lane_number0, defaults={'ip': ip0, 'port': port0, 'camera_ip': camera_ip0, 'camera_user': camera_username0, 'camera_pass': camera_password0})
        Display.objects.update_or_create(lane_number=lane_number1, defaults={'ip': ip1, 'port': port1, 'camera_ip': camera_ip1, 'camera_user': camera_username1, 'camera_pass': camera_password1})
        Display.objects.update_or_create(lane_number=lane_number2, defaults={'ip': ip2, 'port': port2, 'camera_ip': camera_ip2, 'camera_user': camera_username2, 'camera_pass': camera_password2})
        Display.objects.update_or_create(lane_number=lane_number3, defaults={'ip': ip3, 'port': port3, 'camera_ip': camera_ip3, 'camera_user': camera_username3, 'camera_pass': camera_password3})

        # SAVE SPEED LIMIT
        speed_limit = data.get('speed-limit')
        speed_limit_obj = SpeedLimit.objects.first()
        if speed_limit_obj:
            # Update the speed limit value
            speed_limit_obj.limit = speed_limit
            speed_limit_obj.save()
        else:
            # Create a new SpeedLimit object if none exists
            SpeedLimit.objects.create(limit=speed_limit)

        # SAVE RADAR CONFIG
        ip = data.get('radar_ip')
        host_ip = data.get('host_ip')
        radar_obj = Radar.objects.first()
        if radar_obj:
            # Update the Radar value
            radar_obj.ip = ip
            radar_obj.host_ip = host_ip
            radar_obj.save()
        else:
            # Create a new Radar object if none exists
            Radar.objects.create(ip=ip, host_ip=host_ip)

        # SAVE TRIGGER CONFIG
        display = data.get('display_trigger')
        camera = data.get('camera_trigger')

        # Check if a TriggerPoint record already exists
        trigger_point_obj = TriggerPoint.objects.first()

        if trigger_point_obj:
            # Update the existing TriggerPoint record
            trigger_point_obj.display = display
            trigger_point_obj.camera = camera
            trigger_point_obj.save()
        else:
            # Create a new TriggerPoint object if none exists
            TriggerPoint.objects.create(display=display, camera=camera)

        # LOCATION CONFIG
        address = data.get('address')

        # Check if a TriggerPoint record already exists
        location_obj = Location.objects.first()

        if location_obj:
            # Update the existing TriggerPoint record
            location_obj.address = address
            location_obj.save()
        else:
            # Create a new TriggerPoint object if none exists
            Location.objects.create(address=address)

    if data.get("connect-status") == "Connect":
        status = True
    else:
        status = False
    configured_connection_obj = ConfiguredConnection.objects.first()
    if configured_connection_obj:
        configured_connection_obj.status = status
        configured_connection_obj.save()
    else:
        ConfiguredConnection.objects.create(status=status)
