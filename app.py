import streamlit as st
import PyPDF2
import docx
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Advanced Resume Screener AI",
    layout="centered"
)

# =========================================================
# EXTRACT TEXT FROM PDF
# =========================================================
def extract_text_from_pdf(file):
    text = ""

    pdf_reader = PyPDF2.PdfReader(file)

    for page in pdf_reader.pages:
        extracted = page.extract_text()

        if extracted:
            text += extracted + "\n"

    return text

# =========================================================
# EXTRACT TEXT FROM DOCX
# =========================================================
def extract_text_from_docx(file):
    doc = docx.Document(file)

    text = ""

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text

# =========================================================
# CLEAN TEXT
# =========================================================
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9+#.\s]', ' ', text)
    return text

# =========================================================
# CALCULATE ATS MATCH
# =========================================================
def calculate_match(resume, jd):

    tfidf = TfidfVectorizer(stop_words='english')

    matrix = tfidf.fit_transform([resume, jd])

    similarity = cosine_similarity(matrix)[0][1]

    return round(similarity * 100, 2)

# =========================================================
# LARGE SKILLS DATABASE
# =========================================================
skills_database = [

    # Programming
    "python", "java", "c++", "c", "javascript",
    "typescript", "php", "ruby", "swift", "kotlin",

    # Web
    "html", "css", "react", "nextjs", "nodejs",
    "express", "tailwind", "bootstrap",

    # AI / ML
    "machine learning", "deep learning",
    "tensorflow", "pytorch", "opencv",
    "nlp", "computer vision",

    # Data
    "sql", "mysql", "postgresql",
    "mongodb", "pandas", "numpy",
    "excel", "power bi", "tableau",

    # Cloud
    "aws", "azure", "gcp", "docker",
    "kubernetes", "firebase",

    # Soft Skills
    "communication", "leadership",
    "teamwork", "problem solving",
    "critical thinking",

    # Tools
    "git", "github", "streamlit",
    "linux", "figma"
]

# =========================================================
# IMPROVED SKILL EXTRACTION
# =========================================================
def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in skills_database:

        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, text):
            found_skills.append(skill)

    return sorted(list(set(found_skills)))

# =========================================================
# EXTRACT EMAIL
# =========================================================
def extract_email(text):

    match = re.search(
        r'[\w\.-]+@[\w\.-]+',
        text
    )

    if match:
        return match.group(0)

    return "your.email@example.com"

# =========================================================
# EXTRACT PHONE
# =========================================================
def extract_phone(text):

    match = re.search(
        r'(\+?\d[\d\s\-]{8,15})',
        text
    )

    if match:
        return match.group(0)

    return "Your Phone Number"

# =========================================================
# EXTRACT NAME
# =========================================================
def extract_name(text):

    lines = text.split("\n")

    for line in lines[:10]:

        line = line.strip()

        if len(line.split()) >= 2 and len(line) < 40:
            return line.title()

    return "Your Name"

# =========================================================
# GENERATE PROFESSIONAL SUMMARY
# =========================================================
def generate_summary(skills):

    if len(skills) == 0:
        return (
            "Results-driven professional with strong "
            "technical and communication skills."
        )

    top_skills = ", ".join(skills[:5])

    return (
        f"Results-driven professional with expertise in "
        f"{top_skills}. Skilled in problem-solving, "
        f"team collaboration, and delivering high-quality solutions."
    )

# =========================================================
# ATS PROFESSIONAL CV FORMATTER
# =========================================================
def generate_professional_cv(
    name,
    email,
    phone,
    skills,
    raw_text
):

    summary = generate_summary(skills)

    skills_section = " | ".join(skills)

    professional_cv = f"""
{name.upper()}

Email: {email}
Phone: {phone}

==================================================
PROFESSIONAL SUMMARY
==================================================

{summary}

==================================================
TECHNICAL SKILLS
==================================================

{skills_section}

==================================================
PROFESSIONAL EXPERIENCE
==================================================

• Developed and maintained professional projects.
• Worked on real-world problem-solving tasks.
• Collaborated with teams to deliver solutions.
• Improved performance and workflow efficiency.

==================================================
EDUCATION
==================================================

Bachelor's Degree / Relevant Education

==================================================
PROJECTS
==================================================

• AI Resume Screening System
• ATS Resume Generator
• Machine Learning Projects

==================================================
CERTIFICATIONS
==================================================

• Add certifications here

==================================================
LANGUAGES
==================================================

• English
"""

    return professional_cv

# =========================================================
# GENERATE SUGGESTIONS
# =========================================================
def generate_suggestions(
    missing_skills,
    match
):

    suggestions = []

    if match < 50:
        suggestions.append(
            "Your resume needs more alignment with the job description."
        )

    if missing_skills:
        suggestions.append(
            "Add these missing skills: "
            + ", ".join(missing_skills)
        )

    suggestions.append(
        "Use measurable achievements in experience."
    )

    suggestions.append(
        "Add more technical projects."
    )

    suggestions.append(
        "Use ATS-friendly formatting with clean headings."
    )

    return suggestions

# =========================================================
# UI
# =========================================================
st.title("📄 Advanced ATS Resume Screener AI")

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf", "docx"]
)

jd = st.text_area(
    "Paste Job Description"
)

# =========================================================
# PROCESS FILE
# =========================================================
if uploaded_file:

    # Extract Resume Text
    if uploaded_file.name.endswith(".pdf"):
        resume_text = extract_text_from_pdf(uploaded_file)

    else:
        resume_text = extract_text_from_docx(uploaded_file)

    cleaned_resume = clean_text(resume_text)

    # Extract Info
    name = extract_name(resume_text)
    email = extract_email(resume_text)
    phone = extract_phone(resume_text)

    # Extract Skills
    resume_skills = extract_skills(cleaned_resume)

    # =====================================================
    # SHOW EXTRACTED DETAILS
    # =====================================================
    st.subheader("🧠 Extracted Resume Information")

    st.write("### 👤 Name")
    st.success(name)

    st.write("### 📧 Email")
    st.success(email)

    st.write("### 📱 Phone")
    st.success(phone)

    st.write("### 💻 Skills Found")

    if resume_skills:
        st.success(", ".join(resume_skills))
    else:
        st.error("No skills detected.")

    # =====================================================
    # JOB DESCRIPTION MATCH
    # =====================================================
    if jd:

        cleaned_jd = clean_text(jd)

        jd_skills = extract_skills(cleaned_jd)

        match = calculate_match(
            cleaned_resume,
            cleaned_jd
        )

        missing_skills = list(
            set(jd_skills) - set(resume_skills)
        )

        st.subheader(f"✅ ATS Match Score: {match}%")

        st.progress(match / 100)

        st.write("### ❌ Missing Skills")

        if missing_skills:
            st.warning(", ".join(missing_skills))
        else:
            st.success("No important skills missing.")

        # Suggestions
        st.subheader("💡 Resume Suggestions")

        suggestions = generate_suggestions(
            missing_skills,
            match
        )

        for suggestion in suggestions:
            st.write("👉", suggestion)

    # =====================================================
    # GENERATE PROFESSIONAL ATS CV
    # =====================================================
    st.divider()

    st.subheader("📄 Professional ATS-Friendly CV")

    professional_cv = generate_professional_cv(
        name,
        email,
        phone,
        resume_skills,
        resume_text
    )

    st.text_area(
        "Generated CV",
        professional_cv,
        height=600
    )

    # Download Button
    st.download_button(
        label="📥 Download ATS CV",
        data=professional_cv,
        file_name="Professional_ATS_CV.txt",
        mime="text/plain"
    )
