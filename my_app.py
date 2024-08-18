import streamlit as st
import fitz  # PyMuPDF
import requests

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_file):
    pdf_text = ""
    with fitz.open(stream=pdf_file, filetype="pdf") as doc:
        for page in doc:
            pdf_text += page.get_text()
    return pdf_text

# Function to send a question to the Hugging Face API
def ask_question_to_huggingface(api_key, question, context):
    url = 'https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B'  # Replace with the actual API endpoint
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }
    data = {
        'inputs': {
            'question': question,
            'context': context
        }
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': response.text}

# Streamlit app
st.title('PDF Question Answering with Hugging Face')

# Upload PDF file
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    # Extract text from the uploaded PDF
    pdf_text = extract_text_from_pdf(uploaded_file)

    st.write("Text extracted from PDF:")
    st.text_area("Extracted Text", pdf_text, height=300)

    # Input API key for Hugging Face
    api_key = st.text_input("Enter your Hugging Face API key", type="password")

    if api_key:
        question = st.text_input("Ask a question related to the PDF content")

        if st.button('Get Answer'):
            if not question:
                st.error("Please enter a question.")
            else:
                with st.spinner('Getting answer from Hugging Face API...'):
                    result = ask_question_to_huggingface(api_key, question, pdf_text)
                    st.write("Hugging Face API Response:")
                    st.json(result)
