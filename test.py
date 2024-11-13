import socket
import time
#from pynput import keyboard

esp32_ip = '192.168.2.218'  # ESP32의 IP 주소
esp32_port = 8080  # ESP32에서 설정한 포트

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((esp32_ip, esp32_port))

print('connected')

while True:

    # ESP32에서 받은 데이터 수신
    # client_socket.send('Hello, ESP32!'.encode())
    data = client_socket.recv(1024)
    if not(len(data.decode()) ==37):
        pass
    else:
        print("Received from ESP32:", data.decode())


