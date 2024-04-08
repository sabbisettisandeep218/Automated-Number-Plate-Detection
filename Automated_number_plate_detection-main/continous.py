

import datetime

import cv2
import easyocr
import matplotlib.pyplot as plt
#import mysql.connector
from IPython.display import Image
#from mysql.connector import Error

#connection = mysql.connector.connect(host = 'localhost',database = 'mini' , user = 'root' , password = 'password',auth_plugin='mysql_native_password')



harcascade = "C:/Users/hp/OneDrive/Desktop/Automated_number_plate_detection-main/Automated_number_plate_detection-main/model/haarcascade_russian_plate_number.xml"
cap = cv2.VideoCapture(0)


cap.set(3, 640) # width
cap.set(4, 480) #height

min_area = 500
count = 0

while True:
    
    success, img = cap.read()

    plate_cascade = cv2.CascadeClassifier(harcascade)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    plates = plate_cascade.detectMultiScale(img_gray, 1.1, 4)
    for (x,y,w,h) in plates:
        area = w * h

        if area > min_area:
            cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
            cv2.putText(img, "Number Plate", (x,y-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 2)
            img_roi = img[y: y+h, x:x+w]
            cv2.imshow("ROI", img_roi)
        cv2.imshow("Result", img)
        cv2.imwrite("C:/Users/hp/OneDrive/Desktop/Automated_number_plate_detection-main/Automated_number_plate_detection-main/plates/scaned_img_" + str(count) + ".jpg", img_roi)
        cv2.rectangle(img, (0,200), (640,300), (0,255,0), cv2.FILLED)
        cv2.putText(img, "Plate Saved", (150, 265), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255), 2)
        cv2.imshow("Results",img)
        cv2.waitKey(500)
        reader = easyocr.Reader(['en'])
        image="C:/Users/hp/OneDrive/Desktop/Automated_number_plate_detection-main/Automated_number_plate_detection-main/plates/scaned_img_0.jpg"
        output = reader.readtext(str(image))
        if len(output)!=0:
            print(output[0][1])
            #mycursor = connection.cursor()
            #mycursor.execute("INSERT INTO numberplate(vechile_number,detected_date,detected_time) VALUES (%s,%s,%s)",(output[0][1],datetime.datetime.now(),datetime.datetime.now().time()))
            #connection.commit()