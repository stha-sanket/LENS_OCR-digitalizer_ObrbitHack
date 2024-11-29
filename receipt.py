import streamlit as st
from PIL import Image
import pytesseract
import pandas as pd
import re

# Configure Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Function to parse tabular data
def extract_table_data(text):
    # Match rows with table data
    rows = []
    for line in text.split("\n"):
        if re.match(r"^\d+(\s+\w.*?)+\s+[\d,.]+$", line):  # Matches tabular rows (e.g., SN, description, and numbers)
            rows.append(re.split(r"\s{2,}", line))  # Split by 2 or more spaces
    return rows

# Streamlit application
def main():
    st.title("Receipt Digitalization")
    st.write("Upload an image of a receipt to extract and digitalize its content.")
    
    # Upload file
    uploaded_file = st.file_uploader("Upload a receipt image (JPG, PNG)", type=["jpg", "png"])
    
    if uploaded_file:
        # Display uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Receipt", use_column_width=True)
        
        # Extract text using Tesseract OCR
        st.write("### Extracting Text...")
        extracted_text = pytesseract.image_to_string(image)
        st.text(extracted_text)
        
        # Split text into general text and table data
        st.write("### Digitalized Receipt Content")
        lines = extracted_text.split("\n")
        
        general_text = []
        table_data = []
        
        for line in lines:
            # Identify table-like rows
            if re.match(r"^\d+(\s+\w.*?)+\s+[\d,.]+$", line):
                table_data.append(re.split(r"\s{2,}", line))
            else:
                general_text.append(line)
        
        # Display general text
        st.write("#### General Information")
        for line in general_text:
            st.text(line)
        
        # Display table data
        if table_data:
            st.write("#### Table Data")
            # Convert to DataFrame for a cleaner display
            df = pd.DataFrame(table_data)
            st.dataframe(df)
        else:
            st.write("No structured table data found.")

if __name__ == "__main__":
    main()
