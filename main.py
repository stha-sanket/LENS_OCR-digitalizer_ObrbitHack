import streamlit as st
import easyocr
import numpy as np
from PIL import Image as PILImage
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Initialize the reader for OCR
reader = easyocr.Reader(['ne', 'en'])  # 'ne' for Nepali and 'en' for English

# Streamlit App
st.title("OCR with Image Processing")

st.write("Upload an image to extract text with OCR and download the result as PDF")

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Convert the uploaded image to a format OpenCV can work with
    image = PILImage.open(uploaded_file)
    img = np.array(image)

    # Display the uploaded image
    st.image(img, caption="Uploaded Image", use_column_width=True)

    # Perform OCR on the uploaded image
    output = reader.readtext(img)
    
    if output:
        # Prepare the extracted text
        extracted_text = "\n".join([result[1] for result in output])
        
        st.write(f'Total number of detections: {len(output)}')
        st.write("Extracted Text:")
        st.text_area("Recognized Text", extracted_text, height=300)

        # Create a PDF file with the recognized text
        pdf_filename = "recognized_text.pdf"
        pdf_buffer = BytesIO()

        # Create the PDF using reportlab
        c = canvas.Canvas(pdf_buffer, pagesize=letter)
        c.setFont("Helvetica", 10)

        # Write the extracted text into the PDF
        text_object = c.beginText(40, 750)  # Set initial position for text
        for line in extracted_text.splitlines():
            text_object.textLine(line)
        c.drawText(text_object)

        # Save the PDF
        c.showPage()
        c.save()

        # Go back to the beginning of the StringIO buffer
        pdf_buffer.seek(0)

        # Provide the PDF file as a download link
        st.download_button(
            label="Download PDF with Recognized Text",
            data=pdf_buffer,
            file_name=pdf_filename,
            mime="application/pdf"
        )
    else:
        st.write("No text detected in the image.")
