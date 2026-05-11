import streamlit as st
import PyPDF2
import docx
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -------------------------------
# Extract text
# -------------------------------
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

# -------------------------------
# Clean text
# -------------------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z ]', '', text)
    return text

# -------------------------------
# Better similarity (TF-IDF)
# -------------------------------
def calculate_match(resume, jd):
    tfidf = TfidfVectorizer()
    matrix = tfidf.fit_transform([resume, jd])
    similarity = cosine_similarity(matrix)[0][1]
    return round(similarity * 100, 2)

# -------------------------------
# Skill extraction
# -------------------------------
skills_list = [
    "python", "machine learning", "data analysis",
    "sql", "java", "deep learning", "excel",
    "communication", "teamwork"
]

def extract_skills(text):
    return [skill for skill in skills_list if skill in text]

# -------------------------------
# Suggestions Feature 🔥
# -------------------------------
def generate_suggestions(missing_skills, match):
    suggestions = []

    if match < 50:
        suggestions.append("Your resume is not aligned with the job. Consider rewriting it based on the job description.")

    if missing_skills:
        suggestions.append(f"Add these important skills: {', '.join(missing_skills)}")

    suggestions.append("Use strong action verbs (e.g., developed, built, optimized).")
    suggestions.append("Quantify your achievements (e.g., increased sales by 20%).")

    return suggestions

# -------------------------------
# UI
# -------------------------------
st.set_page_config(page_title="Resume Screener AI", layout="centered")

st.title("📄 Resume Screener AI (Advanced)")

uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])
jd = st.text_area("Paste Job Description")

if uploaded_file and jd:
    if uploaded_file.name.endswith(".pdf"):
        resume_text = extract_text_from_pdf(uploaded_file)
    else:
        resume_text = extract_text_from_docx(uploaded_file)

    resume_text = clean_text(resume_text)
    jd_clean = clean_text(jd)

    # Match %
    match = calculate_match(resume_text, jd_clean)

    st.subheader(f"✅ Match Score: {match}%")

    # Skills
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_clean)

    st.write("🧠 Skills in Resume:", resume_skills)

    missing_skills = list(set(jd_skills) - set(resume_skills))
    st.write("❌ Missing Skills:", missing_skills)

    # Suggestions
    st.subheader("💡 Suggestions to Improve Resume")
    suggestions = generate_suggestions(missing_skills, match)

    for s in suggestions:
        st.write("👉", s)

    # Progress bar 🔥
    st.progress(match / 100)
