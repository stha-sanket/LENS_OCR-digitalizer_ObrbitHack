import PyPDF2
from gtts import gTTS
import streamlit as st
import time

def show():
    """
    Streamlit app that allows users to upload a PDF, extracts the text from it,
    and converts the extracted text to speech.
    """
    
    # Function to extract text from the PDF file
    def extract_text_from_pdf(pdf_file):
        """
        This function extracts the text content from the provided PDF using PyPDF2.
        It reads each page of the PDF and concatenates the text into one string.
        """
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        # Loop through all the pages of the PDF and extract text
        for page in reader.pages:
            text += page.extract_text()  # Add text from each page
        return text

    # Function to convert extracted text to speech using gTTS
    def text_to_speech(text, output_path="output.mp3", language='en', slow=False):
        """
        This function takes the extracted text and converts it to speech using gTTS (Google Text-to-Speech).
        It saves the speech to an MP3 file, which can be played back by the user.
        """
        tts = gTTS(text, lang=language, slow=slow)  # Create gTTS object with chosen language and speed
        tts.save(output_path)  # Save the generated speech as an MP3 file
        return output_path  # Return the path of the saved MP3 file

    # Streamlit Interface Setup

    st.title("📄 PDF to Speech Converter 🎙️")
    st.write("""
        **Welcome to the PDF to Speech Converter!**  
        Upload a PDF file, extract its text, and convert it into speech with just a few clicks.
    """)

    # File upload widget
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        # Extract text from the uploaded PDF
        st.write("Processing the uploaded file...")
        text = extract_text_from_pdf(uploaded_file)
        
        if text.strip():  # Check if text is extracted successfully
            st.write("Text extracted successfully!")
            st.text_area("Extracted Text", text, height=200)  # Display extracted text for user verification

            # Options to customize the speech
            language = st.selectbox("Choose language for speech", options=["en", "es", "fr", "de", "it", "ne"])
            slow = st.checkbox("Speak Slowly?", value=False)

            # Progress Bar for Text-to-Speech Conversion
            st.write("Converting text to speech... Please wait!")
            progress_bar = st.progress(0)  # Initialize progress bar at 0%
            time.sleep(1)  # Give the user a moment before starting the conversion (simulate loading)

            # Start the conversion in chunks (simulate progress)
            for i in range(1, 101):
                time.sleep(0.03)  # Simulate the time it takes to convert text
                progress_bar.progress(i)  # Update progress bar

            # Once the progress reaches 100%, convert the text to speech
            audio_path = text_to_speech(text, language=language, slow=slow)

            # Display audio player for the user to listen to the converted speech
            st.audio(audio_path, format="audio/mp3")

            # Provide a download link for the audio file (MP3)
            st.download_button(
                label="Download Audio",
                data=open(audio_path, "rb").read(),
                file_name="converted_speech.mp3",
                mime="audio/mp3"
            )

            # Final success message
            st.success("Speech conversion completed successfully!")

        else:
            st.error("No extractable text found in the PDF. Please upload a valid document with readable text.")
