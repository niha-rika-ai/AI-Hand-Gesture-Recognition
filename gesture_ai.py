import cv2
import mediapipe as mp
import pyttsx3
import time

# ==============================
# MediaPipe Initialization
# ==============================

mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.75,
    min_tracking_confidence=0.75
)

mp_draw = mp.solutions.drawing_utils

# ==============================
# Voice Engine
# ==============================

engine = pyttsx3.init()

# Voice speed
engine.setProperty('rate', 150)

last_gesture = ""

# ==============================
# Webcam
# ==============================

cap = cv2.VideoCapture(0)

# Camera Resolution
cap.set(3, 1280)
cap.set(4, 720)

prev_time = 0

gesture = "WAITING..."

# ==============================
# Main Loop
# ==============================

while True:

    success, frame = cap.read()

    if not success:
        break

    # Mirror Effect
    frame = cv2.flip(frame, 1)

    # RGB Conversion
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Hand Detection
    results = hands.process(rgb)

    # ==============================
    # HAND LANDMARKS
    # ==============================

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            # Stylish Hand Drawing
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,

                mp_draw.DrawingSpec(
                    color=(0, 255, 255),
                    thickness=2,
                    circle_radius=3
                ),

                mp_draw.DrawingSpec(
                    color=(255, 255, 255),
                    thickness=2
                )
            )

            landmarks = []

            # Store Landmark Coordinates
            for lm in hand_landmarks.landmark:
                landmarks.append([lm.x, lm.y])

            # ==============================
            # Finger Detection
            # ==============================

            tip_ids = [4, 8, 12, 16, 20]

            fingers = []

            # Thumb
            if landmarks[4][0] < landmarks[3][0]:
                fingers.append(1)
            else:
                fingers.append(0)

            # Other Fingers
            for tip in [8, 12, 16, 20]:

                if landmarks[tip][1] < landmarks[tip - 2][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            total_fingers = fingers.count(1)

            # ==============================
            # Gesture Recognition
            # ==============================

            if fingers == [0, 0, 0, 0, 0]:
                gesture = "FIST"

            elif fingers == [0, 1, 0, 0, 0]:
                gesture = "ONE"

            elif fingers == [0, 1, 1, 0, 0]:
                gesture = "VICTORY"

            elif fingers == [0, 0, 1, 1, 1]:
                gesture = "NICE"

            elif fingers == [0, 1, 1, 1, 1]:
                gesture = "PALM"

            elif fingers == [1, 1, 1, 1, 1]:
                gesture = "OPEN HAND"

            elif fingers == [1, 0, 0, 0, 1]:
                gesture = "ROCK"

            elif fingers == [1, 0, 0, 0, 0]:
                gesture = "THUMBS UP"

            else:
                gesture = "UNKNOWN"

            # ==============================
            # Voice Output
            # ==============================

            if gesture != last_gesture:

                engine.say(gesture)
                engine.runAndWait()

                last_gesture = gesture

            # ==============================
            # Confidence Score
            # ==============================

            confidence = int((total_fingers / 5) * 100)

            # ==============================
            # Futuristic UI Panel
            # ==============================

            # Main Box
            cv2.rectangle(frame, (20, 20), (450, 180), (15, 15, 15), -1)

            # Border
            cv2.rectangle(frame, (20, 20), (450, 180), (0, 255, 255), 2)

            # Gesture Text
            cv2.putText(
                frame,
                f"Gesture : {gesture}",
                (40, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2
            )

            # Finger Count
            cv2.putText(
                frame,
                f"Fingers : {total_fingers}",
                (40, 115),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 255, 0),
                2
            )

            # Confidence
            cv2.putText(
                frame,
                f"Confidence : {confidence}%",
                (40, 155),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 0),
                2
            )

    # ==============================
    # FPS Counter
    # ==============================

    current_time = time.time()

    fps = 1 / (current_time - prev_time)

    prev_time = current_time

    cv2.putText(
        frame,
        f"FPS : {int(fps)}",
        (1050, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    # ==============================
    # AI Title
    # ==============================

    cv2.putText(
        frame,
        "AI Gesture Control System",
        (320, 680),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 0, 255),
        2
    )

    # ==============================
    # Show Window
    # ==============================

    cv2.imshow("Gesture AI", frame)

    # Exit Key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ==============================
# Release Resources
# ==============================

cap.release()

cv2.destroyAllWindows()