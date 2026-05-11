import streamlit as st
import PyPDF2
import docx
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# =========================================
# PAGE CONFIG
# =========================================
st.set_page_config(
    page_title="Resume Screener AI",
    layout="centered"
)

# =========================================
# EXTRACT TEXT FROM PDF
# =========================================
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""

    for page in pdf_reader.pages:
        extracted = page.extract_text()

        if extracted:
            text += extracted + "\n"

    return text

# =========================================
# EXTRACT TEXT FROM DOCX
# =========================================
def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = ""

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text

# =========================================
# CLEAN TEXT
# =========================================
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9 ]', ' ', text)
    return text

# =========================================
# MATCH SCORE
# =========================================
def calculate_match(resume, jd):
    tfidf = TfidfVectorizer()

    matrix = tfidf.fit_transform([resume, jd])

    similarity = cosine_similarity(matrix)[0][1]

    return round(similarity * 100, 2)

# =========================================
# SKILLS LIST
# =========================================
skills_list = [
    "python",
    "machine learning",
    "data analysis",
    "sql",
    "java",
    "deep learning",
    "excel",
    "communication",
    "teamwork",
    "html",
    "css",
    "javascript",
    "react",
    "nodejs",
    "streamlit",
    "pandas",
    "numpy"
]

# =========================================
# EXTRACT SKILLS
# =========================================
def extract_skills(text):
    found_skills = []

    for skill in skills_list:
        if skill.lower() in text.lower():
            found_skills.append(skill)

    return found_skills

# =========================================
# GENERATE SUGGESTIONS
# =========================================
def generate_suggestions(missing_skills, match):
    suggestions = []

    if match < 50:
        suggestions.append(
            "Your resume is not strongly aligned with the job description."
        )

    if missing_skills:
        suggestions.append(
            f"Add these important skills: {', '.join(missing_skills)}"
        )

    suggestions.append(
        "Use strong action verbs like developed, optimized, managed."
    )

    suggestions.append(
        "Add measurable achievements and project results."
    )

    return suggestions

# =========================================
# FORMAT ATS RESUME
# =========================================
def format_resume(text, skills):

    lines = text.split("\n")

    name = "Your Name"

    if len(lines) > 0:
        if lines[0].strip() != "":
            name = lines[0]

    ats_resume = f"""
# {name}

## PROFESSIONAL SUMMARY
Results-driven professional skilled in {', '.join(skills)}.

## SKILLS
{', '.join(skills)}

## EXPERIENCE
- Add your work experience
- Add achievements
- Add projects

## EDUCATION
- Add education details

## CERTIFICATIONS
- Add certifications
"""

    return ats_resume

# =========================================
# ATS CV GENERATOR
# =========================================
def generate_ats_cv(
    name,
    email,
    skills,
    experience,
    education
):

    cv = f"""
{name}
Email: {email}

------------------------------------
PROFESSIONAL SUMMARY
------------------------------------
Results-driven professional with expertise in {', '.join(skills)}.

------------------------------------
SKILLS
------------------------------------
{', '.join(skills)}

------------------------------------
EXPERIENCE
------------------------------------
{experience}

------------------------------------
EDUCATION
------------------------------------
{education}
"""

    return cv

# =========================================
# TITLE
# =========================================
st.title("📄 Resume Screener AI + ATS CV Generator")

# =========================================
# RESUME UPLOAD
# =========================================
uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf", "docx"]
)

jd = st.text_area("Paste Job Description")

# =========================================
# PROCESS RESUME
# =========================================
if uploaded_file and jd:

    # Extract Resume Text
    if uploaded_file.name.endswith(".pdf"):
        resume_text = extract_text_from_pdf(uploaded_file)

    else:
        resume_text = extract_text_from_docx(uploaded_file)

    # Clean Text
    cleaned_resume = clean_text(resume_text)
    cleaned_jd = clean_text(jd)

    # Match Score
    match = calculate_match(
        cleaned_resume,
        cleaned_jd
    )

    st.subheader(f"✅ Match Score: {match}%")

    # Skills
    resume_skills = extract_skills(cleaned_resume)

    jd_skills = extract_skills(cleaned_jd)

    missing_skills = list(
        set(jd_skills) - set(resume_skills)
    )

    # Show Skills
    st.subheader("🧠 Resume Skills")
    st.write(resume_skills)

    st.subheader("❌ Missing Skills")
    st.write(missing_skills)

    # Suggestions
    st.subheader("💡 Suggestions")

    suggestions = generate_suggestions(
        missing_skills,
        match
    )

    for suggestion in suggestions:
        st.write("👉", suggestion)

    # Progress Bar
    st.progress(match / 100)

    # ATS Resume Preview
    st.subheader("📑 ATS Resume Preview")

    ats_resume = format_resume(
        resume_text,
        resume_skills
    )

    st.markdown(ats_resume)

    # Download ATS Resume
    st.download_button(
        label="⬇ Download ATS Resume",
        data=ats_resume,
        file_name="ATS_Resume.txt",
        mime="text/plain"
    )

# =========================================
# DIVIDER
# =========================================
st.divider()

# =========================================
# ATS CV GENERATOR UI
# =========================================
st.header("📄 Generate ATS-Friendly CV")

name = st.text_input("Your Name")

email = st.text_input("Your Email")

skills_input = st.text_input(
    "Skills (comma separated)"
)

experience = st.text_area("Experience")

education = st.text_area("Education")

# =========================================
# GENERATE BUTTON
# =========================================
if st.button("Generate ATS CV"):

    skills = [
        s.strip()
        for s in skills_input.split(",")
        if s.strip() != ""
    ]

    ats_cv = generate_ats_cv(
        name,
        email,
        skills,
        experience,
        education
    )

    st.subheader("✅ Your ATS-Friendly CV")

    st.text_area(
        "CV Output",
        ats_cv,
        height=350
    )

    # Download CV
    st.download_button(
        label="📥 Download CV",
        data=ats_cv,
        file_name="ATS_CV.txt",
        mime="text/plain"
    )
