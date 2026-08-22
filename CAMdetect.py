import cv2 as cv
import numpy as np
import time

cap = cv.VideoCapture(2)

# Create CLAHE
clahe = cv.createCLAHE(clipLimit=2.0,tileGridSize=(8, 8))

# Create morphology kernel 
kernel = np.ones((5, 5), np.uint8)

# Variables for FPS calculation
prev_time = time.time()

# Dictionary for smoothing object centers
previous_centers = {}

# ==========================
# Main Loop
# ==========================

while True:

    ret, frame = cap.read()
    if not ret:
        break

    # Convert to HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # CLAHE Brightness Enhancement
    h, s, v = cv.split(hsv)
    v = clahe.apply(v)
    hsv = cv.merge([h, s, v])

    # Dynamic brightness threshold
    brightness = np.mean(v)

    if brightness < 70:
        min_v = 30
    else:
        min_v = 80

    # HSV ranges
    colors = {

        "Red": [(np.array([0, 140, min_v]), np.array([8, 255, 255])),
                (np.array([172, 140, min_v]), np.array([179, 255, 255]))],

        "Green": [(np.array([45, 70, min_v]), np.array([80, 255, 255]))],

        "Blue": [(np.array([100, 80, min_v]), np.array([125, 255, 255]))]
}

    draw_colors = {

        "Red": (0, 0, 255),

        "Green": (0, 255, 0),

        "Blue": (255, 0, 0)

    }

    # ==========================
    # Detect each color
    # ==========================

    for color_name, ranges in colors.items():

        mask = np.zeros(hsv.shape[:2], dtype=np.uint8)

        # Combine all HSV ranges
        for lower, upper in ranges:
            mask |= cv.inRange(hsv, lower, upper)

        # Remove noise
        mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
        mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)

        cv.imshow(color_name, mask)

        contours, _ = cv.findContours(mask,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)

        # Skip if nothing detected
        if len(contours) == 0:
            continue

        # Detect only the largest object
        largest = max(contours, key=cv.contourArea)

        area = cv.contourArea(largest)

        if area < 800:
            continue

        x, y, w, h = cv.boundingRect(largest)

        # aspect_ratio = w / h

        # # Ignore very thin objects
        # if aspect_ratio < 0.5 or aspect_ratio > 2:
        #     continue

        # Object center
        center_x = x + w // 2
        center_y = y + h // 2

        # Smooth coordinates

        if color_name in previous_centers:

            old_x, old_y = previous_centers[color_name]

            center_x = int(old_x * 0.7 + center_x * 0.3)
            center_y = int(old_y * 0.7 + center_y * 0.3)

        previous_centers[color_name] = (center_x, center_y)

        # Store coordinates
    

        # # detected = {

        #     "color": color_name,

        #     "x": center_x,

        #     "y": center_y

        # }

        # Print for debugging
        # print(detected)

        # Draw marker
        cv.drawMarker(frame,(center_x, center_y),(255, 255, 255),markerType=cv.MARKER_CROSS,markerSize=20,thickness=2)

        cv.rectangle(frame,(x, y),(x + w, y + h),draw_colors[color_name],2)

        cv.putText(frame,f"{color_name} ({center_x},{center_y})",(x, y - 10),cv.FONT_HERSHEY_SIMPLEX,0.8,draw_colors[color_name],2)

    # ==========================
    # FPS
    # ==========================

    current_time = time.time()

    fps = 1 / (current_time - prev_time)

    prev_time = current_time

    cv.putText(frame,f"FPS: {fps:.1f}",(10, 30),cv.FONT_HERSHEY_SIMPLEX,0.8,(255, 255, 255),2)

    cv.imshow("Camera", frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()