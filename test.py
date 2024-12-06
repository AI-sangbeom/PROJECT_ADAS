import os
import time
import timm
import serial
import torch
import torch.nn as nn
import numpy as np
import socket
from torchvision import  transforms
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from huggingface_hub import hf_hub_download
from ultralytics import YOLO
from supervision import Detections
esp32_ip = '192.168.146.119'  # ESP32의 IP 주소
esp32_port = 8080  # ESP32에서 설정한 포트

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # self.client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1) 
    client_socket.connect((esp32_ip, esp32_port))
    # time.sleep(1)  # 시리얼 연결 대기
    print('ESP32 Connected')
except serial.SerialException as e:
    print(f"Could not open  port: {e}")
    print('hello')
    print('hihii')