import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image
from PyPDF2 import PdfReader
import json

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(prompt):
    
    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

    response = model.generate_content(prompt)
    return response.text  

def input_pdf_text(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Prompt template
prompt_template = """
Hey, act like a skilled ATS (Application Tracking System)
with expertise in tech roles: software engineer, data scientist, ML engineer, MLOps, generative AI, big data.
Evaluate the resume below against the job description and provide:
1. Percentage match
2. Missing keywords
3. Profile summary
Resume: {text}
Job Description: {jd}

Respond in JSON format like:
{{"JD Mtch":"%","MissingKeywords": [],"Profile Summary":""}}
"""

# Streamlit UI
st.title("Smart ATS")
st.write("Upload your resume and paste the job description to get ATS analysis.")

jd = st.text_area("Paste Job Description")
uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")

if st.button("Submit"):
    if uploaded_file is not None and jd:
        text = input_pdf_text(uploaded_file)
        final_prompt = prompt_template.format(text=text, jd=jd)
        response = get_gemini_response(final_prompt)

        st.subheader("ATS Evaluation")
        try:
            st.json(json.loads(response))
        except:
            st.write(response)
    else:
        st.warning("Please upload a resume and paste a job description.")
