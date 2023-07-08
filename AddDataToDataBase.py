import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("ServiceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendancerealtime-a21fd-default-rtdb.firebaseio.com/"
                                    }
                             )

ref = db.reference('Students')

data = {

    "2":
        {
            "name": "Sunita Kumari",
            "age": 50,
            "occupation": "teacher",
            "total attendance": 0,
            "last Attendance time": "2022-12-11 00:54:33"
        },

    "3":
        {
            "name": "Akshansh Garg",
            "age": 24,
            "occupation": "Doctor",
            "total attendance": 0,
            "last Attendance time": "2022-12-11 00:54:33"
        },

    "4":
        {
            "name": "Abhinav garg",
            "age": 20,
            "occupation": "Engineer",
            "total attendance": 0,
            "last Attendance time": "2022-12-11 00:54:33"
        },
    "1":
        {
            "name": "Om Prakash",
            "age": 51,
            "occupation": "Teacher",
            "total attendance": 0,
            "last Attendance time": "2022-12-11 00:54:33"
        }

}

for key, value in data.items():
    ref.child(key).set(value)
