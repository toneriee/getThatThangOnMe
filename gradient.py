import cv2 as cv
import urllib.request
import numpy as np

url = "https://i.pinimg.com/1200x/68/c4/24/68c42465f60f9572989142c8cbccbd13.jpg"
resp = urllib.request.urlopen(url)
image = np.asarray(bytearray(resp.read()), dtype=np.uint8)
img = cv.imdecode(image, cv.IMREAD_COLOR)
cv.imshow('Image', img)

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('Gray', gray)

# Laplacian
lap = cv.Laplacian(gray, cv.CV_64F)
lap = np.uint8(np.absolute(lap))
cv.imshow('Laplacian', lap)

# Sobel
sobelx = cv.Sobel(gray, cv.CV_64F, 1, 0)
sobely = cv.Sobel(gray, cv.CV_64F, 0, 1)
combine_sobel = cv.bitwise_or(sobelx, sobely)
cv.imshow('Combine Sobel', combine_sobel)
cv.imshow('Sobel_X', sobelx)
cv.imshow('Sobel_Y', sobely)

canny = cv.Canny(gray, 150, 175)
cv.imshow('Canny', canny)
cv.waitKey(0)