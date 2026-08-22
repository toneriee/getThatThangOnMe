import cv2 as cv
import urllib.request
import numpy as np
import matplotlib.pyplot as plt

def rescaleFrame(frame, scale=0.5):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)

    dimensions = (width, height)

    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

url = "https://i.pinimg.com/1200x/46/86/6a/46866a41aaf6e1b00ca993cac75cc538.jpg"
resp = urllib.request.urlopen(url)
image = np.asarray(bytearray(resp.read()), dtype=np.uint8)
img = cv.imdecode(image, cv.IMREAD_COLOR)
cv.imshow('Image',img)
# gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# cv.imshow('Gray',gray)
blank = np.zeros(img.shape[:2], dtype='uint8')
circle = cv.circle(blank, (img.shape[1]//2,img.shape[0]//2),100,255,-1)
mask = cv.bitwise_and(img,img, mask=circle)
# # Grayscale histogram
# gray_hist = cv.calcHist([gray], [0], mask, [256], [0,256])
cv.imshow('Mask',mask)
plt.figure()
plt.title('Color Histogram')
plt.xlabel('Bins')
plt.ylabel('# of pixels')
# plt.plot(gray_hist)
# plt.xlim([0,256])
# plt.show()

# Color Histogram
colors = ('b','g','r')
for i,col in enumerate(colors):
    hist = cv.calcHist([img], [i], circle, [256], [0,256])
    plt.plot(hist, color=col)
    plt.xlim([0,256])
plt.show()
# resized_img = rescaleFrame(img)

while True:
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()