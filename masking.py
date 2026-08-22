import cv2 as cv
import numpy as np

img = cv.imread(r'Photos\frieren.jpg')
cv.imshow('Frieren', img)

blank = np.zeros(img.shape[:2], dtype='uint8')

circle = cv.circle(blank.copy(), (img.shape[1]//2, img.shape[0]//2), 200, 255, -1)
cv.imshow('Cicle', circle)
rectangle = cv.rectangle(blank.copy(), (30,30), (370,370), 255, -1)
cv.imshow('Rectangle', rectangle)

weird_shape = cv.bitwise_and(circle, rectangle)
cv.imshow('Weird Shape', weird_shape)

masked = cv.bitwise_and(img,img,mask=weird_shape)
cv.imshow('Masked Image', masked)

cv.waitKey(0)