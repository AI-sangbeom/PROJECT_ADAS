import socket
import time
#from pynput import keyboard

esp32_ip = '192.168.2.218'  # ESP32의 IP 주소
esp32_port = 8080  # ESP32에서 설정한 포트

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((esp32_ip, esp32_port))

cnt = 0

# 데이터 전송
# while (cnt < 10):
    # esp32 로 데이터 송신
while True:
    # text = input("Input : ")
    # if text == 'q':
    #     break
    client_socket.send("Hello from Python".encode())

    time.sleep(0.1)
    # ESP32에서 받은 데이터 수신
    data = client_socket.recv(1024)
    print("Received from ESP32:", data.decode())

    time.sleep(0.1)


client_socket.close()
print('Client 종료')