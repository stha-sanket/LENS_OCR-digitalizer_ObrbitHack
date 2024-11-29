import streamlit as st
import pytesseract
import cv2
from PIL import Image
import numpy as np
import os


# Configure Tesseract OCR path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Streamlit App
st.title("Nepali Text Extraction from Image")
st.write("Upload an image, and this app will extract text (including Nepali) from it.")

# File uploader
uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Load the image using PIL
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    # Convert the image to a format compatible with OpenCV
    image_np = np.array(image)
    
    # Preprocess the image
    st.write("Preprocessing the image for better OCR results...")

    # Step 1: Resize image (reduce size if resolution is very high)
    height, width, _ = image_np.shape
    max_dimension = 1500  # Limit the maximum dimension
    if max(height, width) > max_dimension:
        scaling_factor = max_dimension / max(height, width)
        new_width = int(width * scaling_factor)
        new_height = int(height * scaling_factor)
        image_np = cv2.resize(image_np, (new_width, new_height), interpolation=cv2.INTER_AREA)
        st.write(f"Image resized to {new_width}x{new_height} for better processing.")

    # Convert to grayscale for better OCR results
    gray_image = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)

    # Perform OCR using Tesseract
    with st.spinner("Extracting text..."):
        try:
            extracted_text = pytesseract.image_to_string(gray_image, lang="nep")
            if extracted_text.strip():
                st.success("Text extracted successfully!")
                st.text_area("Extracted Text", extracted_text, height=200)
            else:
                st.warning("No text was extracted. Please try with a clearer image.")
        except Exception as e:
            st.error(f"Error during text extraction: {e}")

# Optional: Add footer
st.markdown("---")
st.markdown("Built with ❤️ using [Streamlit](https://streamlit.io/) and [Tesseract OCR](https://github.com/tesseract-ocr/tesseract).")
