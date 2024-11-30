# Lens - AI-powered Nepali Document Digitization and Interaction Platform

Lens is a platform that uses **AI** and **OCR** technology to digitize **Nepali documents**, enable **editing and printing**, and save **receipts** and **invoices**. With features like **"Chat with PDF"**, users can query and interact with the document content, and the **Text-to-Speech** tool allows for reading and translations.

## Features

- **PDF Upload & Management**: Upload Nepali PDF documents and have them processed.
- **Text Extraction**: Extracts text from Nepali PDFs for further querying and manipulation.
- **AI-Powered Chat**: Ask questions about the document content, powered by Google's **Generative AI (Gemini)**.
- **Text-to-Speech**: Listen to the text extracted from PDFs using **Text-to-Speech** technology.
- **Editable Content**: Modify and interact with the content of scanned documents.
- **OCR**: Digitize scanned Nepali receipts and invoices for easy access and management.

## Architecture

The **Lens** platform consists of the following main components:

1. **Frontend (Streamlit UI/UX)**: Provides an intuitive interface for users to upload PDFs, ask questions, and interact with the document.
2. **Backend (Text Extraction, AI, and Storage)**: Handles the PDF text extraction (using **PyMuPDF**), processes user questions using the **Generative AI Model** (Google Gemini), and stores data for faster access.
3. **Text-to-Speech Module**: Converts the extracted text to speech for a hands-free experience.
4. **User Interaction Logging**: Logs user interactions with the platform for analysis and improvements.

## System Architecture

```plaintext
+------------------+             +---------------------------+       +-------------------------------+
|   User Device    |   --->      |   Frontend (Streamlit)     |   ---> |   Backend (Server/Cloud)      |
|  (Web Browser)   |             |   (UI/UX Interface)        |       |   (AI Models, PDF Processor)  |
+------------------+             +---------------------------+       +-------------------------------+
                                              |                                     |
                                              |                                     |
                                              v                                     v
                          +--------------------------------+       +-------------------------------+
                          |    PDF Upload & Management    |       |    Text Extraction Module     |
                          |    (File upload, storage)     |       |   (PyMuPDF)                   |
                          +--------------------------------+       +-------------------------------+
                                              |                                     |
                                              v                                     v
                          +--------------------------------+       +-------------------------------+
                          |   Text-to-Speech Module        |       |   Generative AI Model (Gemini)|
                          |   (Convert text to speech)    |       |   (Question answering, chat)  |
                          +--------------------------------+       +-------------------------------+
                                              |                                     |
                                              v                                     v
                          +--------------------------------+       +-------------------------------+
                          |  Text Storage & Caching       |       |   Response Generation         |
                          |  (Cache extracted text)       |       |   (Process responses)         |
                          +--------------------------------+       +-------------------------------+
                                              |
                                              v
                          +--------------------------------+
                          |   User Interaction Logging    |
                          |   (Store user questions &    |
                          |    interactions)             |
                          +--------------------------------+
