📄 AI Resume Analyzer — Hybrid Evaluation System
🎯 Problem Statement

Resume screening is often either:

Manual and time-consuming, or

Fully AI-driven but opaque and non-deterministic.

Pure conversational LLM tools can analyze resumes, but they lack transparency, reproducibility, and structured integration into hiring systems.

This project explores how to build a structured, explainable AI system that evaluates resume–job fit using a hybrid deterministic + LLM architecture.

🚀 Overview

AI Resume Analyzer is a hybrid evaluation system that combines:

Deterministic skill-based scoring

LLM-powered qualitative analysis

Weighted final scoring

The system extracts structured information from both a resume and a job description, computes an objective skill match score, and enhances it with contextual reasoning from a large language model.

The goal is not just resume feedback — but architecturally controlled AI evaluation.

🏗️ Architecture Overview

The system follows a clean 3-layer architecture:

                ┌─────────────────────────┐
                │   Resume (PDF / TXT)    │
                └────────────┬────────────┘
                             │
                ┌────────────▼────────────┐
                │   Structured Extraction │  (LLM → JSON)
                └────────────┬────────────┘
                             │
                ┌────────────▼────────────┐
                │ Deterministic Skill Gap │  (Python Logic)
                └────────────┬────────────┘
                             │
                ┌────────────▼────────────┐
                │   LLM Qualitative Eval  │
                └────────────┬────────────┘
                             │
                ┌────────────▼────────────┐
                │    Weighted Final Score │
                └─────────────────────────┘
🔎 System Components
1️⃣ Structured Extraction (LLM → JSON)

The LLM is used strictly as a structured parser.

It extracts:

Skills

Projects

Certifications

Education

Experience summary

Required job skills

All outputs are enforced as JSON and parsed using json.loads().

Why structured JSON?

Machine-readable

Reduces hallucination risk

Enables deterministic scoring

Allows downstream system integration

2️⃣ Deterministic Skill Matching (Python Logic)

Skill matching is computed using:

Lowercase normalization

Token-level overlap matching

Substring containment checks

Match Percentage:

Matched Required Skills / Total Required Skills
Deterministic Score Formula
Base Score = Skill Match %

+ 10 points (≥ 3 projects)
+ 5 points (certifications present)

Score is capped at 100.

Why deterministic scoring?

Pure LLM evaluation is non-deterministic and opaque.
This rule-based layer ensures:

Transparency

Reproducibility

Explainability

Auditability

3️⃣ LLM Qualitative Evaluation

The LLM evaluates:

Strengths

Weaknesses

Improvement suggestions

Qualitative score (0–100)

The model receives:

Structured resume data

Required skills

Computed skill gap

It does not reprocess raw resume text unnecessarily.

4️⃣ Hybrid Final Score

The final score is calculated using weighted averaging:

Final Score = (0.6 × Deterministic Score)
            + (0.4 × LLM Score)
Why weighted?

Deterministic scoring = objective, stable

LLM evaluation = contextual, nuanced

The hybrid design balances:

Stability

Explainability

Contextual intelligence

🖥️ Streamlit Interface

The application provides a clean evaluation dashboard:

Deterministic Score

LLM Score

Final Weighted Score

Matched Skills

Missing Skills

Strengths

Weaknesses

Improvement Suggestions

UI is intentionally minimal to emphasize system logic over styling.

⚙️ Engineering Decisions
✔ Hybrid Instead of Pure LLM

Pure LLM scoring is opaque and unstable.
Pure rule-based systems lack contextual reasoning.
This system intentionally combines both.

✔ Structured Output Enforcement

JSON-based prompting ensures machine-readable and parseable results.

✔ Token-Level Matching

Avoids heavy NLP pipelines while remaining more robust than exact string matching.

✔ Fixed 60/40 Weighting

Simple, transparent, and interview-defensible.
In production, weights could be calibrated using historical hiring data.

✔ No OCR for Scanned PDFs

The system supports text-based PDFs only.
OCR was intentionally excluded to keep scope focused and lightweight.

📦 Tech Stack

Python

Streamlit

PyPDF2

OpenAI-compatible Groq API

LLM: openai/gpt-oss-20b

JSON-based structured prompting

▶️ How to Run

1️⃣ Install dependencies:

pip install -r requirements.txt

2️⃣ Run the application:

streamlit run app.py

3️⃣ Upload:

Resume (.pdf or .txt)

Job Description (.txt)

🚧 Current Limitations

No OCR for scanned resumes

Basic token-level skill matching (no semantic embeddings yet)

Fixed weighting strategy

No persistence or authentication

🔮 Future Improvements

Embedding-based semantic skill matching

Historical data calibration for scoring weights

Bias monitoring and fairness auditing

OCR integration

PDF export of evaluation report

🧠 What This Project Demonstrates

Structured LLM extraction

Deterministic vs probabilistic system design

Hybrid AI architecture

Hallucination control

Explainable scoring systems

Practical GenAI debugging experience