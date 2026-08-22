import cv2 as cv
import numpy as np
blank = np.zeros((500,500,3), dtype='uint8')
cv.imshow("Blank", blank)

# 1. Paint the image a certain color
# blank[200:300, 200:300] = 0,255,0
# cv.imshow("Painted", blank)

# 2. Draw a rectangle
# cv.rectangle(blank, (0,0), (blank.shape[1]//2, blank.shape[0]//2), (0,255,0), thickness =-1)
# cv.imshow("Rectangle", blank)

# # 3. Draw a circle
# cv.circle(blank, (blank.shape[1]//2, blank.shape[0]//2), 40, (0,0,255), thickness = -1)
# cv.imshow("Circle", blank)

# # 4. Draw a line
# cv.line(blank, (0,300), (blank.shape[1]//2, blank.shape[0]//2), (255,255,255), thickness = 5)
# cv.imshow("Line", blank)

# 5. Write text
cv.putText(blank, 'Hello', (190,50), cv.FONT_HERSHEY_TRIPLEX, 1.0, (255,0,0), 2)
cv.putText(blank, 'Everyone', (190,90), cv.FONT_HERSHEY_TRIPLEX, 1.0, (255,0,0), 2)
cv.imshow("Line", blank)
cv.waitKey(0)
