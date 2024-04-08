import cv2
import matplotlib.pyplot as plt
import cv2
import easyocr
from IPython.display import Image
import mysql.connector
from mysql.connector import Error
import datetime

connection = mysql.connector.connect(host = 'localhost',database = 'mini' , user = 'root' , password = 'password',auth_plugin='mysql_native_password')


harcascade = "/home/black-devil/Desktop/Car-Number-Plates-Detection-main/model/haarcascade_russian_plate_number.xml"
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
    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite("/home/black-devil/Desktop/Car-Number-Plates-Detection-main/plates/scaned_img_" + str(count) + ".jpg", img_roi)
        cv2.rectangle(img, (0,200), (640,300), (0,255,0), cv2.FILLED)
        cv2.putText(img, "Plate Saved", (150, 265), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255), 2)
        #cv2.imshow("Results",img)
        cv2.waitKey(500)
        reader = easyocr.Reader(['en'])
        image="/home/black-devil/Desktop/Car-Number-Plates-Detection-main/plates/scaned_img_0.jpg"
        output = reader.readtext(str(image))
        print(output[0][1])
        mycursor = connection.cursor()
        mycursor.execute("INSERT INTO numberplate(vechile_number,detected_date,detected_time) VALUES (%s,%s,%s)",(output[0][1],datetime.datetime.now(),datetime.datetime.now().time()))
        connection.commit()