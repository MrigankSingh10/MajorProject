# import system module
import sys

# import some PyQt5 modules
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer,Qt

# import Opencv module
import cv2
#import PyAutoGui and UI For the app
import numpy as np
import pyautogui
from ui_main_window import *

font = cv2.FONT_HERSHEY_SIMPLEX

yellow_lower = np.array([20, 100, 100])
yellow_upper = np.array([30, 255, 255])
upper_limit=200
lower_limit=300
left_limit=270-50
right_limit=370+25

actions={'space':False,'left':False,'down':False,'right':False,'up':False}

def pressup():
    if actions.get('up')==False:
        pyautogui.press('up')
        actions['up']=True
        print(actions)

def pressdown():
    if actions.get('down')==False:
        pyautogui.press('down')
        actions['down']=True
        print(actions)

def pressspace():
    if actions.get('space')==False:
        pyautogui.press('space')
        actions['space']=True
        print(actions)

def pressright():
    if actions.get('right')==False:
        pyautogui.press('right')
        actions['right']=True
        print(actions)

def pressleft():
    if actions.get('left')==False:
        pyautogui.press('left')
        actions['left']=True
        print(actions)

def Neutral():
    if actions.get('space') or actions.get('up') or actions.get('down') or actions.get('left') or actions.get('right'):
        actions['space']=False
        actions['up']=False
        actions['down']=False
        actions['left']=False
        actions['right']=False
        print(actions)

#App Development
class MainWindow(QWidget):
    # class constructor
    def __init__(self):
        # call QWidget constructor
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # create a timer
        self.timer = QTimer()
        # set timer timeout callback function
        self.timer.timeout.connect(self.viewCam)
        # set control_bt callback clicked  function
        self.ui.control_bt.clicked.connect(self.controlTimer)
        
    # view camera
    def viewCam(self):
        # read image in BGR format
        ret, frame = self.cap.read()
        # convert image to RGB format and put lines to divide regions
        
        frame=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        mask=cv2.inRange(frame,yellow_lower,yellow_upper)
        contours,hierarchy=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        frame = cv2.line(frame,(0,198),(640,198),(255,255,255),4)
        frame = cv2.line(frame,(0,298+45),(640,298+45),(255,255,255),4)
        frame = cv2.line(frame,(218,0),(218,480),(255,255,255),4)
        frame = cv2.line(frame,(368+50,0),(368+50,480),(255,255,255),4)
        cv2.putText(frame,'Space',(50, 50),font, 1,(0, 255, 255),2, cv2.LINE_4)
        cv2.putText(frame,'Up',(250, 50),font, 1,(0, 255, 255),2, cv2.LINE_4)
        cv2.putText(frame,'right',(50, 250),font, 1,(0, 255, 255),2, cv2.LINE_4)
        cv2.putText(frame,'down',(250, 400),font, 1,(0, 255, 255),2, cv2.LINE_4)
        cv2.putText(frame,'left',(450, 250),font, 1,(0, 255, 255),2, cv2.LINE_4)
        for c in contours:
            # So that unneccessary objects are not detected 
            area=cv2.contourArea(c)
            if area>300:
                x,y,w,h=cv2.boundingRect(c)
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,255),2)

                if y<upper_limit and x<left_limit:
                    pressspace()
                elif y<upper_limit and x>left_limit and x<right_limit:
                    pressup()
                elif y>lower_limit and x>left_limit and x<right_limit:
                    pressdown()
                elif y>upper_limit and y<lower_limit and x<left_limit:
                    pressright()
                elif y>upper_limit and y<lower_limit and x>right_limit:
                    pressleft()
                elif y>upper_limit and y<lower_limit and x>left_limit and x<right_limit:
                    Neutral()

        frame=cv2.cvtColor(frame,cv2.COLOR_HSV2BGR)
        # get image infos
        height, width, channel = frame.shape
        step = channel * width
        # create QImage from image
        qImg = QImage(frame.data, width, height, step,QImage.Format_BGR888)
        # show image in img_label
        self.ui.image_label.setPixmap(QPixmap.fromImage(qImg))

    # start/stop timer
    def controlTimer(self):
        # if timer is stopped
        if not self.timer.isActive():
            # create video capture
            self.cap = cv2.VideoCapture(0)
            # start timer
            self.timer.start(20)
            # update control_bt text
            self.ui.control_bt.setText("Stop")
        # if timer is started
        else:
            # stop timer
            self.timer.stop()
            # release video capture
            self.cap.release()
            # update control_bt text
            self.ui.control_bt.setText("Start")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    try:
        # create and show mainWindow
        mainWindow = MainWindow()
        mainWindow.show()
        sys.exit(app.exec_())
    except Exception as e:
        
        print(e)
        sys.exit(1)