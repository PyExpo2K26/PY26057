from ultralytics import YOLO
# This pulls the smallest model to test
model = YOLO("yolo11n.pt") 
print("Success! YOLO is installed and ready.")