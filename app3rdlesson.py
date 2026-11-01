import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
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
    filter_option = st.sidebar.selectbox("Choose a filter", ["none", "BandW", "blur", "invert", "brightness", "contrast","sketch"])
    processed_image = img_array.copy()

    if filter_option == "BandW":
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        processed_image = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
    elif filter_option == "blur":
        processed_image = cv2.GaussianBlur(img_array, (15, 15), 0)
    elif filter_option == "invert":
        processed_image = 255 - img_array
    elif filter_option == "brightness":
        processed_image = cv2.convertScaleAbs(img_array, alpha=1.0, beta=50)
    elif filter_option == "contrast":
        processed_image = cv2.convertScaleAbs(img_array, alpha=1.8, beta=0)
    elif filter_option == "sketch":
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        inverted = 255 - gray
        blurred = cv2.GaussianBlur(inverted, (21, 21), 0)
        processed_image = cv2.divide(gray, 255 - blurred, scale=256)
    with col2:
        st.subheader("Processed Image")
        st.image(processed_image,width="stretch")
        result_image = Image.fromarray(processed_image)
        buf = io.BytesIO()
        result_image.save(buf, format="PNG")
        bytes_im = buf.getvalue()

        st.download_button(
            label="Download Processed Image",
            data=bytes_im,
            file_name="processed_image.png",
            mime="image/png"
        )