import cv2 as cv
import urllib.request
import numpy as np

url = "https://i.pinimg.com/736x/33/e4/8a/33e48a7df0f3e60e56db6c6071f44eb2.jpg"
resp = urllib.request.urlopen(url)
image = np.asarray(bytearray(resp.read()), dtype=np.uint8)
img = cv.imdecode(image, cv.IMREAD_COLOR)
cv.imshow('Image', img)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('Gray', gray)

# Simple Threholding
threshold, thresh = cv.threshold(gray, 150, 255, cv.THRESH_BINARY)
cv.imshow('Threshold', thresh)
threshold, thresh_inv = cv.threshold(gray, 150, 255, cv.THRESH_BINARY_INV)
cv.imshow('Threshold Inverse', thresh_inv)

# Adaptive Thresholding
adaptive_threshold = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 11, 3)
cv.imshow('Adaptive Threshold', adaptive_threshold)
cv.waitKey(0)