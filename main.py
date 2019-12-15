import requests
import json
#import check_cam as cc
import numpy as np
import cv2
def get_cam(username,c):
    time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    cap = cv2.VideoCapture(0)
    face_detector = cv2.CascadeClassifier('Desktop/haarcascade_frontalface_default.xml')
    #face_id = input('\n enter user id end press <return> ==>  ')
    print("\n [INFO] Initializing face capture. Look the camera and wait ...")
    cap.set(3,640) # set Width
    cap.set(4,480) # set Height
    count=0
    while(True):
        ret, img = cap.read()

        #img = cv2.flip(img, -1) # flip video image vertically
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)
            count += 1
            # Save the captured image into the datasets folder
            c.execute("INSERT INTO RfidImages (UserName,TimeStamp,Photo) VALUES(?,?,%s)",(username,time,img,))
            cv2.imwrite("Desktop//dataset/" + str(username) + '.' + str(count) + ".jpg", img)
            cv2.imshow('image', img)
        k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
        if k == 27:
            break
        elif count >= 5: # Take 30 face sample and stop video
             break
    cap.release()
    cv2.destroyAllWindows()
send_url = 'http://api.ipstack.com/50.204.41.130?access_key=????????????????'
r = requests.get(send_url)
j = json.loads(r.text)
lat = j['latitude']
lon = j['longitude']
import pyodbc
from datetime import datetime, timedelta
update_data = """ UPDATE RfidTimestamps SET EndTime=?, isEntry=? WHERE (RfidCode,isEntry)=(?,?);"""
check_entry_data = """ SELECT * FROM RfidTimestamps WHERE (RfidCode,Date,IsEntry)=(?,?,?); """
insert_data = """ INSERT INTO RfidTimestamps ( RfidCode, Date, StartTime, IsEntry,UserName) VALUES ( ?,?,?,?,? );"""
#user_name=("SELECT UserName FROM RfidUsers WHERE RfidCode=?", (rfidcode,))
def create_table_connection():
    server='xx.xx.com'
    database= 'xxxx'
    username = 'xxx'
    password = 'xxxxxx'
    #print(pyodbc.drivers())
	#conn = pyodbc.connect('DRIVER{freetds};Server=Server2;DATABASE=Test1;UID=user;PWD=pass;')
    conn = pyodbc.connect('DRIVER={freetds};PORT=1433;TDS_Version=7.2;SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    try:
        c = conn.cursor()
        print("Connected")
        return conn
    except Error as e:
        print(e)
    #c.execute("SELECT * from UmasUsers where DisplayName='Hitanshu Rami' OR DisplayName='Prashant Kumar'")
    #row = c.fetchone()
    #while row:
    #    print(row)
    #    row = c.fetchone()

def data_entry(conn, rfidcode):

    date = datetime.now().strftime("%m/%d/%Y 00:00:00")
    time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    #is_teacher = validate_rfidcode(rfidcode)
    c = conn.cursor()
    username=c.execute("SELECT UserName FROM RfidUsers WHERE RfidCode=?", (rfidcode,))
    user_name=username.fetchone()
    print(user_name[0])
    name=user_name[0].partition("@")[0][:-1]


    #print(user_name)
    c.execute(" SELECT * FROM RfidTimestamps WHERE RfidCode=? AND IsEntry=? AND DATE=?", (rfidcode,True,date))
    row = c.fetchall()
    if row:
        #c.execute("UPDATE DB_128266_adsdb.dbo.RfidTimestamps SET UserName='Hitanshu' WHERE RfidCode=0009636712")

        c.execute(""" UPDATE RfidTimestamps SET EndTime=?, IsEntry=? WHERE RfidCode=? AND isEntry=? AND DATE=?;""", (time, False, rfidcode, True,date))
        conn.commit()
        name=name+"out"
        get_cam(name,c)
        print("Out Time recorded for ",username[0])
    else:
        c.execute(""" INSERT INTO RfidTimestamps ( RfidCode, Date, StartTime, IsEntry,UserName,Longitude,Latitude,Location) VALUES ( ?,?,?,?,?,?,?,? );""", (rfidcode, date, time, True, user_name[0],lat,lon,"Corporate"))
        print("In Time recorded for ",username[0])
        name=name+"in"
        get_cam(name,c)
        conn.commit()
def main():
    c = create_table_connection()
    rfidcode = ""
    while rfidcode is not "q":
        rfidcode = input("Scan the  ID:")

            data_entry(c, rfidcode)

if __name__ == "__main__":
    main()
