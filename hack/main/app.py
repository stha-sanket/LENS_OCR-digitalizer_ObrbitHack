import streamlit as st

# Set page config
st.set_page_config(page_title="LENS-OCR", page_icon="🔍")

# Import the necessary modules for different functionalities
# Ensure that these modules exist and have a 'show' function
import gem
import nepaliocr
import invoice
import contact
import text2

# Custom CSS for styling the footer
st.markdown("""
    <style>
    .footer {
        padding: 20px;
        text-align: center;
    }
    .footer img {
        width: 70px;
        display: block;
        margin: 0 auto 10px;
    }
    .footer .footer-content {
        max-width: 800px;
        margin: 0 auto;
    }
    .footer .footer-left {
        margin: 10px 0;
    }
    .footer .footer-left h3 {
        font-size: 1.5rem;
        margin: 10px 0;
    }
    .footer .footer-left p {
        font-size: 1rem;
        margin: 10px 0;
    }
    .footer .footer-bottom {
        margin-top: 20px;
        font-size: 0.9rem;
        text-align: center;
    }
    .footer .horizontal-line {
        border: 0.5px solid white;
        margin: 20px 0;
    }
    @media (max-width: 768px) {
        .footer .footer-left h3 {
            font-size: 1.2rem;
        }
        .footer .footer-left p {
            font-size: 0.9rem;
        }
        .footer .footer-bottom {
            font-size: 0.8rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# JavaScript for smooth scrolling and sidebar behavior
st.markdown("""
    <script>
    function scrollToTop() {
        window.scrollTo(0, 0);
    }
    </script>
""", unsafe_allow_html=True)

# Initialize session state for page tracking
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"
    st.session_state.sidebar_state = 'collapsed'

# Sidebar for navigation
with st.sidebar:
    st.title("LENS OCR")
    
    # Navigation buttons for different pages
    if st.button("🏠 Home"):
        st.session_state.current_page = "Home"
        st.session_state.sidebar_state = 'collapsed'
    
    if st.button("ℹ️ Document Digitilizer"):
        st.session_state.current_page = "Document extractor"
        st.session_state.sidebar_state = 'collapsed'
    
    if st.button("🤖 ChatPDF"):
        st.session_state.current_page = "ChatPDF"
        st.session_state.sidebar_state = 'collapsed'
    
    if st.button("🎧 Text-Audio"):
        st.session_state.current_page = "Text-Audio"
        st.session_state.sidebar_state = 'collapsed'
    
    if st.button("📄 Document"):
        st.session_state.current_page = "Invoice"
        st.session_state.sidebar_state = 'collapsed'
    
    if st.button("📞 Contact"):
        st.session_state.current_page = "Contact"
        st.session_state.sidebar_state = 'collapsed'

# Main content area
main_content = st.container()

# Handle page rendering based on the session state
with main_content:
    if st.session_state.current_page == "Home":
        st.title("Welcome to LENS")
        st.write("\n")
        st.write("Lens is a platform that uses AI and OCR technology to turn Nepali documents into digital text, making them easy to edit and print. It also lets you save receipts and invoices for easy access. Other features include a Chat with PDF option, where you can ask questions about your PDF documents, and a Text-to-Speech tool, which reads text aloud and helps with translations.")
        st.write("\n")
        st.write("\n")
        st.write("\n")
        
        st.header("Our Services")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("📄 Document Digitization")
            st.write("Our platform uses AI and OCR to digitize Nepali documents, making them easy to edit and print.")

        with col2:
            st.success("💼 Invoice & Receipt Storage")
            st.write("Easily save and manage your receipts and invoices for quick access and organization.")

        with col3:
            st.warning("🤖 AI-Powered Features")
            st.write("Explore our advanced features like Chat with PDF and Text-to-Speech translation for enhanced accessibility.")
            
        st.write("\n")

    elif st.session_state.current_page == "Document extractor":
        nepaliocr.show()  # Make sure nepaliocr.show() is implemented correctly

    elif st.session_state.current_page == "ChatPDF":
        gem.show()  # Make sure gem.show() is implemented correctly

    elif st.session_state.current_page == "Text-Audio":
        text2.show()  # Make sure text2.show() is implemented correctly

    elif st.session_state.current_page == "Invoice":
        invoice.show()  # Make sure invoice.show() is implemented correctly

    elif st.session_state.current_page == "Contact":
        contact.show()  # Make sure contact.show() is implemented correctly

    else:
        st.write(f"Page '{st.session_state.current_page}' is not recognized.")

# Footer with company details
st.markdown("""
    <div class="footer">
        <div class="footer-content">
            <div class="footer-left">
                <br>
                <br>
                <br>
                <h3>Transforming Documents in Digital Fashion</h3>
                <p>Lens uses AI and OCR to digitize your Nepali documents, making them easy to edit, print, and store. From receipts to invoices, we help you streamline your digital workflow. Start simplifying your document management today.</p>
            </div>
        </div>
        <hr class="horizontal-line">
        <div class="footer-bottom">
            &copy; 2024 Lens Technologies. All Rights Reserved.
        </div>
    </div>
""", unsafe_allow_html=True)

# JavaScript to scroll to top when page changes
st.markdown('<script>scrollToTop();</script>', unsafe_allow_html=True)

# Set sidebar state with JavaScript
st.sidebar.markdown(f"""
    <script>
        var sidebar = window.parent.document.querySelector('[data-testid="stSidebar"]');
        sidebar.setAttribute('data-collapsed', '{st.session_state.sidebar_state}');
    </script>
""", unsafe_allow_html=True)
