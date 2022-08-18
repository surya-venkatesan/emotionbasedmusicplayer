import json
import pickle
import numpy as np
from sklearn import datasets
from pl import *
# happy = []
# energitic = []
# sad = []
# calm = []
play = input(print("Enter: "))
add_songs(play)
with open("add.json", 'r') as s , open('songmodel','rb') as m:
    data = json.load(s)
    pred = pickle.load(m)
    
    json_arr = np.asarray(data)
#     print(json_arr[0])


for i in json_arr:
        
        X_new = np.array([[i['energy'],i['valence']]])
        
        prediction = pred.predict(X_new)
#         i['mood'] = ' '.join(prediction) 
        
        if prediction == 'Happy':
            # happy.append(i)
                with open("happy.json" , 'r',encoding='utf-8') as g: 
                    mood = json.load(g)
                    mood.append(i)
                    print(mood)
                with open("happy.json" , 'w') as h:
                    json.dump(mood, h, indent = 3)                   
               
        elif prediction == 'Energitic':
            # energitic.append(i)
                with open("energy.json", 'r', encoding='utf-8') as g:
                    mood = json.load(g)
                    mood.append(i)
                    print(mood)
                with open("energy.json" , 'w') as h:
                    json.dump(mood, h, indent = 3)
               
        elif prediction == 'Sad':
            # sad.append(i)
                with open("sad.json", 'r', encoding='utf-8') as g:
                    mood = json.load(g)
                    mood.append(i)
                    print(mood)
                with open("sad.json" , 'w') as h:
                    json.dump(mood, h, indent = 3)                
               
        else:
            # calm.append(i)
                with open("calm.json", 'r', encoding='utf-8') as g:
                    mood = json.load(g)
                    mood.append(i)
                    print(mood)
                with open("calm.json" , 'w') as h:
                    json.dump(mood, h, indent = 3)                
               
        # print(f"{i['name']} by {i['artist']} is {prediction}")
