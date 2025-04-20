import cv2
import numpy as np

# Initialize model paths
yolo_cfg_path = "yolov3.cfg"  # Path to YOLO configuration file
yolo_weights_path = "best2.pt"  # Path to YOLO weights file
yolo_class_names_path = "coco.names"  # Path to class names file

# Load YOLO model
net = cv2.dnn.readNetFromDarknet(yolo_cfg_path, yolo_weights_path)
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Load class names
with open(yolo_class_names_path, 'r') as f:
    class_names = [line.strip() for line in f.readlines()]

def modelInference(task_number):
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    mid_line = frame_width // 2

    # Initialize counters for detected objects
    xs_count = s_count = m_count = l_count = 0
    overflow_count = standard_count = underfill_count = 0

    tracking_history = {}  # tracking_id: previous_x
    counted_ids = set()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), (0, 0, 0), swapRB=True, crop=False)
        net.setInput(blob)
        outputs = net.forward(output_layers)

        # Process detections
        class_ids = []
        confidences = []
        boxes = []

        height, width = frame.shape[:2]
        for output in outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.4:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x1 = int(center_x - w / 2)
                    y1 = int(center_y - h / 2)

                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([x1, y1, w, h])

        # Apply non-maxima suppression
        indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.4, 0.6)
        if len(indices) > 0:
            for i in indices.flatten():
                x1, y1, w, h = boxes[i]
                cls_id = class_ids[i]
                confidence = confidences[i]

                # Get the tracking ID and center X of bounding box
                center_x = x1 + w // 2

                # Track objects and count on crossing mid-line
                tracking_id = cls_id  # Simplified tracking by class ID for this example
                prev_x = tracking_history.get(tracking_id)

                if prev_x is not None and tracking_id not in counted_ids:
                    if prev_x < mid_line and center_x >= mid_line:
                        if task_number == 1:  # Size Detection
                            if cls_id == 0:
                                xs_count += 1
                            elif cls_id == 1:
                                s_count += 1
                            elif cls_id == 2:
                                m_count += 1
                            elif cls_id == 3:
                                l_count += 1
                        elif task_number == 2:  # Fill Level Detection
                            if cls_id == 0:
                                overflow_count += 1
                            elif cls_id == 1:
                                standard_count += 1
                            elif cls_id == 2:
                                underfill_count += 1
                        counted_ids.add(tracking_id)

                tracking_history[tracking_id] = center_x

                # Draw bounding box and label
                color = (0, 255, 0) if task_number == 1 else (0, 0, 255)
                label = f"{class_names[cls_id]}: {confidence:.2f}"
                cv2.rectangle(frame, (x1, y1), (x1 + w, y1 + h), color, 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        # Draw mid-line
        cv2.line(frame, (mid_line, 0), (mid_line, 720), (0, 255, 255), 2)

        # Display counts
        if task_number == 1:
            cv2.putText(frame, f'Extra Small: {xs_count}', (50, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
            cv2.putText(frame, f'Small: {s_count}', (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            cv2.putText(frame, f'Medium: {m_count}', (50, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 165, 255), 2)
            cv2.putText(frame, f'Large: {l_count}', (50, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
        else:
            cv2.putText(frame, f'Standard: {standard_count}', (50, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            cv2.putText(frame, f'Underfill: {underfill_count}', (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 165, 255), 2)
            cv2.putText(frame, f'Overflow: {overflow_count}', (50, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        # Display the annotated frame
        cv2.imshow("Bottle Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

