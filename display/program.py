import socket

def send_data_to_ip_port(ip, port, data):
    # Create a socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Connect to the IP address and port
        s.connect((ip, port))
        # Send the data
        s.sendall(data.encode())

# Example usage:
ip = '192.168.40.219'
port = 4001
data = "|T|10-70|SLOW DOWN|5|1|1|0|\r\n"
send_data_to_ip_port(ip, port, data)
