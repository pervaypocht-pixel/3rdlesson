import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

st.set_page_config(
    page_title="Image Processing App",
    page_icon=":camera:",
    layout="wide"
)

st.title("Image Processing App")
st.write("This app allows you to upload an image and apply various image processing techniques.")

st.sidebar.header("Change Image")

uploaded_file = st.sidebar.file_uploader(
    "Choose an image...",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")
    img_array = np.array(image)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original Image")
        st.image(img_array, width="stretch")

    filter_option = st.sidebar.selectbox(
        "Choose a filter",
        [
            "none",
            "BandW",
            "blur",
            "invert",
            "brightness",
            "contrast",
            "sketch",
            "Flip",
            "Brightness Settings",
            "Contrast Settings",
            "Red Color Splash"
        ])

    processed_image = img_array.copy()

    if filter_option == "BandW":
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        processed_image = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)

    elif filter_option == "blur":
        processed_image = cv2.GaussianBlur(img_array, (15, 15), 0)

    elif filter_option == "invert":
        processed_image = 255 - img_array

    elif filter_option == "brightness":
        processed_image = cv2.convertScaleAbs(
            img_array, alpha=1.0, beta=50
        )

    elif filter_option == "contrast":
        processed_image = cv2.convertScaleAbs(
            img_array, alpha=1.8, beta=0
        )

    elif filter_option == "sketch":
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        inverted = 255 - gray
        blurred = cv2.GaussianBlur(inverted, (21, 21), 0)
        processed_image = cv2.divide(gray, 255 - blurred, scale=256)
    elif filter_option == "Flip":
        processed_image = cv2.flip(img_array, 1)
    elif filter_option == "Brightness Settings":

        brightness_val = st.sidebar.slider(
            "Brightness Level",
            -100, 100, 0
        )

        processed_image = cv2.convertScaleAbs(
            img_array, alpha=1.0, beta=brightness_val
        )
    elif filter_option == "Contrast Settings":

        contrast_val = st.sidebar.slider(
            "Contrast Level",
            0.5, 3.0, 1.0, step=0.1
        )

        processed_image = cv2.convertScaleAbs(
            img_array, alpha=contrast_val, beta=0
        )
    elif filter_option == " Red Color Splash":

     hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)

     lower_red1 = np.array([0, 100, 100])
     upper_red1 = np.array([10, 255, 255])

     lower_red2 = np.array([160, 100, 100])
     upper_red2 = np.array([180, 255, 255])

     mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
     mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

     mask = mask1 + mask2


     gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
     gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)

     processed_image = np.where(
         mask[:, :, np.newaxis] > 0,
         img_array,
         gray)
    

    with col2:
        st.subheader("Processed Image")
        st.image(processed_image, width="stretch")

        result_image = Image.fromarray(processed_image)

        buf = io.BytesIO()
        result_image.save(buf, format="PNG")

        bytes_im = buf.getvalue()

        st.download_button(
            label="Download Processed Image",
            data=bytes_im,
            file_name="processed_image.png",
            mime="image/png")