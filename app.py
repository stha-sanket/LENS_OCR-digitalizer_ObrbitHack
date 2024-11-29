# import streamlit as st
# from PIL import Image
# import pytesseract

# # Set the path to the Tesseract executable (update this for Windows)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
#   # Update for Windows

# # Streamlit app
# def main():
#     st.title("OCR Document Digitalizer")
#     st.markdown("Upload an image file to extract text using Tesseract OCR.")
    
#     # File uploader
#     uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

#     if uploaded_file is not None:
#         # Open the image file
#         image = Image.open(uploaded_file)

#         # Display the uploaded image
#         st.image(image, caption="Uploaded Image", use_column_width=True)

#         # Perform OCR to extract text
#         extracted_text = pytesseract.image_to_string(image)

#         # Display the extracted text
#         if extracted_text:
#             st.subheader("Extracted Text:")
#             st.text_area("Text", extracted_text, height=300)
#         else:
#             st.warning("No text detected in the image.")

# if __name__ == "__main__":
#     main()


import streamlit as st
from PIL import Image
import pytesseract
import pandas as pd
from fpdf import FPDF
import re

# Set the path to the Tesseract executable (update this for Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update for Windows

# Function to extract invoice data in a standardized table format
def extract_invoice_data(text):
    # Regular expressions to extract standard invoice fields
    item_pattern = r"([a-zA-Z0-9\s]+)"  # Match item description
    quantity_pattern = r"(\d+)"  # Match quantity
    price_pattern = r"(\d+\.\d{2})"  # Match price with decimal
    amount_pattern = r"(\d+\.\d{2})"  # Match amount with decimal
    
    # Split the text into lines
    lines = text.split('\n')

    # Initialize lists to hold the extracted data
    items = []
    quantities = []
    unit_prices = []
    amounts = []

    # Loop through lines to extract data using regular expressions
    for line in lines:
        item_match = re.search(item_pattern, line)
        quantity_match = re.search(quantity_pattern, line)
        price_match = re.search(price_pattern, line)
        amount_match = re.search(amount_pattern, line)

        # If we find a match for item, quantity, price, and amount, store it
        if item_match and quantity_match and price_match and amount_match:
            items.append(item_match.group(1).strip())
            quantities.append(quantity_match.group(1).strip())
            unit_prices.append(price_match.group(1).strip())
            amounts.append(amount_match.group(1).strip())

    # Return as a DataFrame to display as a table
    invoice_data = {
        "Item/Description": items,
        "Quantity": quantities,
        "Unit Price": unit_prices,
        "Amount": amounts
    }
    
    return pd.DataFrame(invoice_data)

# Function to generate PDF for non-invoice documents
def generate_pdf(text, filename="document.pdf"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text)
    
    pdf.output(filename)

# Streamlit app
def main():
    st.title("OCR Document Digitalizer")
    st.markdown("Upload an image file to extract text using Tesseract OCR.")
    
    # File uploader
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        # Open the image file
        image = Image.open(uploaded_file)

        # Display the uploaded image
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Perform OCR to extract text
        extracted_text = pytesseract.image_to_string(image)

        # Display the extracted text
        if extracted_text:
            st.subheader("Extracted Text:")
            st.text_area("Text", extracted_text, height=300)
            
            # Check if the text contains the word "Invoice" or a known structure
            if "invoice" in extracted_text.lower():
                # Extract invoice data into a table
                invoice_df = extract_invoice_data(extracted_text)
                
                if not invoice_df.empty:
                    st.subheader("Invoice Data:")
                    st.write(invoice_df)
                    
                    # Provide option to download the invoice as a CSV
                    csv = invoice_df.to_csv(index=False)
                    st.download_button(label="Download Invoice CSV", data=csv, file_name="invoice.csv", mime="text/csv")
                
            else:
                # For other documents, generate PDF
                st.subheader("Document PDF:")
                pdf_file_name = "document.pdf"
                generate_pdf(extracted_text, pdf_file_name)
                
                # Provide a download button for the PDF
                with open(pdf_file_name, "rb") as f:
                    st.download_button(label="Download PDF", data=f, file_name=pdf_file_name, mime="application/pdf")
                
        else:
            st.warning("No text detected in the image.")

if __name__ == "__main__":
    main()
