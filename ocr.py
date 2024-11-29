import numpy as np
import easyocr
import streamlit as st
from PIL import Image

st.title('OCR with EasyOCR')

# Upload the image
uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Open the image
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Image", use_column_width=True)

    # Initialize the EasyOCR reader
    reader = easyocr.Reader(['en'])  # Add language codes like 'en', 'ne' for Nepali if needed

    # Perform OCR
    results = reader.readtext(np.array(img), detail=0)

    # Display results
    st.subheader("Extracted Text:")
    st.text_area("Extracted Text", "\n".join(results), height=200)




