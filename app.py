import streamlit as st
from dotenv import load_dotenv
from utils import file_handler, ai_logic

# Load environment variables from .env file
load_dotenv()

# --- 1. PAGE CONFIGURATION & STYLING ---
st.set_page_config(
    page_title="Resume Relevance Checker",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<style>
    /* --- Base App Styling --- */
    .stApp { background-color: #0E1117; color: #FAFAFA; }
    h1, h2, h3 {
        background: -webkit-linear-gradient(45deg, #00FFA3, #00B8FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* --- Widget Styling --- */
    .stButton>button {
        border-radius: 20px; border: 1px solid #00FFA3;
        color: #00FFA3; background-color: transparent;
    }
    .stButton>button:hover { background-color: #00FFA3; color: #0E1117; }
    
    [data-testid="stFileUploader"] button {
        border-radius: 20px; border: 1px solid #00B8FF; color: #00B8FF;
    }

    /* --- Layout Styling --- */
    .metric-card {
        background-color: rgba(40, 48, 61, 0.5);
        border-radius: 12px;
        padding: 25px;
        margin-bottom: 15px;
        border: 1px solid rgba(0, 255, 163, 0.3);
    }
    
    /* --- Responsive Fixes --- */
    @media (max-width: 768px) {
        div[data-testid="stHorizontalBlock"], .footer-flex-container {
            flex-direction: column !important;
        }
        .footer-flex-container div {
            padding: 10px 0 !important;
            border-left: none !important;
        }
    }
    
    /* --- Custom Header & Footer Styling --- */
    [data-testid="stCheckbox"] label {
        font-size: 1.25rem !important; font-weight: bold !important;
        color: #00B8FF !important; transition: color 0.3s;
    }
    [data-testid="stCheckbox"] label:hover { color: #00FFA3 !important; }
    
    .footer-links a {
        color: #00B8FF; text-decoration: none; font-weight: bold;
    }
    .footer-links a:hover { color: #00FFA3; }
    .footer-links svg { vertical-align: middle; margin-right: 8px; }

</style>
""", unsafe_allow_html=True)


# --- 2. SESSION STATE INITIALIZATION ---
if 'ai_results' not in st.session_state:
    st.session_state['ai_results'] = None


# --- 3. MAIN APP UI & WORKFLOW ---
st.title("🤖 Resume Relevance Check System")
st.markdown("Upload a resume and paste a job description for an instant AI-powered analysis.")

input_cols = st.columns(2)
with input_cols[0]:
    st.subheader("Upload Your Resume")
    resume_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"], key="resume", label_visibility="visible")
with input_cols[1]:
    st.subheader("Paste Job Description")
    job_description = st.text_area("Paste the job description here", height=320, key="jd", label_visibility="visible", placeholder="e.g., Senior Python Developer...")

button_cols = st.columns([1, 1])
with button_cols[0]:
    if st.button("✨ Check Relevance", use_container_width=True, type="primary"):
        if resume_file and job_description:
            st.session_state['ai_results'] = None
            with st.spinner("Our AI is analyzing... 🧠"):
                resume_text = file_handler.read_file_content(resume_file)
                if resume_text:
                    ai_results = ai_logic.get_relevance_score(resume_text, job_description)
                    if ai_results:
                        st.session_state['ai_results'] = ai_results
        else:
            st.error("Please upload a resume and provide a job description.")

with button_cols[1]:
    if st.button("Clear Results", use_container_width=True):
        st.session_state['ai_results'] = None
        st.rerun()

# --- 4. RESULTS VISUALIZATION (USING CHECKBOXES) ---
if st.session_state['ai_results']:
    results = st.session_state['ai_results']
    score = results.get("score", 0)

    st.header("Analysis Results")
    
    st.subheader(f"Relevance Score: {score}%")
    if score >= 80: st.progress(score / 100, text="🟢 Excellent Match!")
    elif score >= 60: st.progress(score / 100, text="🟡 Good Match")
    else: st.progress(score / 100, text="🔴 Needs Improvement")

    st.markdown(f'<div class="metric-card"><b>Summary:</b> {results.get("summary", "No summary provided.")}</div>', unsafe_allow_html=True)

    feedback_cols = st.columns(2)
    with feedback_cols[0]:
        if st.checkbox("✅ Strengths Aligned with Job", value=True):
            with st.container():
                strengths = results.get("strengths", ["No specific strengths identified."])
                for strength in strengths:
                    st.success(strength, icon="✅")
    with feedback_cols[1]:
        if st.checkbox("⚠️ Missing from Resume", value=True):
            with st.container():
                weaknesses = results.get("weaknesses", ["No specific weaknesses identified."])
                for weakness in weaknesses:
                    st.warning(weakness, icon="⚠️")
    
    if st.checkbox("🔑 Keywords Matched", value=False):
        with st.container():
            keywords = results.get("keywords_matched", [])
            if keywords:
                st.info(", ".join(keywords))
            else:
                st.info("No specific keywords were matched.")
# --- 5. FINAL, PERSONALIZED FOOTER ---
st.divider()

# SVG Icons
USER_ICON = """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>"""
EMAIL_ICON = """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg>"""
LINKEDIN_ICON = """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path><rect x="2" y="9" width="4" height="12"></rect><circle cx="4" cy="4" r="2"></circle></svg>"""
PORTFOLIO_ICON = """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path></svg>"""
RESUME_ICON = """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line></svg>"""

footer_html = f"""
<div class="metric-card">
    <div class="footer-flex-container" style="display: flex; justify-content: space-between;">
        <div style="flex: 2; padding-right: 30px;">
            <h4 style="color: #FFFFFF;">About This App</h4>
            <p style="color: #cccccc;">This tool leverages Generative AI to provide an instant analysis of a resume's relevance to a job description. It offers valuable insights for recruiters to streamline hiring and for job seekers to optimize their resumes.</p>
        </div>
        <div style="flex: 1; padding-left: 30px; border-left: 1px solid #00FFA3;" class="footer-links">
            <h4 style="color: #FFFFFF;">About the Creator</h4>
            <p>{USER_ICON} <strong>Manikumar K</strong></p>
            <p>{EMAIL_ICON} <a href="mailto:your.manikumarkundena@gmail.com">Contact via Email</a></p>
            <p>{LINKEDIN_ICON} <a href="https://www.linkedin.com/in/manikumar-k-2a637b378">LinkedIn Profile</a></p>
            <p>{PORTFOLIO_ICON} <a href="https://fg5fqm.csb.app/">Portfolio</a></p>
            <p>{RESUME_ICON} <a href="https://drive.google.com/file/d/1H_2hDH5Qy124Q2ikroX3i1B4tbaJz3bi/view?usp=sharing">Resume</a></p>
        </div>
    </div>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)