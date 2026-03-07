import streamlit as st
import pandas as pd
from src.resume_parser import extract_text_from_pdf
from src.text_cleaner import clean_text
from src.similarity import calculate_similarity, get_missing_skills

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Resume Screener",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Custom CSS for Styling ---
st.markdown("""
<style>
    /* Overall background */
    .stApp {
        background-color: #F7F7F7;
        font-family: 'Inter', sans-serif;
    }
    
    /* Header styling */
    h1 {
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.5rem;
        color: #000000;
    }
    .subtitle {
        text-align: center;
        margin-bottom: 2rem;
        font-size: 1.1rem;
        color: #555555;
    }
    
    /* Make the two main layout columns look like distinct cards */
    [data-testid="column"] {
        background-color: #FFFFFF;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        border: 1.5px solid #EAEAEA;
        height: 100%;
        transition: all 0.2s ease-in-out;
    }
    
    /* Card Hover State */
    [data-testid="column"]:hover {
        border: 1.5px solid #000000;
        box-shadow: none;
    }
    
    /* Make the results section at the bottom look like a distinct card */
    [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] > div:nth-child(4) {
        background-color: #FFFFFF;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        border: 1.5px solid #EAEAEA;
        margin-top: 2rem;
        transition: all 0.2s ease-in-out;
    }

    /* Results section hover state */
    [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] > div:nth-child(4):hover {
        border: 1.5px solid #000000;
        box-shadow: none;
    }

    /* Style the file uploader within the card */
    .stFileUploader {
        padding: 1rem;
        border-radius: 8px;
        background-color: #F7F7F7;
        border: 1.5px dashed #cccccc;
        transition: all 0.2s ease-in-out;
    }

    /* File uploader hover state */
    .stFileUploader:hover {
        border: 1.5px dashed #000000;
        background-color: #FFFFFF;
    }
    
    /* Table styling */
    .dataframe {
        border-radius: 8px !important;
        overflow: hidden !important;
        border: 1px solid #EAEAEA;
    }
</style>
""", unsafe_allow_html=True)

# --- App Header ---
st.title("AI Resume Screener")
st.markdown("<p class='subtitle'>Automate your recruitment process by intelligently matching candidate resumes against your target job description.</p>", unsafe_allow_html=True)

# --- Main App Layout ---
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 📝 Job Description")
    st.markdown("Paste the requirements and skills for the open role.")
    
    # Default JD for demonstration
    default_jd = """Technical & Analytical Skills
Proficiency in MS Excel (formulas, pivot tables, data handling)
Basic to intermediate knowledge of SQL for data querying
Working knowledge of Python or any programming language for data manipulation or automation
"""
    
    job_description = st.text_area(
        "", 
        value=default_jd,
        height=300,
        placeholder="Enter your Job Description here..."
    )

with col2:
    st.markdown("### 📄 Upload Resumes")
    st.markdown("Upload candidate resumes in PDF format. You can upload multiple files at once.")
    
    uploaded_files = st.file_uploader(
        "Upload Candidate PDFs", 
        type="pdf", 
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

# --- Processing & Results section ---
st.divider()

if not uploaded_files:
    st.info("👋 Welcome! Please enter a job description and upload one or more resumes to see the analysis.")
elif not job_description.strip():
    st.warning("⚠️ Please provide a job description for comparison.")
else:
    st.markdown("### 📊 Candidate Leaderboard")
    
    with st.spinner('Analyzing documents using NLP...'):
        results = []
        cleaned_jd = clean_text(job_description)
        
        for file in uploaded_files:
            try:
                # Process each file directly from Streamlit's InMemoryUploadedFile
                pdf_text = extract_text_from_pdf(file)
                cleaned_resume = clean_text(pdf_text)
                
                # Compute Similarity
                score = calculate_similarity(cleaned_resume, cleaned_jd)
                match_percentage = round(score * 100, 2)
                
                # Extract Missing Skills
                missing_skills = get_missing_skills(cleaned_resume, cleaned_jd)
                missing_str = ", ".join(missing_skills) if missing_skills else "None"
                
                results.append({
                    "Candidate File": file.name,
                    "Match Score (%)": match_percentage,
                    "Missing Skills": missing_str,
                    "Status": "✅ Analyzed"
                })
            except Exception as e:
                results.append({
                    "Candidate File": file.name,
                    "Match Score (%)": 0.0,
                    "Missing Skills": "N/A",
                    "Status": f"❌ Error: {str(e)}"
                })
        
        # Convert results to DataFrame for beautiful display
        df = pd.DataFrame(results)
        
        # Sort by Match Score descending
        df = df.sort_values(by="Match Score (%)", ascending=False).reset_index(drop=True)
        
        # Add visual indicators for scores
        def highlight_scores(val):
            if isinstance(val, (int, float)):
                if val >= 50:
                    color = '#dcfce7' # light green
                elif val >= 25:
                    color = '#fef08a' # yellow
                else:
                    color = '#fee2e2' # red
                return f'background-color: {color}'
            return ''
            
        styled_df = df.style.map(highlight_scores, subset=['Match Score (%)'])
        
        # Display Leaderboard
        st.dataframe(
            styled_df,
            column_config={
                "Match Score (%)": st.column_config.ProgressColumn(
                    "Match",
                    help="Semantic similarity percentage against target JD",
                    format="%f%%",
                    min_value=0,
                    max_value=100,
                ),
                "Candidate File": st.column_config.TextColumn("Candidate Resume Document", width="medium"),
                "Missing Skills": st.column_config.TextColumn("Identified Skill Gaps", width="large")
            },
            hide_index=True,
            use_container_width=True
        )

        
        # Display Top Metrics
        if not df.empty:
            st.markdown("#### Summary Insights")
            col_m1, col_m2, col_m3 = st.columns(3)
            with col_m1:
                st.metric(label="Total Candidates", value=len(df))
            with col_m2:
                top_scorer_name = df.iloc[0]["Candidate File"]
                top_scorer_score = f"{df.iloc[0]['Match Score (%)']}%"
                st.metric(label="Top Candidate", value=top_scorer_name)
            with col_m3:
                average_score = round(df['Match Score (%)'].mean(), 2)
                st.metric(label="Average Match", value=f"{average_score}%")
