import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

path = 'static/images'
images = []
classnames = []
mylist = os.listdir(path)

print(mylist)

for cl in mylist:
    curimg = cv2.imread(f'{path}/{cl}')
    images.append(curimg)
    classnames.append(os.path.splitext(cl)[0])

print(classnames)    

def find_encodings(images):
    encodelist = []
    for img in images:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodelist.append(encode)
    return encodelist

def mark_attendence(name):
    with open('attendence.csv','r+') as f:
        mydatalist = f.readlines()
        namelist = []
        for line in mydatalist:
            entry = line.split(',')
            namelist.append(entry[0])
        if name not in namelist:
            now = datetime.now()
            dtstring = now.strftime('%H:%M:%S')  
            f.writelines(f'\n{name},{dtstring}')  
        print(mydatalist)

#mark_attendence('Obama')

encodelistknown = find_encodings(images)
print('encoding complete')

cap = cv2.VideoCapture(0)

while True:
    success , img = cap.read()
    imgs = cv2.resize(img,(0,0),None,0.25,0.25)
    imgs = cv2.cvtColor(imgs,cv2.COLOR_BGR2RGB)
    
    facescurframe = face_recognition.face_locations(imgs)
    encodescurframe = face_recognition.face_encodings(imgs,facescurframe)

    for encodeFace,faceloc in zip(encodescurframe,facescurframe):
        matches = face_recognition.compare_faces(encodelistknown,encodeFace)
        face_dis = face_recognition.face_distance(encodelistknown,encodeFace)
        print(face_dis)
        matchIndex = np.argmin(face_dis)

        if matches[matchIndex]:
            name = classnames[matchIndex].upper()
            print(name)
            y1,x2,y2,x1 = faceloc
            y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            mark_attendence(name)

    cv2.imshow('Webcam',img)
    cv2.waitKey(1)

