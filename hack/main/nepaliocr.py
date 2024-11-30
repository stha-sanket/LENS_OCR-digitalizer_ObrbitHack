import streamlit as st
import easyocr
import numpy as np
from PIL import Image as PILImage
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def show():
    # Initialize EasyOCR reader for Nepali and English
    reader = easyocr.Reader(['ne', 'en'])  # 'ne' for Nepali, 'en' for English 

    # Streamlit App UI with improved flow
    st.title("📝 Turn Your images Into Digital Text")
    st.markdown("Upload an image to extract text with OCR and download the result as a PDF.")

    st.subheader("How it works:")
    st.write(
        """
        1. Upload an image containing text.
        2. The OCR engine will analyze the text in the image.
        3. The recognized text will be displayed, and you can download it as a PDF.
        """
    )

    # Image Upload Section
    uploaded_file = st.file_uploader("📤 Choose an image (JPG, PNG, JPEG)", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        # Convert the uploaded image to a format OpenCV can work with
        image = PILImage.open(uploaded_file)
        img = np.array(image)

        # Display the uploaded image with a caption
        st.image(img, caption="Uploaded Image", use_container_width=True)

        # OCR Processing
        st.markdown("### Processing...")
        with st.spinner("Extracting text from your image... Please wait!"):
            output = reader.readtext(img)

        # Displaying Results
        if output:
            # Prepare the extracted text
            extracted_text = "\n".join([result[1] for result in output])

            # Display number of detections and extracted text
            st.success(f"✔️ {len(output)} text elements detected!")
            st.subheader("Extracted Text:")
            st.text_area("Recognized Text", extracted_text, height=300)

            # Create a PDF with the recognized text
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
            st.markdown("### Download Your Extracted Text PDF")
            st.download_button(
                label="Download PDF with Recognized Text 📥",
                data=pdf_buffer,
                file_name=pdf_filename,
                mime="application/pdf"
            )
        else:
            st.warning("⚠️ No text detected in the image. Please try again with a clearer image.")

