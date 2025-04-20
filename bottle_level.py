from ultralytics import YOLO
import cv2
from PIL import Image
import numpy as np


def BottleFilling(frame):

    lowerLimit = np.array([20, 100, 100])
    upperLimit = np.array([40, 255, 255])

    if frame is None:
        print("Error: Could not load image.")
        return frame  # Return as-is

    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)
    mask_ = Image.fromarray(mask)
    bbox = mask_.getbbox()

    if bbox is not None:
        x1, y1, x2, y2 = bbox
        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)

    return frame 


model = YOLO("best2.onnx", task="detect")
cap = cv2.VideoCapture(1)
cv2.namedWindow("Cream Soda Detection Live", cv2.WINDOW_NORMAL)


frame_no = 0

while True:
    success, frame = cap.read()
    
    if not success:
        print("Error: Failed to read frame.")
        break   

    result_list = model.track(frame, persist=True)
    results = list(result_list)[0]

    # Annotate and process each detection
    if results.boxes is not None:
        for box in results.boxes:
            cls_id = int(box.cls[0])
            tracking_id = int(box.id[0]) if box.id is not None else None

            # Print tracking debug info
            print(f"Class: {model.names[cls_id]}, ID: {tracking_id}")

            # Get bounding box
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cropped_bottle = frame[y1:y2, x1:x2]

            # Apply your bottle filling logic
            filled_bottle = BottleFilling(cropped_bottle)
            

            # Overwrite the original frame with processed bottle
            frame[y1:y2, x1:x2] = filled_bottle

            # Draw rectangle and label
            label_text = f'{model.names[cls_id]} ID:{tracking_id}'
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label_text, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Show frame
    cv2.imshow("Cream Soda Detection Live", frame)
    cv2.imwrite(f"tracked_frame{frame_no}.jpg", frame)

    frame_no += 1

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()


