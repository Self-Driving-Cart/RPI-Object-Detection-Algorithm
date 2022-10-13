import numpy as np
import cv2
import RPi.GPIO as GPIO
import time
import serial

ser = serial.Serial(

        port='/dev/ttyAMA1',

        baudrate=115200,

        parity=serial.PARITY_NONE,

        stopbits=serial.STOPBITS_ONE,

        bytesize=serial.EIGHTBITS,

        timeout=1

        )

GPIO.setmode(GPIO.BCM)

pin1 = 23
pin2 = 24
EN1 = 25
y = 0


GPIO.setup(pin1, GPIO.OUT)
GPIO.setup(pin2, GPIO.OUT)
GPIO.setup(EN1, GPIO.OUT)

pwm1 = GPIO.PWM(EN1, 100)

pwm1.start(1)

# Cascades 디렉토리의 haarcascade_frontalface_default.xml 파일을 Classifier로 사용

faceCascade = cv2.CascadeClassifier('/home/kingjw/fullbody/haarcascade_fullbody.xml')

cap = cv2.VideoCapture(0)

cap.set(3,640) # set Width

cap.set(4,480) # set Height

while True:

    ret, img = cap.read()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(

        gray,

        scaleFactor=1.1,

        minNeighbors=-1,

        minSize=(70, 250)
    )

    for (x,y,w,h) in faces:

        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

        roi_gray = gray[y:y+h, x:x+w]

        roi_color = img[y:y+h, x:x+w]

        data1='1'

        data2='2'

        data3='3'

        if x<250:

             ser.write(str(data1).encode())

        elif x>380:

             ser.write(str(data2).encode())

        else :

             ser.write(str(data3).encode())

    cv2.imshow('video',img) # video라는 이름으로 출력

    k = cv2.waitKey(30) & 0xff


    if k == 27: # press 'ESC' to quit # ESC를 누르면 종료


        break

cap.release()

cv2.destroyAllWindows()
