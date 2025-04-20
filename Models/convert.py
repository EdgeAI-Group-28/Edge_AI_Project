from ultralytics import YOLO
model = YOLO("best2.pt")  # Load a pretrained YOLOv8 model
model.export(format="onnx", dynamic=True) # dynamic=True  # Export the model to ONNX format