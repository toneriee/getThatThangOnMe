import cv2 as cv
import urllib.request
import numpy as np

url = "https://tse3.mm.bing.net/th/id/OIP.98fiH8rz80wgjnBDsGUwyAHaE8?r=0&rs=1&pid=ImgDetMain&o=7&rm=3"
resp = urllib.request.urlopen(url)
image = np.asarray(bytearray(resp.read()), dtype=np.uint8)
img = cv.imdecode(image, cv.IMREAD_COLOR)
cv.imshow('Image', img)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('Gray', gray)
haar_cascade = cv.CascadeClassifier('haar_face.xml')

# #Resize
# resized = cv.resize(gray, (500,500), interpolation=cv.INTER_AREA)
# cv.imshow('Resized', resized)

face_rect = haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3)

print(f'Number of faces found: {len(face_rect)}')


for (x,y,w,h) in face_rect:
    detect = cv.rectangle(img, (x,y), (x+w,y+h), (0,255,0), thickness=1)
cv.imshow('Detected', detect)
cv.waitKey(0)