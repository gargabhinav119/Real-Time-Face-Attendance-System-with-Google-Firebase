import cv2
import face_recognition
import pickle
import os
import numpy as np
import cvzone
import firebase_admin
from datetime import datetime

from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage


cred = credentials.Certificate("ServiceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://faceattendancerealtime-a21fd-default-rtdb.firebaseio.com/",
    'storageBucket':"faceattendancerealtime-a21fd.appspot.com"
}
)

bucket = storage.bucket()

cap = cv2. VideoCapture(0)
cap.set(3, 640)#width
cap.set(4, 480)#height

imgBackGround = cv2.imread('Resources/finalbackground.png')

#importing the modes image into list
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath,path)))
# print(modePathList)
# print(len(imgModeList))

# Load the encoding file
print("Loading Encode File...........:")
file = open('EncodeFile.p','rb')
encodeListKnownwithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownwithIds
# print (studentIds)
print("......Encode File Loaded.")

modeType = 0
id = 0
counter = 0
imgStudent = []

while True:
    success, img = cap.read()

    # starting point of heigh:last point of height
    imgBackGround[162:162 + 480, 54:54 + 640] = img
    imgBackGround[0 + 0:0 + 0 + 720, 0 + 778:0 + 778 + 1280] = imgModeList[modeType]


    # resize the captured image to match the size of the region we want to replace in the background image
    # img = cv2.resize(img,(309,289))
    # x,y
    imgS = cv2.resize(img, (0, 0), None, (0.25), (0.25))
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)


    faceCurrFrame = face_recognition.face_locations(imgS)
    encodeCurrFrame = face_recognition.face_encodings(imgS, faceCurrFrame)
    # we don't want to find the encoding of the whole image,we want to find
    # encoding of the face present in the image ,so we are giving the location
    # of face present in the face

    if faceCurrFrame:
        for encodeFace, faceLoc in zip(encodeCurrFrame, faceCurrFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print("matches",matches)
            # print("faceDis",faceDis)
            matchIndex = np.argmin(faceDis)
            # get the name of the person
            name = studentIds[matchIndex]
            # draw the name on the output image
            if matches[matchIndex]:
                # print("This is ", studentIds[matchIndex])
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
                bbox = 64+x1,167+y1,x2-x1,y2-y1
                imgBackGround = cvzone.cornerRect(imgBackGround,bbox,rt=0)
                id = studentIds[matchIndex]
                if counter == 0:
                    cvzone.putTextRect(imgBackGround,"Loading",(300,300))
                    cv2.imshow("Face Attendance", imgBackGround)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1


        if counter != 0:
            if counter == 1:

                #Get the data
                StudentInfo = db.reference(f'Students/{id}').get()
                print(StudentInfo)

                #get the image from the storage
                blob = bucket.get_blob(f'Images/{id}.png')
                array = np.frombuffer(blob.download_as_string(),np.uint8)
                imgStudent = cv2.imdecode(array,cv2.COLOR_BGRA2BGR)

                #update data of attendance
                datetimeObject = datetime.strptime(StudentInfo['last Attendance time'],"%Y-%m-%d %H:%M:%S")

                secondsElapsed = (datetime.now()-datetimeObject).total_seconds()
                print(secondsElapsed)
                if secondsElapsed>30:
                    ref = db.reference(f'Students/{id}')
                    StudentInfo['total attendance'] +=1
                    ref.child('total attendance').set(StudentInfo['total attendance'])
                    ref.child('last Attendance time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modeType = 3
                    counter = 0

            if modeType!=3:

                if 10<counter<20:
                    modeType = 2
                imgBackGround[0 + 0:0 + 0 + 720, 0 + 778:0 + 778 + 1280] = imgModeList[modeType]

                if counter<10:
                    cv2.putText(imgBackGround,str(StudentInfo['total attendance']),(861,75),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                    cv2.putText(imgBackGround,str(StudentInfo['name']),(918,468),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                    cv2.putText(imgBackGround,str(StudentInfo['age']),(1008,564),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                    cv2.putText(imgBackGround,str(StudentInfo['occupation']),(955,656),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                    imgBackGround[135:135+250,909:909+250] = imgStudent

                counter = counter + 1

                if counter>=20:
                    counter = 0
                    modeType = 0
                    StudentInfo = []
                    imgStudent = []
                    imgBackGround[0 + 0:0 + 0 + 720, 0 + 778:0 + 778 + 1280] = imgModeList[modeType]

    else:
        modeType = 0
        counter = 0

    # resize = cv2.resize(imgBackGround, (640, 480))


    cv2.imshow("Face Attendance", imgBackGround)
    if cv2.waitKey(1) == ord('q'):
        break