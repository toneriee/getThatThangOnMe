import cv2 as cv
import matplotlib.pyplot as plt

img = cv.imread(r'Photos\gogogo.png')
cv.imshow('Gojo', img)
# plt.imshow(img)
# plt.show()
# BGR to Grayscale
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('Gray', gray)

# BGR to HSV
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
cv.imshow('HSV', hsv)

# BGR to L*a*b
lab = cv.cvtColor(img, cv.COLOR_BGR2LAB)
cv.imshow('LAB', lab)

# BGR to RGB
rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
cv.imshow('RGB', rgb)

# HSV to BGR
hsv2bgr = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
cv.imshow('HSV2BGR', hsv2bgr)
  
cv.waitKey(0)