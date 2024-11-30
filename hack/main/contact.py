import streamlit as st
import requests

def show():
    # Custom CSS for styling
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

    # Header section
    st.title("Contact Us - Lens OCR")
    st.subheader("Transforming Your Documents into Digital Text with AI")

    # Introduction text
    st.markdown("""
    Have a question or need assistance with using Lens OCR? Whether you want to learn more about our document digitization services or need help with the platform, feel free to reach out to us! We’re here to help you with all your document management needs.
    """)

    # Initialize session state variables
    if 'form_submitted' not in st.session_state:
        st.session_state.form_submitted = False

    # Check if the form was just submitted
    if st.session_state.form_submitted:
        st.success("Thank you for your message! Our team will get back to you shortly.")
        # Reset the form_submitted state
        st.session_state.form_submitted = False
    
    # Contact form
    with st.form(key='contact_form'):
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        subject = st.text_input("Subject")
        message = st.text_area("Message")

        # Submit button
        submit_button = st.form_submit_button(label='Submit')
        
    if submit_button:
        if not name or not email or not message:
            st.error("Please fill out all fields.")
        else:
            form_data = {
                'name': name,
                'email': email,
                'subject': subject,
                'message': message
            }
            # Submit form data to Formspree endpoint (replace with your own endpoint if needed)
            response = requests.post('https://formspree.io/f/mpwawqyr', data=form_data)

            if response.status_code == 200:
                st.session_state.form_submitted = True
                # Rerun the app to show the success message and clear the form
                st.experimental_rerun()
            else:
                st.error("Oops! Something went wrong. Please try again later.")

    # Footer Section
    st.markdown("""
    <div class="footer">
        <div class="footer-content">
            <div class="footer-left">
                <br>
                <br>
                <br>
                <h3>Transforming Documents into Digital Fashion</h3>
                <p>LENS uses AI and OCR to digitize your Nepali documents, making them easy to edit, print, and store. From receipts to invoices, we help you streamline your digital workflow. Start simplifying your document management today.</p>
            </div>
        </div>
        <hr class="horizontal-line">
        <div class="footer-bottom">
            &copy; 2024 Lens Technologies. All Rights Reserved.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # JavaScript to scroll to top after form submission
    st.markdown('<script>scrollToTop();</script>', unsafe_allow_html=True)

# Run the show function to display the contact form
if __name__ == '__main__':
    show()
