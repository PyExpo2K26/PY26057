from ultralytics import YOLO

model = YOLO("runs/detect/fruit_quality_check3/weights/best.pt")

results = model.predict(
    source="Test/images/Apple",
    show=True,
    save=True
)

