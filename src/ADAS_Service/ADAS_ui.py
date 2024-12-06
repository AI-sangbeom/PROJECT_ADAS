import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import sys
import time
import cv2
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from Modules import *

from_class = uic.loadUiType("src/ADAS_Service/ADAS.ui")[0]
        
class ADAS_ui(QDialog, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.start = 0
        self.end = 0
        self.duration = 0
        self.isPowerOn = False
        self.isDrowsy1 = False
        self.isDrowsy2 = False
        self.w1, self.h1 = self.Screen1.width(), self.Screen1.height()
        self.pixmap1 = QPixmap(self.w1, self.h1)
        self.DrowseDetectionModel = DrowseDetectionModel()
        self.DrowseDetectionModel.get_state_dict('src/ADAS_Service/Detection/Drowsy')
        self.FaceDetection = DetectionModel()

        # CAM1 Setting
        self.CAM1 = Camera()
        self.daemon = True
        self.CAM1.update.connect(self.updateCAM1)

        self.msg_list = {'Go': '0', 'Stop': '0', 'Back': '0', 'Drowsy': '0'}

        self.ADAS_CAR = Arduino()
        self.ADAS_CAR.esp32_ip = '192.168.146.119'
        self.ADAS_CAR.distance_signal.connect(self.GetDistance)

        self.btnPower.clicked.connect(self.Click_Power)
        self.btnGo.clicked.connect(self.Click_Go)
        self.btnBack.clicked.connect(self.Click_Back)
        self.btnStop.clicked.connect(self.Click_Stop)

    def Click_Go(self):
        try:
            self.msg_list['Stop'] = '0'
            self.msg_list['Back'] = '0'
            self.msg_list['Go'] = '1'
            self.label_4.setText('Front')
            self.Direction.setText('Go')
            # pass
        except:
            pass
        self.sent_MSG()

    def Click_Back(self):
        try:
            self.msg_list['Stop'] = '0'
            self.msg_list['Go'] = '0'
            self.msg_list['Back'] = '1'
            self.label_4.setText('Back')
            self.Direction.setText('Back')
        except:
            pass
        self.sent_MSG()

    def Click_Stop(self):
        try:
            self.msg_list['Stop'] = '1'
            self.msg_list['Go'] = '0'
            self.msg_list['Back'] = '0'
            self.label_4.setText('Front')
            self.Direction.setText('Stop')
            # pass
        except:
            pass
        self.sent_MSG()

    def DrowsyDetection(self, frame):
        try:
            x1, y1, x2, y2 = self.FaceDetection(frame)
            predict = self.DrowseDetectionModel(frame[y1:y2, x1:x2])

            if predict == 0:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                if self.duration > 2:
                    self.Drowsy.setStyleSheet("background-color: red")
                    self.Screen1.setStyleSheet("border: 5px solid red")
                    self.isDrowsy1 = True
                    self.Direction.setText('Stop')
            else:
                self.start = time.time()
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                self.Drowsy.setStyleSheet("background-color: green")
                self.Screen1.setStyleSheet("border: 3px solid green")
                self.isDrowsy1 = False
        except:
            self.msg_list['Drowsy'] = '0'
            self.start = time.time()
            self.isDrowsy1 = False
            self.Drowsy.setStyleSheet("background-color: white")
            self.Screen1.setStyleSheet("border: 1px solid white")
            
    def ScreenOFF(self):
        self.pixmap1.fill(QColor(0, 0, 0))
        self.Screen1.setPixmap(self.pixmap1)

    def Click_Power(self):
        if not self.isPowerOn:
            self.isPowerOn = True
            self.CAM1.start()
            self.CAM1.isRunning = True
            self.ADAS_CAR.start()
            self.video1 = cv2.VideoCapture(-1)
            self.Direction.setText('Stop')

        else:
            self.isPowerOn = False
            self.CAM1.stop()
            self.CAM1.isRunning = False
            self.ADAS_CAR.stop()
            self.ADAS_CAR.quit()
            self.Direction.setText('')

            self.video1.release()
            self.ScreenOFF()


    def GetDistance(self, distance):
        
        data = distance.split(' ')
        # print(data)
        if data[0] != '\r\n':
            if len(data) == 3:
                distance = data[0].replace('\r\n','') # if '\r\n' not in data[0] else data[:-4]
                infrared_left = data[1].replace('\r\n','')
                infrared_right = data[2].replace('\r\n','')
                # print(distance, infrared_left, infrared_right)
                try:
                    self.Front.setText(distance + 'cm')
                    if infrared_left == 'L0':
                        self.Lane.setText('Left')
                        self.Direction.setText('Right')
                    elif (infrared_right == 'R0'):
                        self.Lane.setText('Right')
                        self.Direction.setText('Left')
                    else:
                        self.Lane.setText('')
                        self.Direction.setText('Go')
      
                except:
                    self.Front.setText('No Signal')
            else:
                distance = data[0].split('\r\n')[0]
                self.Front.setText(distance + 'cm')
                
        

    def distance_alarm(self, distance):
        if self.msg_list['Back'] == '1' and eval(distance) < 10:
            self.msg_list['Stop'] = '1'
            self.msg_list['Go'] = '0'
            self.msg_list['Back'] = '0'
            self.sent_MSG()
            self.Direction.setText('Stop')        


    def sent_MSG(self):
        try:
            msg = ''.join(list(self.msg_list.values())) + '\n'
            self.ADAS_CAR.client_socket.send(msg.encode())
            print(msg)
        except:
            pass

    def send_Drowsy(self):
        
        self.isDrowsy2 = self.isDrowsy1
        if self.isDrowsy1:
            self.msg_list['Drowsy'] = '1'
            self.msg_list['Go'] = '0'
            self.msg_list['Back'] = '0'
            self.msg_list['Stop'] = '1'
        else:
            self.msg_list['Drowsy'] = '0'
        
        self.sent_MSG()

    def updateCAM1(self):
        ret, self.frame1 = self.video1.read()
        
        if ret:
            frame = cv2.cvtColor(self.frame1, cv2.COLOR_BGR2RGB)
            frame = cv2.flip(frame, 1)
            self.DrowsyDetection(frame)
            
            if self.isDrowsy1 != self.isDrowsy2:
                self.send_Drowsy()

            self.end = time.time()
            self.duration = self.end - self.start
                
            h, w, c = frame.shape
            qImg = QImage(frame, w, h, w*c, QImage.Format_RGB888)
            self.pixmap1 = self.pixmap1.fromImage(qImg)
            self.pixmap1 = self.pixmap1.scaled(self.w1, self.h1)
            self.Screen1.setPixmap(self.pixmap1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ADAS_ui()
    window.show()
    app.exec_()

    