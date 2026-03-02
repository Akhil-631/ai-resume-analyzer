import os
import json
from PyPDF2 import PdfReader

from llm_client import call_llm
from prompts import RESUME_EXTRACTION_PROMPT, JOB_DESCRIPTION_EXTRACTION_PROMPT, LLM_EVALUATION_PROMPT

def _read_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()
    
def _read_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"

    if not text.strip():
        raise ValueError(
            "No extractable text found. PDF may be scanned. "
            "Only text-based PDFs are supported."
        )

    return text

def read_document(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError("File not found.")
    
    if file_path.endswith(".txt"):
        return _read_txt(file_path)
    
    elif file_path.endswith(".pdf"):
        return _read_pdf(file_path)
    
    else:
        raise ValueError("unsupported file format. Only .txt and .pdf are supported")
    
def clean_text(text):
    lines=text.splitlines()
    cleaned_lines=[]

    for line in lines:
        stripped=line.strip()
        if stripped !="":
            cleaned_lines.append(stripped)

    return "\n".join(cleaned_lines)


def extract_resume_data(file_path):

    raw_text=read_document(file_path)
    cleaned_text=clean_text(raw_text)

    if not cleaned_text.strip():
        raise ValueError("Resume text is empty after cleaning.")
    
    user_input = f"""
Resume Text:
{cleaned_text}
""" 
    response=call_llm(
        RESUME_EXTRACTION_PROMPT,
        user_input
    )
    return json.loads(response)

def extract_job_description_data(file_path):

    raw_text=read_document(file_path)
    cleaned_text=clean_text(raw_text)

    if not cleaned_text.strip():
        raise ValueError("Job Description text is empty after cleaning.")
    
    user_input = f"""
    Job Description:
    {cleaned_text}
    """

    response=call_llm(JOB_DESCRIPTION_EXTRACTION_PROMPT, user_input)
    
    return json.loads(response)
    


def compute_skill_gap(resume_data, jd_data):

    resume_skills=resume_data.get("skills", [])
    required_skills=jd_data.get("required_skills", [])

    resume_normalized= [skill.lower().strip() for skill in resume_skills]
    required_normalized=[skill.lower().strip() for skill in required_skills]

    matched=[]
    missing=[]

    for req in required_normalized:
        if any(any(word in req for word in res.split()) for res in resume_normalized):
            matched.append(req)
        else:
            missing.append(req)

    total_required=len(required_normalized)
    match_percentage=(len(matched) / total_required * 100) if total_required > 0 else 0

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "match_percentage": round(match_percentage,2)

    }

def compute_deterministic_score(resume_data, gap_data):

    base_score=gap_data["match_percentage"]

    project_bonus=0
    cert_bonus=0

    projects=resume_data.get("projects", [])
    certifications=resume_data.get("certifications", [])

    if len(projects) >=3:
        project_bonus=10
    elif len(projects) >=1:
        project_bonus=5

    if certifications:
        cert_bonus=5
    
    final_score=base_score+project_bonus+cert_bonus

    return round(min(final_score, 100), 2)

def compute_llm_evaluation(resume_data, jd_data, gap_data):

    user_input = f"""
Resume Data:
{resume_data}

Job Required Skills:
{jd_data.get("required_skills", [])}

Skill Gap:
Matched: {gap_data.get("matched_skills", [])}
Missing: {gap_data.get("missing_skills", [])}
Match Percenatge: {gap_data.get("match_percentage", [])}
"""
    response=call_llm(LLM_EVALUATION_PROMPT, user_input)

    return json.loads(response)

def compute_final_score(det_score, llm_score):
    
    final=(0.6 * det_score) + (0.4 * llm_score)

    return round(final, 2)

if __name__ == "__main__":

    print("This module is intended to be used via Streamlit app.")
    print("For testing, call functions directly with valid file paths.")

    resume_path = "VenkataSaiNandaKishore.Resume.pdf" 
    jd_path = "Job_Title_Data_Analyst.txt"

    resume_data = extract_resume_data(resume_path)
    jd_data = extract_job_description_data(jd_path)

    gap=compute_skill_gap(resume_data, jd_data)
    det_score=compute_deterministic_score(resume_data, gap)
    llm_eval=compute_llm_evaluation(resume_data, jd_data, gap)

    final_score=compute_final_score(det_score, llm_eval["llm_score"])

    print("Deterministic Score:", det_score)
    print("LLM Evaluation:", llm_eval)
    print("Final Score:", final_score)
