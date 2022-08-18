import cv2
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


### 2. Capture from video file
video = cv2.VideoCapture(1)
while video.isOpened():
    ## Read video frames and convert to grayscale
    _, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    ### 3. Find areas with faces using Haar cascade classifier
    faces = faceCascade.detectMultiScale(image= gray, scaleFactor= 1.1, minNeighbors= 4)
        # scaleFactor: how much the image size is reduced at each image scale
        # minNeighbors: how many neighbors each candidate rectangle should have to retain it

    # x, y coordinates, w (weight) and h (height) of each "face" rectangle in frame
    for (x, y, w, h) in faces:
        # input, point1, point2, color, thickness=2    
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        # Get the region of interest: face rectangle sub-image in gray and colored
        faceROIGray = gray[y: y+h, x: x+w]
        faceROIColored = frame[y: y+h, x: x+w]
        cv2.putText(frame, 'face detected', (x, y-10),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)
        
        ### 4. Find areas with eyes in faces using Haar cascade classifier
            #### 5. Show the output video
    cv2.imshow('Face Detection - OpenCV', frame)
    if cv2.waitKey(10) == 27: break  # Wait Esc key to end program
