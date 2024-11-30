import streamlit as st
from PIL import Image
import pytesseract
import pandas as pd
from fpdf import FPDF
import re
import time

# Configure Tesseract path (update for your environment)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update for Windows

# Function to extract table data
def extract_table_data(text):
    rows = []
    for line in text.split("\n"):
        if re.match(r"^\d+(\s+\w.*?)+\s+[\d,.]+$", line):  # Matches tabular rows (e.g., SN, description, and numbers)
            rows.append(re.split(r"\s{2,}", line))  # Split by 2 or more spaces
    return rows

# Function to extract invoice data into a standardized table format
def extract_invoice_data(text):
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

# Streamlit app implementation in show() function
def show():
    st.title("🖼️ OCR Document Digitalizer")
    st.markdown("""
        **OCR Document Digitalizer** allows you to upload images and extract text using **Tesseract OCR**.  
        - If the document is an invoice, it will extract the item details.
        - For other documents, the text will be converted into a downloadable PDF.
        - Structured table data (e.g., receipts) is displayed in a clean format.
    """)
    
    # Language selection for OCR
    lang_choice = st.selectbox("Choose the language for OCR", ["eng", "nepali", "deu", "fra", "spa"], index=0)
    st.markdown(f"Selected OCR Language: **{lang_choice.upper()}**")

    # File uploader widget
    uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        # Display uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Show progress bar while OCR is processing
        with st.spinner("Extracting text from the image..."):
            time.sleep(2)  # Simulate processing time
            progress_bar = st.progress(0)

            for i in range(1, 101):
                time.sleep(0.02)
                progress_bar.progress(i)

            # Perform OCR to extract text
            extracted_text = pytesseract.image_to_string(image, lang=lang_choice)

        # Display the extracted text
        if extracted_text.strip():
            st.subheader("Extracted Text:")
            st.text_area("Text", extracted_text, height=300)

            # Check if the document is an invoice
            if "invoice" in extracted_text.lower():
                # Extract invoice data into a table
                invoice_df = extract_invoice_data(extracted_text)

                if not invoice_df.empty:
                    st.subheader("Invoice Data:")
                    st.write(invoice_df)
                    
                    # Provide option to download the invoice as CSV
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

            # Split text into general text and table data for receipts
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
        
        else:
            st.warning("No text detected in the image. Please upload a valid image with text.")

# Calling the show function to run the app
if __name__ == "__main__":
    show()
