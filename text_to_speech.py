import PyPDF2
from gtts import gTTS
import streamlit as st

# Function to extract text from the PDF file
def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Function to convert extracted text to speech
def text_to_speech(text, output_path="output.mp3"):
    # Create a gTTS object
    tts = gTTS(text, lang='en', slow=False)
    
    # Save the speech to an audio file
    tts.save(output_path)
    return output_path

# Streamlit Interface
def main():
    st.title("PDF to Speech Converter")
    st.write("Upload a PDF file, and we'll extract the text and convert it into speech.")

    # File upload widget
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        # Extract text from the uploaded PDF
        st.write("Processing the uploaded file...")
        text = extract_text_from_pdf(uploaded_file)
        
        if text.strip():  # Check if text is not empty
            st.write("Text extracted successfully!")
            st.text_area("Extracted Text", text, height=200)
            
            if st.button("Convert to Speech"):
                st.write("Converting text to speech...")
                audio_path = text_to_speech(text)
                st.audio(audio_path, format="audio/mp3")
                st.success("Speech conversion completed!")
        else:
            st.error("No extractable text found in the PDF.")

if __name__ == "__main__":
    main()


