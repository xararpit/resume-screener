import spacy

# Load the model with NER enabled to help detect skills/entities
nlp = spacy.load("en_core_web_md")

def calculate_similarity(resume_text: str, jd_text: str) -> float:
    """
    Calculates semantic similarity between resume and JD using SciPy word vectors.
    """
    if not resume_text or not jd_text:
        return 0.0
        
    resume_doc = nlp(resume_text)
    jd_doc = nlp(jd_text)
    
    # Using SpaCy's built-in vector similarity
    return resume_doc.similarity(jd_doc)

def get_missing_skills(resume_text: str, jd_text: str) -> list:
    """
    Extracts noun chunks from the JD as 'skills' and checks if they exist in the resume.
    """
    if not jd_text:
        return []

    jd_doc = nlp(jd_text)
    resume_text_lower = resume_text.lower()
    
    # Extract noun chunks (potential skills/technologies) from JD
    jd_skills = set()
    for chunk in jd_doc.noun_chunks:
        # Filter out very short words or common stop pronouns
        skill = chunk.text.lower().strip()
        if len(skill) > 2 and not chunk.root.is_stop:
            jd_skills.add(skill)
            
    # Find which JD skills are missing from the resume
    missing_skills = []
    for skill in jd_skills:
        if skill not in resume_text_lower:
            missing_skills.append(skill)
            
    # Return at most 10 missing skills to avoid overwhelming the UI
    return sorted(missing_skills)[:10]
