import streamlit as st
import tempfile
import json

from analyzer import(
    extract_resume_data,
    extract_job_description_data,
    compute_skill_gap,
    compute_deterministic_score,
    compute_llm_evaluation,
    compute_final_score
)

st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

st.title("📄 AI Resume Analyzer")
st.write("Upload your Resume and Job Description to get an AI-powered evaluation.")

resume_file=st.file_uploader("Upload Resume (.pdf or .txt)", type=["pdf", "txt"])
jd_file = st.file_uploader("Upload Job Description (.pdf or .txt)", type=["pdf", "txt"])

if resume_file and jd_file:
    if st.button("Analyze Resume"):

        resume_suffix = "." + resume_file.name.split(".")[-1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=resume_suffix) as temp_resume:
            temp_resume.write(resume_file.read())
            resume_path=temp_resume.name

        jd_suffix = "." + jd_file.name.split(".")[-1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=jd_suffix) as temp_jd:
            temp_jd.write(jd_file.read())
            jd_path=temp_jd.name

        with st.spinner("Analyzing..."):

            resume_data=extract_resume_data(resume_path)
            jd_data=extract_job_description_data(jd_path)

            gap=compute_skill_gap(resume_data, jd_data)
            det_score=compute_deterministic_score(resume_data, gap)
            llm_eval=compute_llm_evaluation(resume_data, jd_data, gap)
            final_score=compute_final_score(det_score, llm_eval["llm_score"])

        st.success("Analysis Complete!")

        st.subheader("📊 Scores")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Deterministic Score", det_score)
        with col2:
            st.metric("LLM Score", llm_eval["llm_score"])
        st.markdown("## 🎯 Final Score")
        st.metric(label="Overall Resume Match", value=f"{final_score}")

        st.subheader("🧩Skill Gap")
        st.markdown("**Matched Skills:**")
        for skill in gap.get("matched_skills", []):
            st.write(f"- {skill}")
        st.markdown("**Missing Skills:**")
        for skill in gap.get("missing_skills", []):
            st.write(f"- {skill}")

        st.subheader("💪 Strengths")
        for s in llm_eval["strengths"]:
            st.write(f"- {s}")

        st.subheader("⚠ Weaknesses")
        for w in llm_eval["weaknesses"]:
            st.write(f"- {w}")

        st.subheader("🚀 Improvement Suggestions")
        for i in llm_eval["improvement_suggestions"]:
            st.write(f"- {i}")
