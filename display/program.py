import socket

from radar.models import Display


def send_data_to_ip_port(lane_number, data):
    display = Display.objects.filter(lane_number=lane_number).first()
    if display:
        # Create a socket object
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Connect to the IP address and port
            s.connect((display.ip, display.port))
            # Send the data
            s.sendall("|C|0-0|128-128|\r\n".encode())
            s.sendall(data.encode())

# # Example usage:
# ip = '192.168.40.219'
# port = 4001
# data = "|T|10-70|SLOW DOWN|5|1|1|0|\r\n"
# send_data_to_ip_port(ip, port, data)
# "|T|0-0|100|8|2|1|0|\r\n"