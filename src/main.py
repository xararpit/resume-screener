from pathlib import Path
from src.resume_parser import extract_text_from_pdf
from src.text_cleaner import clean_text
from src.similarity import calculate_similarity

resume_path = Path(r"data\Arpit resume.pdf")

job_description = """
Technical & Analytical Skills

Proficiency in MS Excel (formulas, pivot tables, data handling)

Basic to intermediate knowledge of SQL for data querying

Working knowledge of Python or any programming language for data manipulation or automation

Understanding of data analysis concepts and structured problem-solving

Familiarity with databases, data validation, and reporting

Cognitive & Problem-Solving Skills

Strong analytical and logical reasoning ability

Ability to break down complex problems into structured steps

Capability to interpret data and derive meaningful insights

Attention to detail with a focus on accuracy and consistency

Communication & Professional Skills

Good verbal and written communication in English

Ability to explain technical findings to non-technical stakeholders

Professional email writing and documentation skills

Stakeholder coordination and collaboration mindset

Behavioral & Consulting Readiness

Strong learning agility and adaptability

Ability to work under deadlines and performance pressure

Ethical mindset and professional judgment

Team-oriented with a client-service attitude
`

"""

text = extract_text_from_pdf(resume_path)
cleaned_resume = clean_text(text)
cleaned_jd = clean_text(job_description)
##print(cleaned_resume)

score = calculate_similarity(cleaned_resume, cleaned_jd)
match_percentage=score * 100
print(f"MATCH PERCENTAGE:{match_percentage:.2f}%")
