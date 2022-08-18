#import sys
# import os
#import re
import cv2
# from django.shortcuts import redirect
from keras.models import load_model
# from time import sleep
import tensorflow as tf
from keras.preprocessing.image import img_to_array
import cv2
import numpy as np
import pickle
from flask import Flask, request, redirect, render_template, url_for
import statistics as st
from pl import *


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index1.html")
    

@app.route("/add" )
def predict():
    url = request.args.get('url')
    # print(url)
    # print('hello')
    # happy = []
    # energitic = []
    # sad = []
    # calm = []
    add_songs(url)
    with open("add.json", 'r') as f , open('songmodel','rb') as m:
        data = json.load(f)
        pred = pickle.load(m)
        
        json_arr = np.asarray(data)
    #     print(json_arr[0])


    for i in json_arr:
            
        X_new = np.array([[i['energy'],i['valence']]])
        
        prediction = pred.predict(X_new)
#         i['mood'] = ' '.join(prediction) 
        if prediction == 'Happy':
            # happy.append(i)
            with open("static/happy.json" , 'r',encoding='utf-8') as g: 
                mood = json.load(g)
                mood.append(i)
                # print(mood)
            with open("static/happy.json" , 'w') as h:
                json.dump(mood, h, indent = 3)                   
               
        elif prediction == 'Energitic':
            # energitic.append(i)
            with open("static/energitic.json", 'r', encoding='utf-8') as g:
                mood = json.load(g)
                mood.append(i)
                # print(mood)
            with open("static/energitic.json" , 'w') as h:
                json.dump(mood, h, indent = 3)
               
        elif prediction == 'Sad':
            # sad.append(i)
            with open("static/sad.json", 'r', encoding='utf-8') as g:
                mood = json.load(g)
                mood.append(i)
                # print(mood)
            with open("static/sad.json" , 'w') as h:
                json.dump(mood, h, indent = 3)                
               
        else:
            # calm.append(i)
            with open("static/calm.json", 'r', encoding='utf-8') as g:
                mood = json.load(g)
                mood.append(i)
                # print(mood)
            with open("static/calm.json" , 'w') as h:
                json.dump(mood, h, indent = 3) 
            # print(f"{i['name']} by {i['artist']} is {prediction}")
         # if(add_songs(url)):
    return render_template("index1.html",keys="Added Successfully", hide="d-block")    
    
@app.route('/camera', methods = ['GET', 'POST'])
def camera():
    i=0

 
    classifier = tf.keras.models.load_model('Model.h5')
    face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    output=[]
    cap = cv2.VideoCapture(1)
    class_labels = ['Angry','Happy','Neutral','Sad','Surprise']
    while (True):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray,1.3,5)

        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(238,130,238),2)
            roi_gray = gray[y:y+h,x:x+w]
            roi_gray = cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)
    ##    
            if np.sum([roi_gray])!=0:
                roi = roi_gray.astype('float')/255.0
                roi = img_to_array(roi)
                roi = np.expand_dims(roi,axis=0)


                predictions = classifier.predict(roi)[0]
                max_index = predictions.argmax()
                predicted_emotion = class_labels[max_index]
                
                print(predicted_emotion)
                label_position = (x,y)
                cv2.putText(frame,predicted_emotion,label_position,cv2.FONT_HERSHEY_SIMPLEX,2,(144, 154, 255),3)
                    
            else:
                cv2.putText(frame,'No Face Found',(20,60),cv2.FONT_HERSHEY_SIMPLEX,2,(144, 154, 255),3)
                

        cv2.imshow('LIVE', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # print(output)
    cap.release()
    cv2.destroyAllWindows()
    # final_output1 = st.mode(output)
    return redirect(url_for("songs",result = predicted_emotion.capitalize()))


@app.route('/templates/buttons', methods = ['GET','POST'])
def buttons():
    return render_template("buttons.html")

@app.route("/songs/<result>")
def songs(result):

    return render_template("songs"+result+".html")
@app.route('/songs/surprise', methods = ['GET', 'POST'])
def songsSurprise():
    return render_template("songsSurprise.html")

@app.route('/songs/angry', methods = ['GET', 'POST'])
def songsAngry():
    return render_template("songsAngry.html")

@app.route('/songs/sad', methods = ['GET', 'POST'])
def songsSad():
    return render_template("songsSad.html")

@app.route('/songs/happy', methods = ['GET', 'POST'])
def songsHappy():
    return render_template("songsHappy.html")

@app.route('/songs/neutral', methods = ['GET', 'POST'])
def songsNeutral():
    return render_template("songsNeutral.html")

@app.route('/templates/test', methods = ['GET', 'POST'])
def join():
    return render_template("index.html")
    
if __name__ == "__main__":
    app.run(debug=True)
