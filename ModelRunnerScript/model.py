from ultralytics import YOLO
import cv2


def modelInference(task_number):
    
    if task_number == 1:
        model = "best.pt"

    elif task_number == 2:
        model = "last.pt"
    

    model = YOLO(model, task="detect")
    cap = cv2.VideoCapture(0)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        exit()

    frame_no = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        result_list = model.track(frame, persist=True)
        results = list(result_list)[0] 

        if results.boxes is not None:
            for box in results.boxes:
                cls_id = int(box.cls[0])
                tracking_id = int(box.id[0]) if box.id is not None else None
                #print(f"Class: {model.names[cls_id]}, ID: {tracking_id}")

        annotated_frame = results.plot()
        cv2.imshow("Object Tracking ", annotated_frame)
        #cv2.imwrite(f"tracked_frame{frame_no}.jpg", annotated_frame)

        frame_no += 1

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()