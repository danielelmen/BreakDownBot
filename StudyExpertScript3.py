import streamlit as st
import fitz  # PyMuPDF
import google.generativeai as genai

# Hent brugere fra secrets
users = st.secrets["users"]

def login():
    """Simpel login-funktion."""
    st.title("Log ind")
    username = st.text_input("Brugernavn")
    password = st.text_input("Adgangskode", type="password")
    
    if st.button("Login"):
        if username in users and users[username] == password:
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.experimental_rerun()
        else:
            st.error("Forkert brugernavn eller adgangskode")

# Hvis ikke logget ind, vis login-skærm
if not st.session_state.get("authenticated", False):
    login()
    st.stop()


# Load API key securely
gemini_key = st.secrets["api_keys"]["gemini"]  # Ensure this matches the secrets file

#st.write("API Key Loaded Successfully!")  # Debugging

# Konfigurer Gemini API
genai.configure(api_key=gemini_key)  # Erstat med din rigtige API-nøgle

# Funktion til at læse systeminstruktion
def read_system_instruction():
    """Læser systeminstruktionen fra system_instruction.txt"""
    try:
        with open("system_instruction.txt", "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        return "Du er en hjælpsom AI, der opsummerer tekst."

# Funktion til at ekstrahere tekst fra PDF
def extract_text_from_pdf(pdf_file):
    """Extracts text from the uploaded PDF file."""
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = "\n".join([page.get_text("text") for page in doc])
    return text

# Funktion til at sende tekst til Gemini AI
def process_text_with_gemini(text):
    """Sender tekst til Gemini AI og returnerer en opsummering."""
    system_instruction = read_system_instruction()
    prompt = f"{system_instruction}\n\n{text}"
    
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    
    return response.text if response else "Ingen respons fra AI."

def main():
    st.title("PDF/Text Summarizer with AI")
    st.write("Upload en PDF-fil eller indsæt tekst, og få en AI-genereret opsummering.")

    uploaded_file = st.file_uploader("Vælg en PDF-fil", type="pdf")
    user_text = st.text_area("Eller indsæt/skrive tekst her", "")

    if st.button("Generer Opsummering"): 
        with st.spinner("AI analyserer teksten..."):
            if uploaded_file is not None:
                extracted_text = extract_text_from_pdf(uploaded_file)
            else:
                extracted_text = user_text
            
            ai_response = process_text_with_gemini(extracted_text)
            st.text_area("AI's Opsummering", ai_response, height=300)

if __name__ == "__main__":
    main()
