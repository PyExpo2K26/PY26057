from ultralytics import YOLO
import torch

# This 'if' block is important for Windows to prevent errors
if __name__ == '__main__':
    # 1. Pull the pre-trained 'Nano' model (fast and lightweight)
    model = YOLO('yolo11n.pt') 

    # 2. Start the training/tuning process
    model.train(
        data='data.yaml',    # Path to your config file
        epochs=50,           # Number of rounds to learn
        imgsz=640,          # Standard image resolution
        batch=16,           # How many images to process at once
        name='fruit_quality_check' # Name of your output folder
    )
    
    print("Training complete! Check the 'runs' folder for your weights.")
    