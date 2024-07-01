import streamlit as st
import google.generativeai as genai
import os
import docx2txt
import PyPDF2 as pdf
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Configure the generative AI model with the Google API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Set up the model configuration for text generation
generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

# Define safety settings for content generation
safety_settings = [
    {"category": f"HARM_CATEGORY_{category}", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
    for category in ["HARASSMENT", "HATE_SPEECH", "SEXUALLY_EXPLICIT", "DANGEROUS_CONTENT"]
]

def generate_response_from_gemini(input_text):
    # Create a GenerativeModel instance with 'gemini-pro' as the model type
    llm = genai.GenerativeModel(
        model_name="gemini-pro",
        generation_config=generation_config,
        safety_settings=safety_settings,
    )
    # Generate content based on the input text
    output = llm.generate_content(input_text)
    # Return the generated text
    return output.text

def extract_text_from_pdf_file(uploaded_file):
    # Use PdfReader to read the text content from a PDF file
    pdf_reader = pdf.PdfReader(uploaded_file)
    text_content = ""
    for page in pdf_reader.pages:
        text_content += str(page.extract_text())
    return text_content

def extract_text_from_docx_file(uploaded_file):
    # Use docx2txt to extract text from a DOCX file
    return docx2txt.process(uploaded_file)

# Prompt Template
input_prompt_template = """
As an experienced Applicant Tracking System (ATS) analyst,
with profound knowledge in technology, software engineering, data science, 
and big data engineering, your role involves evaluating resumes against job descriptions.
Recognizing the competitive job market, provide top-notch assistance for resume improvement.
Your goal is to analyze the resume against the given job description, 
assign a percentage match based on key criteria, and pinpoint missing keywords accurately.
resume:{text}
description:{job_description}
I want the response in one single string having the structure
{{"Job Description Match":"%","Missing Keywords":"","Candidate Summary":"","Experience":""}}
"""

# Streamlit app
# Initialize Streamlit app
st.set_page_config(page_title="Resume Evaluator", page_icon="📝", layout="wide")

# Custom CSS for enhanced UI
st.markdown("""
    <style>
        body {
            background-color: #1a1a1a;
            color: #f0f0f0;
        }
        .main {
            background-color: #1a1a1a;
            color: #f0f0f0;
        }
        .stButton button {
            background-color: #00509e;
            color: white;
            border-radius: 5px;
            width: 100%;
            font-size: 16px;
            padding: 10px;
        }
        .stButton button:hover {
            background-color: #003d73;
        }
        .stTextInput textarea, .stTextInput input {
            border-radius: 5px;
            border: 1px solid #00509e;
            background-color: #333333;
            color: #f0f0f0;
        }
        .stFileUploader label {
            color: #007bff;
        }
        .header {
            font-size: 32px;
            color: #f0f0f0;
            text-align: center;
        }
        .subheader {
            font-size: 24px;
            color: #cccccc;
            text-align: center;
            margin-bottom: 20px;
        }
        .result-header {
            font-size: 28px;
            color: #f0f0f0;
            margin-top: 20px;
        }
        .result-text {
            color: #f0f0f0;
            font-size: 16px;
            margin-top: 10px;
        }
        .strong-match {
            font-size: 20px;
            color: #dc3545;
            margin-top: 10px;
        }
        .considerable-fit {
            font-size: 20px;
            color: #ffc107;
            margin-top: 10px;
        }
        .potential-fit {
            font-size: 20px;
            color: #28a745;
            margin-top: 10px;
        }
        .limited-alignment {
            font-size: 20px;
            color: #6c757d;
            margin-top: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="header">Resume Evaluator - Optimize Your Resume for ATS</h1>', unsafe_allow_html=True)

st.markdown('<h2 class="subheader">Job Description</h2>', unsafe_allow_html=True)
job_description = st.text_area("Paste the Job Description", height=200)

st.markdown('<h2 class="subheader">Upload Your Resume</h2>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload Your Resume", type=["pdf", "docx"], help="Please upload a PDF or DOCX file")

submit_button = st.button("Submit")

if submit_button:
    if uploaded_file is not None:
        with st.spinner('Processing your resume...'):
            if uploaded_file.type == "application/pdf":
                resume_text = extract_text_from_pdf_file(uploaded_file)
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                resume_text = extract_text_from_docx_file(uploaded_file)
            response_text = generate_response_from_gemini(input_prompt_template.format(text=resume_text, job_description=job_description))

            # Extract Job Description Match percentage from the response
            match_percentage_str = response_text.split('"Job Description Match":"')[1].split('"')[0]

            # Remove percentage symbol and convert to float
            match_percentage = float(match_percentage_str.rstrip('%'))

            st.markdown('<h2 class="result-header">ATS Evaluation Result:</h2>', unsafe_allow_html=True)
            st.markdown(f'<div class="result-text">{response_text}</div>', unsafe_allow_html=True)

            # Provide descriptive feedback based on match percentage
            if match_percentage >= 90:
                st.markdown('<p class="strong-match">Strong Match - Highly Recommended for Consideration</p>', unsafe_allow_html=True)
            elif match_percentage >= 80:
                st.markdown('<p class="considerable-fit">Considerable Fit - Strong Candidate</p>', unsafe_allow_html=True)
            elif match_percentage >= 70:
                st.markdown('<p class="potential-fit">Potential Fit - Good Candidate</p>', unsafe_allow_html=True)
            else:
                st.markdown('<p class="limited-alignment">Limited Alignment - Review Required</p>', unsafe_allow_html=True)
    else:
        st.error("Please upload your resume to proceed.")
