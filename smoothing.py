import cv2 as cv
import numpy as np
import urllib.request

url = "https://i.pinimg.com/1200x/53/a4/90/53a490c2e15847f5f9dbe9ea3b29e654.jpg"
resp = urllib.request.urlopen(url)
image = np.asarray(bytearray(resp.read()), dtype=np.uint8)
img = cv.imdecode(image, cv.IMREAD_COLOR)
cv.imshow('Landscape', img)

# Averaging
average = cv.blur(img, (7,7))
cv.imshow('Average Blur', average)

# Gaussian Blur
gauss = cv.GaussianBlur(img, (7,7), 0)
cv.imshow('Gaussian Blur', gauss)

# Median Blur
median = cv.medianBlur(img, 7)
cv.imshow('Median Blur', median)

# Bilateral
bilateral = cv.bilateralFilter(img, 5, 15, 15)
cv.imshow('Bilateral', bilateral)

cv.waitKey(0)