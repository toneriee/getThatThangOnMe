import cv2


# ==========================================
# 1. Load face detector
# ==========================================

face_cascade = cv2.CascadeClassifier("haar_face.xml")


# ==========================================
# 2. Load emoji
# ==========================================

emoji = cv2.imread(r"Photos\smiley_circle_transparent.png", cv2.IMREAD_UNCHANGED)


# ==========================================
# 3. Open input video
# ==========================================

cap = cv2.VideoCapture(r"Videos\connectplcnvscode.mp4")

if not cap.isOpened():
    print("Could not open video")
    exit()


# ==========================================
# 4. Get video information
# ==========================================

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)


# ==========================================
# 5. Create output video
# ==========================================

fourcc = cv2.VideoWriter_fourcc(*"mp4v")

out = cv2.VideoWriter(
    "output.mp4",
    fourcc,
    fps,
    (width, height)
)


# ==========================================
# 6. Function to overlay emoji
# ==========================================

def overlay_image(background, overlay, x, y, size):

    overlay = cv2.resize(
        overlay,
        (size, size)
    )

    h, w = overlay.shape[:2]

    # Check boundaries
    if x < 0 or y < 0:
        return background

    if x + w > background.shape[1]:
        return background

    if y + h > background.shape[0]:
        return background

    # RGB
    overlay_rgb = overlay[:, :, :3]

    # Alpha / transparency
    alpha = overlay[:, :, 3] / 255.0

    for c in range(3):

        background[
            y:y+h,
            x:x+w,
            c
        ] = (
            alpha * overlay_rgb[:, :, c]
            +
            (1 - alpha)
            *
            background[
                y:y+h,
                x:x+w,
                c
            ]
        )

    return background


# ==========================================
# 7. Process video frame-by-frame
# ==========================================

while True:

    ret, frame = cap.read()

    if not ret:
        break


    # Convert to grayscale
    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )


    # Detect faces
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5
    )


    # Process detected faces
    for (x, y, w, h) in faces:

        # Face center
        face_center_x = x + w // 2
        face_center_y = y + h // 2


        # Emoji size
        emoji_size = int(w * 1.2)


        # Emoji position
        emoji_x = (
            face_center_x
            - emoji_size // 2
        )

        emoji_y = (
            face_center_y
            - emoji_size // 2
        )


        # Put emoji on face
        frame = overlay_image(
            frame,
            emoji,
            emoji_x,
            emoji_y,
            emoji_size
        )


    # Show processed frame
    cv2.imshow(
        "Emoji Tracking",
        frame
    )


    # Save processed frame
    out.write(frame)


    # Press Q to stop
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# ==========================================
# 8. Cleanup
# ==========================================

cap.release()
out.release()
cv2.destroyAllWindows()

print("Done! Saved as output.mp4")