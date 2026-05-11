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
    page_title="Professional ATS Resume AI",
    page_icon="📄",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================
st.markdown("""
<style>

.stApp {
    background: linear-gradient(to bottom right, #0f172a, #111827);
    color: white;
}

h1, h2, h3 {
    color: white !important;
}

.big-card {
    background-color: #1e293b;
    padding: 25px;
    border-radius: 15px;
    margin-bottom: 20px;
    border: 1px solid #334155;
}

.skill-box {
    background-color: #2563eb;
    padding: 8px 14px;
    border-radius: 10px;
    display: inline-block;
    margin: 5px;
    color: white;
    font-size: 14px;
}

.score-box {
    background-color: #111827;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #374151;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# PDF TEXT EXTRACTION
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
# DOCX TEXT EXTRACTION
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

    text = re.sub(r'[^a-zA-Z0-9+#. ]', ' ', text)

    return text

# =========================================================
# ATS MATCH SCORE
# =========================================================
def calculate_match(resume, jd):

    tfidf = TfidfVectorizer(stop_words='english')

    matrix = tfidf.fit_transform([resume, jd])

    similarity = cosine_similarity(matrix)[0][1]

    return round(similarity * 100, 2)

# =========================================================
# SKILLS DATABASE
# =========================================================
skills_database = [

    "python",
    "java",
    "c++",
    "c",
    "javascript",
    "typescript",
    "php",
    "react",
    "nextjs",
    "nodejs",
    "express",
    "html",
    "css",
    "bootstrap",
    "tailwind",
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "machine learning",
    "deep learning",
    "tensorflow",
    "pytorch",
    "opencv",
    "nlp",
    "pandas",
    "numpy",
    "excel",
    "power bi",
    "tableau",
    "aws",
    "azure",
    "docker",
    "kubernetes",
    "firebase",
    "git",
    "github",
    "linux",
    "streamlit",
    "figma",
    "communication",
    "leadership",
    "teamwork",
    "problem solving"
]

# =========================================================
# SKILL EXTRACTION
# =========================================================
def extract_skills(text):

    found_skills = []

    text = text.lower()

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

    return "Your Phone"

# =========================================================
# EXTRACT NAME
# =========================================================
def extract_name(text):

    lines = text.split("\n")

    for line in lines[:10]:

        line = line.strip()

        if len(line.split()) >= 2 and len(line) < 35:
            return line.title()

    return "Your Name"

# =========================================================
# PROFESSIONAL SUMMARY
# =========================================================
def generate_summary(skills):

    if len(skills) == 0:
        return (
            "Results-driven professional with strong "
            "technical and communication skills."
        )

    top_skills = ", ".join(skills[:5])

    return (
        f"Results-driven professional skilled in "
        f"{top_skills}. Experienced in problem-solving, "
        f"team collaboration, and delivering high-quality projects."
    )

# =========================================================
# PROFESSIONAL CV GENERATOR
# =========================================================
def generate_professional_cv(
    name,
    email,
    phone,
    skills,
    experience,
    education,
    projects,
    certifications
):

    summary = generate_summary(skills)

    skills_text = " | ".join(skills)

    cv = f"""
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

{skills_text}

==================================================
PROFESSIONAL EXPERIENCE
==================================================

{experience}

==================================================
EDUCATION
==================================================

{education}

==================================================
PROJECTS
==================================================

{projects}

==================================================
CERTIFICATIONS
==================================================

{certifications}

==================================================
LANGUAGES
==================================================

• English
"""

    return cv

# =========================================================
# SUGGESTIONS
# =========================================================
def generate_suggestions(
    missing_skills,
    match
):

    suggestions = []

    if match < 50:
        suggestions.append(
            "Improve alignment with the job description."
        )

    if missing_skills:
        suggestions.append(
            "Add missing skills: "
            + ", ".join(missing_skills)
        )

    suggestions.append(
        "Use measurable achievements with numbers."
    )

    suggestions.append(
        "Add technical projects and certifications."
    )

    suggestions.append(
        "Use clean ATS-friendly formatting."
    )

    return suggestions

# =========================================================
# HERO SECTION
# =========================================================
st.markdown("""
<div class="big-card">
    <h1>📄 Professional ATS Resume AI</h1>
    <p>
        Analyze resumes, calculate ATS score,
        detect skills, and generate professional ATS-friendly CVs.
    </p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# TABS
# =========================================================
tab1, tab2 = st.tabs([
    "📊 Resume Analyzer",
    "📄 ATS CV Builder"
])

# =========================================================
# TAB 1
# =========================================================
with tab1:

    uploaded_file = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx"]
    )

    jd = st.text_area(
        "Paste Job Description"
    )

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

        # Profile Info
        col1, col2, col3 = st.columns(3)

        with col1:
            st.info(f"👤 {name}")

        with col2:
            st.info(f"📧 {email}")

        with col3:
            st.info(f"📱 {phone}")

        # Skills
        st.subheader("💻 Skills Detected")

        if resume_skills:

            for skill in resume_skills:

                st.markdown(
                    f'<span class="skill-box">{skill}</span>',
                    unsafe_allow_html=True
                )

        else:
            st.error("No skills detected.")

        # ATS Match
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

            st.subheader("📊 ATS Match Score")

            st.markdown(
                f"""
                <div class="score-box">
                    <h1>{match}%</h1>
                    <p>Resume Match Score</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.progress(match / 100)

            # Missing Skills
            st.subheader("❌ Missing Skills")

            if missing_skills:

                for skill in missing_skills:
                    st.warning(skill)

            else:
                st.success("No important skills missing.")

            # Suggestions
            st.subheader("💡 Suggestions")

            suggestions = generate_suggestions(
                missing_skills,
                match
            )

            for suggestion in suggestions:
                st.write("👉", suggestion)

# =========================================================
# TAB 2
# =========================================================
with tab2:

    st.subheader("📄 Generate ATS-Friendly CV")

    col1, col2 = st.columns(2)

    with col1:

        cv_name = st.text_input("Full Name")

        cv_email = st.text_input("Email")

        cv_phone = st.text_input("Phone Number")

    with col2:

        skills_input = st.text_area(
            "Skills (comma separated)",
            height=120
        )

    experience = st.text_area(
        "Professional Experience",
        height=150
    )

    education = st.text_area(
        "Education",
        height=120
    )

    projects = st.text_area(
        "Projects",
        height=120
    )

    certifications = st.text_area(
        "Certifications",
        height=100
    )

    if st.button("🚀 Generate ATS CV"):

        skills = [
            s.strip()
            for s in skills_input.split(",")
            if s.strip() != ""
        ]

        generated_cv = generate_professional_cv(
            cv_name,
            cv_email,
            cv_phone,
            skills,
            experience,
            education,
            projects,
            certifications
        )

        st.subheader("✅ Generated ATS-Friendly CV")

        st.text_area(
            "Professional CV",
            generated_cv,
            height=650
        )

        st.download_button(
            label="📥 Download CV",
            data=generated_cv,
            file_name="Professional_ATS_CV.txt",
            mime="text/plain"
        )

# =========================================================
# FOOTER
# =========================================================
st.divider()

st.caption(
    "Built with Streamlit • Professional ATS Resume AI"
)
