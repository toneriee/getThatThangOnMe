import cv2 as cv
import numpy as np

# Read image
path = r'Photos\BGR.jpg'
color_img = cv.imread(path)
HSV_img = cv.cvtColor(color_img, cv.COLOR_BGR2HSV)

# create threshold for blue objects
lower_red1 = np.array([0,60,2],dtype='uint8')
upper_red1 = np.array([15,255,255],dtype='uint8')
lower_red2 = np.array([170,120,70], dtype='uint8')
upper_red2 = np.array([179,255,255],dtype='uint8')


# keep the color wanted (white dots) and remove the rest (black dots)
mask1 = cv.inRange(HSV_img,lower_red1, upper_red1)
mask2 = cv.inRange(HSV_img,lower_red2, upper_red2)
red_mask = mask1 + mask2
cv.imshow('Blue mask', red_mask)
# for only blue object existing
blue_detector = cv.bitwise_and(color_img,color_img,mask = red_mask)
cv.imshow('Blue detector', blue_detector)
# Circle the blue object
contours, hierachy = cv.findContours(red_mask,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)

for pic,contour in enumerate(contours):
    area = cv.contourArea(contour)
    if area > 100:
        x, y, w, h = cv.boundingRect(contour)
        cv.rectangle(color_img,(x,y),(x+w,y+h),(255,0,0),1)
cv.imshow('Red_detector',color_img)

cv.waitKey(0)