
import socket
import sys

def check_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

if __name__ == "__main__":
    is_up = check_port(8000)
    with open('/home/sairam_achanta/Documents/Doorstep_mobile_services/backend/port_check.txt', 'w') as f:
        f.write(f"Port 8000 UP: {is_up}\n")
    print(f"Port 8000 UP: {is_up}")
