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

from_class = uic.loadUiType("src/UI/ADAS.ui")[0]
        
class ADAS_ui(QDialog, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.start = 0
        self.end = 0
        self.duration = 0
        self.isPowerOn = False
        self.w1, self.h1 = self.Screen1.width(), self.Screen1.height()
        self.pixmap1 = QPixmap(self.w1, self.h1)
        self.DrowseDetectionModel = DrowseDetectionModel()
        self.DrowseDetectionModel.get_state_dict('src/UI/Detection/Drowsy')
        self.FaceDetection = DetectionModel()

        # CAM1 Setting
        self.CAM1 = Camera()
        self.daemon = True
        self.CAM1.update.connect(self.updateCAM1)

        # Arduino Setting
        self.Arduino = Arduino()
        self.Arduino.distance_signal.connect(self.GetDistance)

        self.btnPower.clicked.connect(self.Click_Power)

    def DrowsyDetection(self, frame):
        try:
            x1, y1, x2, y2 = self.FaceDetection(frame)
            
            predict = self.DrowseDetectionModel(frame[y1:y2, x1:x2])

            if predict == 0:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                if self.duration > 2:
                    self.Drowsy.setStyleSheet("background-color: red")
                    self.Screen1.setStyleSheet("border: 5px solid red")
            else:
                self.start = time.time()
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                self.Drowsy.setStyleSheet("background-color: green")
                self.Screen1.setStyleSheet("border: 3px solid green")
        except:
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
            self.Arduino.start()
            self.video1 = cv2.VideoCapture(-1)
        else:
            self.isPowerOn = False
            self.CAM1.stop()
            self.CAM1.isRunning = False
            self.Arduino.stop()
            self.Arduino.quit()
            self.video1.release()
            self.ScreenOFF()


    def GetDistance(self, distance):
        self.Front.setText(distance + 'cm')
        try:
            if eval(distance) < 10:
                self.Front.setStyleSheet("border: 3px solid red")
            elif eval(distance) < 20:
                self.Front.setStyleSheet("border: 3px solid green")
            else:
                self.Front.setStyleSheet("border: 1px solid black")
        except:
            self.Front.setText('No Signal')



    def updateCAM1(self):
        ret, self.frame1 = self.video1.read()
        
        if ret:
            frame = cv2.cvtColor(self.frame1, cv2.COLOR_BGR2RGB)
            frame = cv2.flip(frame, 1)
            self.DrowsyDetection(frame)

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