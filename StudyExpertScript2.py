#Takes a pdf and extracts text and sends it to gemini that analyses it

import streamlit as st
import fitz  # PyMuPDF
import google.generativeai as genai

# Konfigurer Gemini API
genai.configure(api_key="AIzaSyB6co8hZEZp52yvW-_NWD4zW6L7H1yZmgA")  # Erstat med din rigtige API-nøgle

# Funktion til at læse systeminstruktion
def read_system_instruction():
    """Læser systeminstruktionen fra system_instruction.txt"""
    try:
        with open("system_instruction.txt", "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        return "Du er en hjælpsom AI, kort sammenfatter det vigtigste fra en tekst."

# Funktion til at ekstrahere tekst fra PDF
def extract_text_from_pdf(pdf_file):
    """Extracts text from the uploaded PDF file."""
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = "\n".join([page.get_text("text") for page in doc])
    return text

# Funktion til at sende tekst til Gemini AI
def process_text_with_gemini(text):
    """Sender tekst til Gemini AI og returnerer svaret."""
    system_instruction = read_system_instruction()
    prompt = f"{system_instruction}\n\n{text}"
    
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    
    return response.text if response else "Ingen respons fra AI."

def main():
    st.title("PDF to Text Extractor with AI")
    st.write("Upload en PDF-fil, og få den ekstraherede tekst analyseret af Gemini AI.")

    uploaded_file = st.file_uploader("Vælg en PDF-fil", type="pdf")

    if uploaded_file is not None:
        st.success("Fil uploadet succesfuldt!")

        # Ekstraher tekst fra PDF
        extracted_text = extract_text_from_pdf(uploaded_file)
        st.text_area("Ekstraheret Tekst", extracted_text, height=300)

        # Send tekst til AI-behandling
        if st.button("Analyser Tekst med AI"):
            with st.spinner("AI analyserer teksten..."):
                ai_response = process_text_with_gemini(extracted_text)
                st.text_area("AI's Svar", ai_response, height=300)

        # Download mulighed for den ekstraherede tekst
        txt_filename = uploaded_file.name.replace(".pdf", ".txt")
        st.download_button(
            label="Download Ekstraheret Tekst",
            data=extracted_text,
            file_name=txt_filename,
            mime="text/plain"
        )

if __name__ == "__main__":
    main()
