import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("ServiceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://faceattendancerealtime-a21fd-default-rtdb.firebaseio.com/",
    'storageBucket':"faceattendancerealtime-a21fd.appspot.com"
}
)

ref = db.reference('Students')


#now we are saving the records of students,Ki wo kaise dikhte hai
#Importing Students images 
folderPath = 'Images'
PathList = os.listdir(folderPath)
imgList = []
StudentIds = []
for path in PathList:
    imgList.append(cv2.imread(os.path.join(folderPath,path)))
    #ab hame .png hatana hai,Sirf id extract krni hai so 
    StudentIds.append(os.path.splitext(path)[0])

    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)



    # print(path)
    # print(os.path.splitext(path)[0])

# print(StudentIds)

def findEncodings(imageList):
    encodeList = []
    for img in imageList:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList


print("Encoding Start:  ")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown,StudentIds]
print("Encoding end:  ")

print(encodeListKnownWithIds[1])


file = open("EncodeFile.p",'wb')
pickle.dump(encodeListKnownWithIds,file)
file.close()
print("FIle SAVED ")

#  encode = face_recognition.face_encodings(img)[0]

# explain this line
# face_encodings() is a function of the face_recognition module that returns a list of 128-dimensional facial feature vectors (also known as encodings) for each face detected in an image.

# In this line of code, the img variable, which contains a single image from the imageList, is passed as an argument to the face_encodings() function to generate its encoding. The [0] index is used to retrieve the first (and only) encoding in the list, as we are assuming that each image in the list contains only one face.

# The resulting encoding is then stored in the encode variable and appended to the encodeList, which is a list of all the encodings generated for all the images in the imageList. Finally, the encodeList containing all the encodings is returned by the function.






# This code performs the following steps to perform face recognition:

# Import the required libraries: The code starts by importing the required libraries,
#  including OpenCV (cv2), face_recognition, pickle, and os.

# Load the student images: The code defines a folder path folderPath where 
# the student images are stored. It uses the os.listdir() function to get a 
# list of all the images in the folder. The path of each image is stored in the list PathList.

# Create a list of images and corresponding student IDs: The code creates two lists, imgList and StudentIds, to store the images and corresponding student IDs respectively. It uses a for loop to iterate over the PathList and add each image to the imgList using the cv2.imread() function. It also extracts the student IDs from the file names by using the os.path.splitext() function to split the file name into two parts and taking the first part, which is the student ID.

# Extract facial encodings from the images: The code defines a function findEncodings() that takes a list of images as input and returns a list of facial encodings. The function uses a for loop to iterate over the list of images and extract the facial encodings for each image using the face_recognition.face_encodings() function. The facial encodings are appended to the encodeList list.

# Store the encodings and student IDs: The code creates a list encodeListKnownWithIds that stores the facial encodings and corresponding student IDs. It opens a pickle file named "EncodeFile.p" using the open() function and the 'wb' (write binary) mode. The list of encodings and student IDs is then saved to the pickle file using the pickle.dump() function. The file is then closed using the file.close() function.

# In summary, this code takes a folder of student images as input, extracts facial encodings from each image using the face_recognition library, and stores the encodings and corresponding student IDs in a pickle file for later use.



