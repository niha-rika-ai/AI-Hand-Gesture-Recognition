import cv2
import os

gesture_name = input("Enter Gesture Name: ")

save_path = f"dataset/{gesture_name}"

os.makedirs(save_path, exist_ok=True)

cap = cv2.VideoCapture(0)

count = 0

while True:
    ret, frame = cap.read()

    cv2.putText(frame, f"Images: {count}", (10,40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.imshow("Collecting Data", frame)

    key = cv2.waitKey(1)

    if key == ord('s'):
        img_name = f"{save_path}/{count}.jpg"
        cv2.imwrite(img_name, frame)
        count += 1

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()