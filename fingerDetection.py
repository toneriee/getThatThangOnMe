import cv2
import time
import os
import HandTrackingModule as htm
width, height = 640, 480
cap = cv2.VideoCapture(2)  # try 0 first

cap.set(3, width)
cap.set(4, height)

folderPath = "FingersImages"
os.makedirs(folderPath, exist_ok=True)  # ensure folder exists
myList = os.listdir(folderPath)
print(myList)

overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    # print(f'{folderPath}/{imPath}')
    overlayList.append(image)
print(len(overlayList))

prev_time = 0
detector = htm.HandDetector(detectionCon=0.75)
tipIds = [4, 8, 12 , 16, 20]

while True:
    ret, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    # print(lmList)

    if len(lmList) != 0:
        fingers=[]
        # Thumb
        if lmList[tipIds[0]][1]>lmList[tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # 4 Fingers
        for id in range(1,5):
            if lmList[tipIds[id]][2]<lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        # print(fingers)
        totalFingers = fingers.count(1)
        print(totalFingers)
        h, w, c = overlayList[totalFingers-1].shape
        img[0:h, 0:w] = overlayList[totalFingers-1]
        cv2.rectangle(img, (0,200), (140,400), (0,255,0), cv2.FILLED)
        cv2.putText(img, str(totalFingers), (16,355), cv2.FONT_HERSHEY_PLAIN, 10, (255,0,0), 25)

    current_time = time.time()
    
    fps = 1 / (current_time - prev_time)
    
    prev_time = current_time
    
    cv2.putText(img,f"FPS: {fps:.1f}",(500, 30),cv2.FONT_HERSHEY_PLAIN,2 ,(255, 0, 0),1)
    
    if not ret:
        print("Camera not accessible")
        break

    cv2.imshow("Image", img)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
