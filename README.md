📄 AI Resume Analyzer (Hybrid Evaluation System)
🚀 Overview

AI Resume Analyzer is a hybrid evaluation system that assesses resume–job fit using a combination of:

Deterministic skill matching (rule-based scoring)

LLM-based qualitative evaluation

Weighted final scoring

The system extracts structured information from both a resume and a job description, computes an objective skill match score, and enhances it with contextual evaluation from a large language model.

This project demonstrates practical GenAI system design beyond simple prompt-based applications.

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
1️⃣ Structured Extraction Layer (LLM → JSON)

The LLM is used strictly as a structured parser.

It extracts:

Skills

Projects

Certifications

Education

Experience summary

Required job skills

All outputs are enforced as JSON and parsed deterministically using json.loads().

Why structured JSON?

Machine-readable

Enables deterministic scoring

Prevents fragile string-based logic

Reduces hallucination impact

2️⃣ Deterministic Skill Matching (Python Logic)

Skill matching is computed using:

Lowercase normalization

Token-level overlap matching

Substring containment checks

Match Percentage:

Matched Required Skills / Total Required Skills

This ensures:

Transparency

Reproducibility

Explainability

Deterministic Score Formula
Base Score = Skill Match %

+ 10 points (≥ 3 projects)
+ 5 points (certifications present)

Final Deterministic Score capped at 100
3️⃣ LLM Qualitative Evaluation

The LLM evaluates:

Strengths

Weaknesses

Improvement suggestions

Overall qualitative score (0–100)

The model receives:

Structured resume data

Required skills

Skill gap results

This avoids reprocessing raw text and improves evaluation consistency.

4️⃣ Final Hybrid Score

Final score uses weighted averaging:

Final Score = (0.6 × Deterministic Score)
            + (0.4 × LLM Score)
Why weighted?

Deterministic scoring is objective → higher trust

LLM evaluation is contextual → nuanced insights

Hybrid approach balances stability and intelligence

🖥️ Streamlit UI

The application provides a clean dashboard with:

Deterministic Score

LLM Score

Final Score

Matched Skills

Missing Skills

Strengths

Weaknesses

Improvement Suggestions

The UI is intentionally minimal to emphasize system logic over styling.

⚙️ Engineering Decisions
✔ Hybrid Evaluation Instead of Pure LLM

Pure LLM scoring is non-deterministic and opaque.
Deterministic logic ensures explainability and auditability.

✔ Structured JSON Enforcement

Prevents fragile text parsing and enables reliable downstream logic.

✔ Token-Level Skill Matching

Avoids heavy NLP libraries while improving robustness over exact string matching.

✔ Fixed 60/40 Weighting

Simple, transparent, and interview-defensible.
In production, weights could be tuned using hiring outcome data.

✔ No OCR for Scanned PDFs

The system supports text-based PDFs only.
OCR was intentionally excluded to keep scope focused and lightweight.

📦 Tech Stack

Python

Streamlit

PyPDF2

Groq API (OpenAI-compatible)

LLM: openai/gpt-oss-20b

JSON-based structured prompting

▶️ How to Run

1️⃣ Install dependencies:

pip install -r requirements.txt

2️⃣ Run the app:

streamlit run app.py

3️⃣ Upload:

Resume (.pdf or .txt)

Job Description (.txt)

📈 Example Output

Deterministic Score: 81.67

LLM Score: 70

Final Score: 77.0

Skill gap analysis with actionable suggestions

🚧 Current Limitations

No OCR support for scanned PDFs

Basic token-level skill matching (no embedding similarity)

No ATS keyword weighting system

No persistent storage or authentication

🔮 Future Improvements

Embedding-based semantic skill matching

Historical hiring data calibration for scoring weights

ATS-style keyword weighting

OCR integration for scanned resumes

Export report as PDF