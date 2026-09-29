from PyPDF2 import PdfReader
from docx import Document


def extract_pdf_text(file):
    reader = PdfReader(file)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text


def extract_docx_text(file):
    document = Document(file)
    text = ""

    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"

    return text



def detect_skills(text):
    skills = [
        "python",
        "java",
        "c",
        "html",
        "css",
        "javascript",
        "sql",
        "mysql",
        "machine learning",
        "artificial intelligence",
        "cloud computing",
        "numpy",
        "pandas",
        "scikit-learn",
        "tensorflow",
        "pytorch",
        "power bi",
        "tableau",
        "communication skills"
    ]

    found_skills = []
    missing_skills = []

    text_lower = text.lower()

    for skill in skills:
        if skill.lower() in text_lower:
            found_skills.append(skill)
        else:
            missing_skills.append(skill)

    return found_skills, missing_skills