import streamlit as st
import cv2
import numpy as np
from PIL import Image
st.set_page_config(page_title="Image Processing App", page_icon=":camera:", layout="wide")
st.title("Image Processing App")
st.write("This app allows you to upload an image and apply various image processing techniques.")
st.sidebar.header("Change Image")
uploaded_file = st.sidebar.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    img_array = np.array(image)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Original Image")
        st.image(img_array,width="stretch")
    filter_option = st.sidebar.selectbox("Choose a filter", ["none", "BandW", "blur", "invert", "vibrance"])
    processed_image = img_array.copy()

    if filter_option == "BandW":
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        processed_image = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
    with col2:
        st.subheader("Processed Image")
        st.image(processed_image,width="stretch")