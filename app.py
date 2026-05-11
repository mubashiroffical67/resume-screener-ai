import streamlit as st
import PyPDF2
import docx
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text
    return text

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z ]', '', text)
    return text

def calculate_match(resume, jd):
    cv = CountVectorizer()
    matrix = cv.fit_transform([resume, jd])
    similarity = cosine_similarity(matrix)[0][1]
    return round(similarity * 100, 2)

skills_list = ["python", "machine learning", "data analysis", "sql", "java"]

def extract_skills(text):
    found_skills = []
    for skill in skills_list:
        if skill in text:
            found_skills.append(skill)
    return found_skills

st.title("📄 Resume Screener AI")

uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])
jd = st.text_area("Paste Job Description")

if uploaded_file and jd:
    if uploaded_file.name.endswith(".pdf"):
        resume_text = extract_text_from_pdf(uploaded_file)
    else:
        resume_text = extract_text_from_docx(uploaded_file)

    resume_text = clean_text(resume_text)
    jd_clean = clean_text(jd)

    match = calculate_match(resume_text, jd_clean)
    st.subheader(f"✅ Match Percentage: {match}%")

    skills = extract_skills(resume_text)
    st.write("🧠 Skills Found:", skills)

    jd_skills = extract_skills(jd_clean)
    missing = list(set(jd_skills) - set(skills))
    st.write("❌ Missing Skills:", missing)
