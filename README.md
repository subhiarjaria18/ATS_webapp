# Resume Evaluator - Optimize Your Resume for ATS

Resume Evaluator is a web application designed to help you optimize your resume for Applicant Tracking Systems (ATS). By analyzing your resume against a given job description, the app provides a percentage match, highlights missing keywords, and offers a detailed summary of your resume's strengths and areas for improvement.

## Features

- Analyze your resume against a job description.
- Get a percentage match score.
- Identify missing keywords.
- Receive a detailed summary and evaluation of your resume.

## Tech Stack

- **Python**: Backend logic.
- **Streamlit**: Frontend framework.
- **google-generativeai**: Integration with Google Generative AI models.
- **python-dotenv**: Management of environment variables.
- **docx2txt**: Extraction of text from DOCX files.
- **PyPDF2**: Extraction of text from PDF files.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/subhiarjaria18/resume-evaluator.git
    cd resume-evaluator
    ```

2. **Create a virtual environment and activate it**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:
    Create a `.env` file in the root directory and add your environment variables:
    ```env
    GOOGLE_API_KEY=your_google_api_key
    ```

## Usage

1. **Run the Streamlit app**:
    ```bash
    streamlit run app.py
    ```

2. **Visit the Web App**:
    - Streamlit: [ATS Web App](https://atswebapp-htghaztmncebuadgq2c5nc.streamlit.app/)
    - Hugging Face: [ATS Web App on Hugging Face](https://huggingface.co/spaces/Subhi09/ATS_webapp)

3. **Upload your resume and job description**:
    - Use the provided interface to upload your resume (PDF or DOCX format).
    - Paste the job description in the designated area.
    - Click "Submit" to receive the analysis.



