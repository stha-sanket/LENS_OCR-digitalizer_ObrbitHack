import streamlit as st
import fitz  # PyMuPDF for PDF processing
import os
import google.generativeai as genai  # Google's Generative AI library

# Configure the Google Generative AI API
os.environ["GEMINI_API_KEY"] = "AIzaSyDT_4vfd1vqa0ZIXMkdsDUsYBqJU1NV_Hg"
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Generation configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 200,
    "response_mime_type": "text/plain",
}

# Model configuration
model = genai.GenerativeModel(
    model_name="gemini-exp-1114",
    generation_config=generation_config,
)

# Title and description of the app
st.title("PDF-Based Chatbot with Google Gemini API")
st.write("Upload a PDF, ask a question, and get AI-powered answers based on the PDF content!")

# PDF file upload
uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"])

@st.cache_data
def extract_text_from_pdf(file):
    """Extracts text from the uploaded PDF using PyMuPDF."""
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as pdf:
        for page in pdf:
            text += page.get_text()
    return text

def chat_with_bot(pdf_text, question):
    """Send the PDF content and question to the generative AI model and get the answer."""
    full_prompt = f"Context from the PDF:\n{pdf_text}\n\nQuestion: {question}"
    
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(full_prompt)
    return response.text  # Return the plain response text

if uploaded_file:
    # Extract text from the PDF
    pdf_text = extract_text_from_pdf(uploaded_file)
    st.success("PDF uploaded and text extracted successfully!")

    # Show a preview of the extracted text (first 500 characters)
    st.write("Extracted Text Preview:")
    st.text_area("PDF Text (First 500 characters):", pdf_text[:500], height=200)

    # Input field for the user to ask a question
    question = st.text_input("Ask a question about the PDF:")

    if question:
        with st.spinner("Finding the answer..."):
            try:
                # Get the answer from the chatbot
                answer = chat_with_bot(pdf_text, question)
                st.write(f"**Answer:** {answer}")
            except Exception as e:
                st.error(f"Error querying the model: {e}")
