import streamlit as st
import pytesseract
import cv2
from PIL import Image
import numpy as np
import os

# Placeholder functions to represent content for each page
def show_about():
    st.subheader("About Us")
    st.write("This is the About Us section. Here you can provide information about your project or company.")

def show_doctor():
    st.subheader("Doctor")
    st.write("This section provides information about the doctors, their specialization, and services offered.")

def show_heart():
    st.subheader("Heart")
    st.write("This section provides information about heart health and related topics.")

def show_contact():
    st.subheader("Contact")
    st.write("This section provides contact information and ways to get in touch.")

# Configure Tesseract OCR path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Add custom CSS for the navbar and general styling
st.markdown("""
    <style>
        /* Navbar styles */
        .navbar {
            background-color: #333;
            overflow: hidden;
            position: sticky;
            top: 0;
            width: 100%;
            z-index: 10;
        }

        .navbar a {
            float: left;
            display: block;
            color: white;
            text-align: center;
            padding: 14px 20px;
            text-decoration: none;
            font-size: 18px;
        }

        .navbar a:hover {
            background-color: #ddd;
            color: black;
        }

        /* Styling for the title */
        .title {
            font-size: 40px;
            font-weight: bold;
            color: #4CAF50;
            text-align: center;
            margin-top: 20px;
        }

        /* Styling for subheader */
        .subheader {
            font-size: 24px;
            color: #FF5722;
            text-align: center;
            margin-top: 20px;
        }

        /* Styling for the image and uploader */
        .upload-container {
            text-align: center;
            margin-top: 20px;
            padding: 20px;
            background-color: #e7f7e7;
            border-radius: 8px;
        }

        /* Styling for buttons */
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
            border-radius: 8px;
            padding: 10px 20px;
            transition: background-color 0.3s;
        }

        .stButton>button:hover {
            background-color: #45a049;
        }

        /* Styling for text area */
        .stTextArea>div>div>textarea {
            font-size: 16px;
            padding: 10px;
            border-radius: 8px;
            background-color: #f4f4f4;
        }

        /* Footer style */
        .footer {
            font-size: 14px;
            color: #888;
            text-align: center;
            margin-top: 40px;
        }
    </style>
""", unsafe_allow_html=True)

# Navbar HTML structure
st.markdown("""
    <div class="navbar">
        <a href="#home">Home</a>
        <a href="#ocr">OCR Text Extraction</a>
        <a href="#about">About</a>
    </div>
""", unsafe_allow_html=True)

# Sidebar for navigation
pages = {
    "About Us": "ℹ️ About Us",
    "Doctor": "👨‍⚕️ Doctor",
    "Heart": "❤️ Heart",
    "Contact": "📞 Contact",
}

selection = st.sidebar.radio("", list(pages.values()), key="nav")

# Display the selected page content
if selection == "ℹ️ About Us":
    show_about()
elif selection == "👨‍⚕️ Doctor":
    show_doctor()
elif selection == "❤️ Heart":
    show_heart()
elif selection == "📞 Contact":
    show_contact()

# Streamlit App
if selection == "ℹ️ About Us" or selection == "OCR Text Extraction":
    st.markdown('<p class="title">Nepali Text Extraction from Image</p>', unsafe_allow_html=True)
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

# Footer with additional info
st.markdown('<p class="footer">Built with ❤️ using [Streamlit](https://streamlit.io/) and [Tesseract OCR](https://github.com/tesseract-ocr/tesseract).</p>', unsafe_allow_html=True)


