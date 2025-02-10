import streamlit as st
import fitz  # PyMuPDF
import os

def extract_text_from_pdf(pdf_file):
    """Extracts text from the uploaded PDF file."""
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = "\n".join([page.get_text("text") for page in doc])
    return text

def main():
    st.title("PDF to Text Extractor")
    st.write("Upload a PDF file, and the extracted text will be saved as a .txt file.")

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        st.success("File uploaded successfully!")
        
        # Extract text from PDF
        extracted_text = extract_text_from_pdf(uploaded_file)

        # Display extracted text in a text area
        st.text_area("Extracted Text", extracted_text, height=300)

        # Provide an option to download the extracted text
        txt_filename = uploaded_file.name.replace(".pdf", ".txt")
        st.download_button(
            label="Download Extracted Text",
            data=extracted_text,
            file_name=txt_filename,
            mime="text/plain"
        )

if __name__ == "__main__":
    main()
