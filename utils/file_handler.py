# in utils/file_handler.py
import streamlit as st
import PyPDF2
import docx
import io

def read_file_content(uploaded_file):
    """Reads text content from a PDF or DOCX file."""
    try:
        if uploaded_file.type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
            text = "".join(page.extract_text() for page in pdf_reader.pages)
            return text
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = docx.Document(io.BytesIO(uploaded_file.read()))
            text = "\n".join(para.text for para in doc.paragraphs)
            return text
    except Exception as e:
        st.error(f"Error reading file: {e}")
        return None
    return ""