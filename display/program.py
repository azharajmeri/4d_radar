import time
import socket

from radar.models import Display


def send_data_to_ip_port(lane_number, data, slow_down=False):
    print(lane_number, "KKKKKKKKKKKKKKKKKKKKKKKK", data)
    display = Display.objects.filter(lane_number=lane_number).first()
    print("LLLLLLLLLLLLLLLLLLLLLLL", display)
    if display:
        # Create a socket object
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Connect to the IP address and port
            s.connect((display.ip, display.port))
            time.sleep(0.1)
            # Send the data
            s.sendall(data.encode())

            if slow_down:
                time.sleep(0.1)
                s.sendall("|T|10-70|SLOW DOWN|5|1|1|0|\r\n".encode())

            time.sleep(2)
            s.sendall("|C|0-0|128-128|\r\n".encode())

# # Example usage:
# ip = '192.168.40.219'
# port = 4001
# data = "|T|10-70|SLOW DOWN|5|1|1|0|\r\n"
# send_data_to_ip_port(ip, port, data)
# "|T|0-0|100|8|2|1|0|\r\n"
            
# send_data_to_ip_port(1, "|T|44-0|10|8|4|1|0|\r", True)