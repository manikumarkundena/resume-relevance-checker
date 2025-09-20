import streamlit as st
import google.generativeai as genai
import json
import os

def get_relevance_score(resume_text, jd_text):
    """Calls Google Gemini API for a standard analysis."""
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        st.error("Google API key is not configured. Please check your .env file.")
        return None

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')

    prompt = f"""
    Analyze the following resume and job description. Provide a detailed analysis in a strict JSON format.
    The JSON object must have these exact keys: "score", "summary", "strengths", "weaknesses", "keywords_matched".

    - "score": An integer from 0 to 100 representing the relevance of the resume to the job.
    - "summary": A 2-3 sentence professional summary of why the candidate is a good or bad fit.
    - "strengths": A python list of 3-4 key skills or experiences from the resume that align with the job description.
    - "weaknesses": A python list of 2-3 key skills or requirements from the job description missing from the resume.
    - "keywords_matched": A python list of important keywords found in both the resume and the job description.

    Resume:
    ---
    {resume_text}
    ---

    Job Description:
    ---
    {jd_text}
    ---

    Provide only the JSON object as a response, with no other text before or after it.
    """
    try:
        response = model.generate_content(prompt)
        json_text = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(json_text)
    except Exception as e:
        st.error(f"An error occurred with the Gemini AI model: {e}")
        return None