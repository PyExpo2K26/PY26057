import streamlit as st
from ultralytics import YOLO
from PIL import Image
import tempfile

st.title("Fruit & Vegetable Detection")

# Load trained model
model = YOLO("models/best.pt")


uploaded_file = st.file_uploader("Upload Image", type=["jpg","png","jpeg"])

if uploaded_file is not None:

    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image")

    # save temporary image
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(uploaded_file.read())

    # prediction
    results = model(temp_file.name)

    # show result
    res_plotted = results[0].plot()
    st.image(res_plotted, caption="Detection Result")
