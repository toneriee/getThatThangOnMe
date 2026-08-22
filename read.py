import cv2 as cv
import urllib.request
import numpy as np

def rescaleFrame(frame, scale=0.5):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)

    dimensions = (width, height)

    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)
url = "https://i.pinimg.com/1200x/a2/ca/cc/a2cacccc96ac624dc0e0deb72adce17d.jpg"
resp = urllib.request.urlopen(url)
image = np.asarray(bytearray(resp.read()), dtype=np.uint8)
img = cv.imdecode(image, cv.IMREAD_COLOR)
resized_img = rescaleFrame(img)
cv.imshow("Geto", resized_img)
cv.waitKey(0)
cv.destroyAllWindows()