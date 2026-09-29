from flask import Flask, render_template, request
from analyzer import extract_pdf_text, extract_docx_text, detect_skills

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    file = request.files["resume"]

    if not file or file.filename == "":
        return "Please upload a resume."

    filename = file.filename.lower()

    if filename.endswith(".pdf"):
        text = extract_pdf_text(file)
    elif filename.endswith(".docx"):
        text = extract_docx_text(file)
    else:
        return "Please upload a PDF or DOCX file."

    skills = detect_skills(text)

    # ---- MISSING SKILLS LOGIC ----
    required_skills = [
        "Python",
        "SQL",
        "Machine Learning",
        "Cloud Computing",
        "Power BI"
    ]

    missing_skills = [
        skill for skill in required_skills
        if skill.lower() not in text.lower()
    ]

    # ---- SCORING ----
    score = 0

    if text:
        score += 30

    if len(skills) >= 5:
        score += 20
    elif len(skills) >= 3:
        score += 10

    sections = ["education", "projects", "experience", "skills", "objective"]

    for section in sections:
        if section in text.lower():
            score += 10

    score = min(score, 100)

    # ---- RECOMMENDATIONS ----
    recommendations = []

    if "projects" not in text.lower():
        recommendations.append("Add a Projects section to highlight your practical work.")

    if "certification" not in text.lower():
        recommendations.append("Add relevant certifications to strengthen your resume.")

    if len(skills) < 5:
        recommendations.append("Add more relevant technical skills.")

    if "education" not in text.lower():
        recommendations.append("Make sure your Education section is clearly included.")

    if len(text) < 500:
        recommendations.append("Add more relevant details about your experience and projects.")

    return render_template(
        "result.html",
        text=text,
        skills=skills,
        score=score,
        recommendations=recommendations,
        missing_skills=missing_skills
    )

if __name__ == "__main__":
    app.run(debug=True)