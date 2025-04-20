
import os
os.environ["YOLO_VERBOSE"] = "False"

from ultralytics import YOLO
import cv2


def modelInference(task_number):
    if task_number == 1:
        model_path = "best.pt"  # Size Detection Model
    elif task_number == 2:
        model_path = "best2.pt"  # Fill Level Detection Model
    else:
        print("Invalid task number.")
        return

    model = YOLO(model_path, task="detect")
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    mid_line = frame_width // 2

    # Label names for Size Detection (Mode 1)
    if task_number == 1:
        class_names = ["Extra Small", "Small", "Medium", "Large"]
        xs_count = 0
        s_count = 0
        m_count = 0
        l_count = 0

    # Label names for Fill Level Detection (Mode 2)
    elif task_number == 2:
        class_names = ["Overflow", "Standard", "Underfill"]
        overflow_count = 0
        standard_count = 0
        underfill_count = 0

    tracking_history = {}  # tracking_id: previous_x
    counted_ids = set()
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
                confidence = float(box.conf[0])
                if confidence < 0.4:
                    continue  # Skip low-confidence predictions

                cls_id = int(box.cls[0])
                tracking_id = int(box.id[0]) if box.id is not None else None

                # Get center x of the bounding box
                x1, y1, x2, y2 = box.xyxy[0]
                center_x = int((x1 + x2) / 2)

                if tracking_id is not None:
                    prev_x = tracking_history.get(tracking_id)

                    # Detect crossing from left to right
                    if prev_x is not None and tracking_id not in counted_ids:
                        if prev_x < mid_line and center_x >= mid_line:
                            if task_number == 1:
                                if cls_id == 0:
                                    xs_count += 1
                                elif cls_id == 1:
                                    s_count += 1
                                elif cls_id == 2:
                                    m_count += 1
                                elif cls_id == 3:
                                    l_count += 1
                            elif task_number == 2:
                                if cls_id == 0:
                                    overflow_count += 1
                                elif cls_id == 1:
                                    standard_count += 1
                                elif cls_id == 2:
                                    underfill_count += 1
                            counted_ids.add(tracking_id)

                    tracking_history[tracking_id] = center_x

        annotated_frame = results.plot()

        # Draw mid-line
        cv2.line(annotated_frame, (mid_line, 0), (mid_line, 720), (0, 255, 255), 2)

        # Display counts
        if task_number == 1:
            cv2.putText(annotated_frame, f'Large: {xs_count}', (50, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
            cv2.putText(annotated_frame, f'Medium: {s_count}', (50, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            cv2.putText(annotated_frame, f'Small: {m_count}', (50, 120),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 165, 255), 2)
            cv2.putText(annotated_frame, f'Extra Small: {l_count}', (50, 160),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
        else:
            cv2.putText(annotated_frame, f'Standard: {standard_count}', (50, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            cv2.putText(annotated_frame, f'Underfill: {underfill_count}', (50, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 165, 255), 2)
            cv2.putText(annotated_frame, f'Overflow: {overflow_count}', (50, 120),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        cv2.imshow("Bottle Detection", annotated_frame)
        frame_no += 1

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
