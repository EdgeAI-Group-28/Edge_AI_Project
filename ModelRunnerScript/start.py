import model
import os

os.environ["YOLO_VERBOSE"] = "False"

user_input = int(input("Enter the task : (1)Size Detection , (2)Filling Level : "))
model.modelInference(user_input)