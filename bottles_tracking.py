from ultralytics import YOLO
import cv2

# Load the model
model = YOLO("best2.onnx", task="detect")

# Start video capture
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

frame_no = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    # Track objects in the frame
    result_list = model.track(frame, persist=True)

    # `result_list` might be a generator in some versions
    results = list(result_list)[0]  # Convert to list and get first result safely

    # Debug: print class names and IDs
    if results.boxes is not None:
        for box in results.boxes:
            cls_id = int(box.cls[0])
            tracking_id = int(box.id[0]) if box.id is not None else None
            print(f"Class: {model.names[cls_id]}, ID: {tracking_id}")

    # Annotate frame
    annotated_frame = results.plot()
    cv2.imshow("Object Tracking", annotated_frame)
    cv2.imwrite(f"tracked_frame{frame_no}.jpg", annotated_frame)

    frame_no += 1

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
