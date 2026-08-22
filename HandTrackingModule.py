import cv2
import mediapipe as mp
import time


class HandDetector:

    def __init__(
        self,
        model_path="hand_landmarker.task",
        maxHands=2,
        detectionCon=0.5,
        trackCon=0.5
    ):

        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        # MediaPipe Tasks
        BaseOptions = mp.tasks.BaseOptions
        VisionRunningMode = mp.tasks.vision.RunningMode
        HandLandmarker = mp.tasks.vision.HandLandmarker
        HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions

        # Options
        options = HandLandmarkerOptions(
            base_options=BaseOptions(
                model_asset_path=model_path
            ),
            running_mode=VisionRunningMode.IMAGE,
            num_hands=maxHands,
            min_hand_detection_confidence=detectionCon,
            min_hand_presence_confidence=trackCon,
            min_tracking_confidence=trackCon
        )

        # Create detector
        self.detector = HandLandmarker.create_from_options(options)

        # Store results
        self.results = None

    # ==========================================
    # FIND HANDS
    # ==========================================

    def findHands(self, img, draw=True):

        # OpenCV BGR -> MediaPipe image
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb
        )

        # Detect
        self.results = self.detector.detect(mp_image)

        # Draw landmarks manually
        if draw and self.results.hand_landmarks:

            for hand_landmarks in self.results.hand_landmarks:

                h, w, c = img.shape

                # -----------------------------
                # Draw points
                # -----------------------------

                for lm in hand_landmarks:

                    cx = int(lm.x * w)
                    cy = int(lm.y * h)

                    cv2.circle(
                        img,
                        (cx, cy),
                        5,
                        (0, 0, 255),
                        cv2.FILLED
                    )

                # -----------------------------
                # Draw connections
                # -----------------------------

                connections = [
                    (0, 1),
                    (1, 2),
                    (2, 3),
                    (3, 4),

                    (0, 5),
                    (5, 6),
                    (6, 7),
                    (7, 8),

                    (5, 9),
                    (9, 10),
                    (10, 11),
                    (11, 12),

                    (9, 13),
                    (13, 14),
                    (14, 15),
                    (15, 16),

                    (13, 17),
                    (17, 18),
                    (18, 19),
                    (19, 20),

                    (0, 17)
                ]

                for start, end in connections:

                    x1 = int(hand_landmarks[start].x * w)
                    y1 = int(hand_landmarks[start].y * h)

                    x2 = int(hand_landmarks[end].x * w)
                    y2 = int(hand_landmarks[end].y * h)

                    cv2.line(
                        img,
                        (x1, y1),
                        (x2, y2),
                        (0, 255, 0),
                        2
                    )

        return img

    # ==========================================
    # FIND POSITION
    # ==========================================

    def findPosition(self, img, handNo=0, draw=True):

        lmList = []

        # Check if a hand exists
        if self.results and self.results.hand_landmarks:

            # Check requested hand number
            if handNo >= len(self.results.hand_landmarks):
                return lmList

            myHand = self.results.hand_landmarks[handNo]

            h, w, c = img.shape

            # Get 21 landmarks
            for id, lm in enumerate(myHand):

                cx = int(lm.x * w)
                cy = int(lm.y * h)

                lmList.append([id, cx, cy])

                # Draw circle
                if draw:

                    cv2.circle(
                        img,
                        (cx, cy),
                        8,
                        (255, 0, 255),
                        cv2.FILLED
                    )

        return lmList


# ==============================================
# MAIN
# ==============================================

def main():

    pTime = 0

    # Camera
    cap = cv2.VideoCapture(2)

    # Create detector
    detector = HandDetector(
        model_path="hand_landmarker.task",
        maxHands=2,
        detectionCon=0.5,
        trackCon=0.5
    )

    while True:

        # Read camera
        success, img = cap.read()

        if not success:
            print("Cannot read camera")
            break

        # --------------------------------------
        # Find hands
        # --------------------------------------

        img = detector.findHands(img)

        # --------------------------------------
        # Get landmark positions
        # --------------------------------------

        lmList = detector.findPosition(img)

        # Print landmarks
        if len(lmList) != 0:

            print(lmList)

            # Example:
            # landmark 8 = index fingertip

            x8 = lmList[8][1]
            y8 = lmList[8][2]

            print(
                "Index fingertip:",
                x8,
                y8
            )

        # --------------------------------------
        # FPS
        # --------------------------------------

        cTime = time.time()

        fps = 1 / (cTime - pTime)

        pTime = cTime

        cv2.putText(
            img,
            f"FPS: {int(fps)}",
            (500, 30),
            cv2.FONT_HERSHEY_PLAIN,
            2,
            (255, 0, 0),
            1
        )

        # --------------------------------------
        # Show
        # --------------------------------------

        cv2.imshow(
            "Hand Tracking",
            img
        )

        # Press Q to quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # ------------------------------------------
    # Cleanup
    # ------------------------------------------

    cap.release()
    cv2.destroyAllWindows()


# ==============================================
# RUN PROGRAM
# ==============================================

if __name__ == "__main__":
    main()