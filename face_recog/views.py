import cv2
import csv
import numpy as np
import json
import pandas as pd
import face_recognition
from django.views.decorators.csrf import csrf_exempt
import os
from datetime import datetime
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as authLogin
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.messages import get_messages
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse
from .models import student
from numpy import asarray
#from face_recog import attendence_system

def home(request):
    return render(request,"n.html",{'context':""})

def show(request):
    df = pd.read_csv("static/attendence.csv")
    #'tableview/static/csv/20_Startups.csv' is the django 
    # directory where csv file exist.
    # Manipulate DataFrame using to_html() function
    json_records = df.reset_index().to_json(orient ='records')
    data = []
    data = json.loads(json_records)
    context = {'d': data}
  
    return render(request, 'show.html', context)

def mark(request):
    path = 'media'
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
        with open('static/attendence.csv','r+') as f:
            mydatalist = f.readlines()
            namelist = []
            now = datetime.now()
            dtdate = now.strftime('%d:%m:%Y')
            for line in mydatalist:
                entry = line.split(',')
                print(entry[1])
                #print(entry[0])
                if entry[1] is dtdate:
                    namelist.append(entry[0])

            if name not in namelist:
                now = datetime.now()
                dtdate = now.strftime('%d:%m:%Y')
                dtstring = now.strftime('%H:%M:%S')  
                f.writelines(f'\n{name},{dtstring},{dtdate}')  
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
        cv2.setWindowProperty("Webcam", cv2.WND_PROP_TOPMOST, 1)
        cv2.waitKey(4000)
        cv2.destroyAllWindows()
        return render(request,"index.html",{'context':"Done"})

def display_all(request):
    students = student.objects.all()
    return render(request,"display.html",{'students':students})   

def play(request,id):
    students=student.objects.filter(id=id)
    for object in students:
        name = object.name
    print(name.upper())    
    with open('static/attendence.csv','r+') as f:
            mydatalist = f.readlines()
            datelist = []
            timelist = []
            #print(mydatalist)
            print(name.upper())
            for line in mydatalist:
                entry = line.split(',')
                print(entry[1])
                if entry[0] == name.upper():
                    datelist.append(entry[2])
                    timelist.append(entry[1])
    print(datelist)                

    return render(request,"play.html",{'datelist':datelist,'timelist':timelist})         