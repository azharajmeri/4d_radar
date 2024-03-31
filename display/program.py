import threading
import time
import socket

from radar.models import Display

timer0 = None
timer1 = None
timer2 = None
timer3 = None

def clear_function(lane_number):
    display = Display.objects.filter(lane_number=lane_number).first()
    if display:
        # Create a socket object
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Connect to the IP address and port
            s.connect((display.ip, display.port))
            time.sleep(0.1)
            # Send the data
            s.sendall("|C|0-0|128-128|\r\n".encode())


def schedule_clear(lane_number, delay):
    global timer0, timer1, timer2, timer3

    if lane_number == 0:
        if timer0:
            timer0.cancel()

        timer0 = threading.Timer(delay, clear_function, args=[0])
        timer0.start()

    if lane_number == 1:
        if timer1:
            timer1.cancel()

        timer1 = threading.Timer(delay, clear_function, args=[1])
        timer1.start()

    if lane_number == 2:
        if timer2:
            timer2.cancel()

        timer2 = threading.Timer(delay, clear_function, args=[2])
        timer2.start()

    if lane_number == 3:
        if timer3:
            timer3.cancel()

        timer3 = threading.Timer(delay, clear_function, args=[3])
        timer3.start()


def send_data_to_ip_port(lane_number, data, speed, slow_down=False):
    display = Display.objects.filter(lane_number=lane_number).first()
    if display:
        # Create a socket object
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Connect to the IP address and port
            s.connect((display.ip, display.port))
            # Send the data
            time.sleep(0.1)
            s.sendall("|C|0-0|128-128|\r\n".encode())

            time.sleep(0.1)
            s.sendall(data.encode())

            if slow_down:
                time.sleep(0.1)
                s.sendall("|T|10-70|SLOW DOWN|5|1|1|0|\r\n".encode())

        if speed <= 40:
            delay = 4
        elif speed <= 80:
            delay = 3
        else:
            delay = 2

        schedule_clear(lane_number, delay)

# # Example usage:
# ip = '192.168.40.219'
# port = 4001
# data = "|T|10-70|SLOW DOWN|5|1|1|0|\r\n"
# send_data_to_ip_port(ip, port, data)
# "|T|0-0|100|8|2|1|0|\r\n"
# send_data_to_ip_port(1, "|T|44-0|10|8|4|1|0|\r", True)
