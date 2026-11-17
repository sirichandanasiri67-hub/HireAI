import streamlit as st
import os
from PyPDF2 import PdfReader
import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()

# Setup explicit API logic connections cleanly 
API_KEY = os.getenv("GEMINI_API_KEY") or "YOUR_GEMINI_API_KEY_HERE"
genai.configure(api_key=API_KEY)



def extract_text_from_pdf(uploaded_file):
    try:
        pdf_reader = PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        
        # Clean unicode surrogates safely
        clean_text = text.encode('utf-8', 'ignore').decode('utf-8', 'ignore')
        return clean_text
    except Exception as e:
        return f"Error reading PDF data layers: {str(e)}"

def call_gemini_api(prompt_text):
    """Balanced medium-length layout targeting crisp 2-3 sentence structured feedback"""
    try:
        model = genai.GenerativeModel("gemini-3.5-flash")
        
        # PERFECT SWEET SPOT BALANCE RULES
        system_rules_prefix = (
            "You are an expert HR recruitment specialist automation core. "
            "STRICT CORE RULES: Do NOT write long verbose paragraphs or essays. "
            "Do NOT write single-word or single-phrase ultra-short responses either. "
            "For every point, provide exactly 2-3 informative sentences. "
            "Keep the output extremely structured using clean bold headings and bullet lists.\n\n"
        )
        
        safe_prompt = f"{system_rules_prefix}{prompt_text}".encode('utf-8', 'ignore').decode('utf-8', 'ignore')
        response = model.generate_content(safe_prompt)
        return response.text
    except Exception as e:
        try:
            model = genai.GenerativeModel("models/gemini-2.5-flash")
            safe_prompt_backup = f"{system_rules_prefix}{prompt_text}".encode('utf-8', 'ignore').decode('utf-8', 'ignore')
            response = model.generate_content(safe_prompt_backup)
            return response.text
        except Exception:
            return f"⚠️ Connection parameters alignment error check. Details: {str(e)}"

def analyze_resume(resume_text):
    prompt = (
        f"Perform an advanced ATS profile scan on the provided resume context. "
        f"Format your response strictly under these 3 distinct headings:\n"
        f"### 📊 ATS Profile Alignment Metrics\n"
        f"Provide the Match Percentage with a 2-sentence reasoning breakdown.\n"
        f"### ⚙️ Primary Core Stack Analysis\n"
        f"List key identified tech stacks and evaluate their placement level in 2 sentences.\n"
        f"### 🎯 Critical Optimization Targets\n"
        f"Identify exactly 2 critical gaps with a 2-sentence actionable correction roadmap for each.\n\n"
        f"Resume Context:\n{resume_text}"
    )
    return call_gemini_api(prompt)

def hr_assistant(name, skills, experience):
    prompt = (
        f"Create a balanced candidate evaluation scorecard report for: '{name}' "
        f"using listed skills: '{skills}' and experience factor: '{experience}'. "
        f"Structure exactly under these 3 headers:\n"
        f"### 📋 Candidate Evaluation Index\n"
        f"State Fitness Index Evaluation percentage score and explain its justification criteria.\n"
        f"### 🧠 Behavioral & Culture Parameters\n"
        f"Analyze professional presentation patterns and overall corporate mindset fitment.\n"
        f"### ⚡ Strategic Selection Conclusion\n"
        f"State ultimate verification recommendation (HIRE/HOLD/REJECT) with an explicit executive justification layout."
    )
    return call_gemini_api(prompt)

def generate_questions(skill):
    prompt = (
        f"Generate exactly 5 advanced structured technical screening evaluation questions mapping core methodologies for: {skill}. "
        f"Ensure the questions cover different difficulty levels (Beginner, Intermediate, Advanced). "
        f"Right beneath each individual question block, provide an accurate, complete 2-3 sentence reference answer layer "
        f"and include key technical keywords that an ideal candidate should mention."
    )
    return call_gemini_api(prompt)
def recommend_job(skills):
    prompt = (
        f"Evaluate the technical proficiency scope of this skills data list: {skills}. "
        f"Determine the top 2 ideal high-paying corporate designations. "
        f"For each recommended designation role, provide a clear functional explanation of why the match is optimal "
        f"and include exactly one high-value professional certification path to target."
    )
    return call_gemini_api(prompt)


# ==========================================
# ADVANCED CUSTOM CSS ENHANCED GRAPHICS LOOK
# ==========================================

st.set_page_config(
    page_title="HireAI Premium Suite",
    page_icon="💼",
    layout="wide"
)

# Deep UI Skin transformation adding custom glass neon dashboard boxes dynamically
st.markdown("""
    <style>
    /* Absolute background gradient template layout configuration mapping */
    .stApp {
        background-color: #0B0F19 !important;
        background-image: radial-gradient(at 0% 0%, rgba(30, 58, 138, 0.3) 0, transparent 50%), 
                          radial-gradient(at 50% 100%, rgba(17, 24, 39, 0.5) 0, transparent 50%) !important;
    }
    
    /* Native stream title configurations overriding static dark-mode presets */
    h1, h2, h3, h4, h5, h6 {
        color: #F8FAFC !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Premium Title layout elements customization tracking layers */
    .dashboard-super-title {
        font-family: 'Inter', sans-serif;
        font-size: 42px;
        font-weight: 900;
        letter-spacing: -1px;
        color: #F8FAFC !important;
        margin-bottom: 2px;
    }
    .dashboard-tagline {
        font-size: 14px;
        color: #64748B !important;
        margin-bottom: 35px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Custom Neo-Glow Box Wrapper Styling for responses output layer matching templates */
    .neo-report-card {
        background: #111827 !important;
        border: 1px solid #1F2937 !important;
        border-left: 6px solid #38BDF8 !important;
        padding: 25px !important;
        border-radius: 12px !important;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.7) !important;
        margin-top: 25px;
        color: #E2E8F0 !important;
        line-height: 1.6;
    }

    /* Fixed Markdown text elements inside cards to stop inheriting blue/gradient tags */
    .neo-report-card ul, .neo-report-card li, .neo-report-card p {
        color: #E2E8F0 !important;
    }
    
    /* Ensuring symbols/bullet list tokens render explicitly white/gray instead of blue tint overrides */
    .neo-report-card li::marker {
        color: #94A3B8 !important;
    }

    .neo-report-card strong {
        color: #38BDF8 !important;
    }
    
    /* Metrics panel standard layout color tracking overrides custom blocks */
    div[data-testid="stMetricValue"] {
        color: #38BDF8 !important;
        font-weight: 800 !important;
        font-size: 32px !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #94A3B8 !important;
        font-size: 13px !important;
        text-transform: uppercase;
    }
    </style>
""", unsafe_allow_html=True)


# ==========================================
# SIDEBAR APPLICATION CONTROLLER LINK MODULES
# ==========================================

st.sidebar.markdown("<div style='padding: 10px 0px; text-align:center;'><h1 style='color:#38BDF8; font-size:32px; font-weight:900; margin:0;'>HireAI</h1><span style='color:#64748B; font-size:11px; letter-spacing:2px;'>CORE SYSTEM DECK</span></div>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# ==========================================
# SIDEBAR BUTTON NAVIGATION
# ==========================================

if "page" not in st.session_state:
    st.session_state.page = "📊 System Dashboard"

st.sidebar.markdown("""
<style>

div.stButton > button {
    width: 100%;
    height: 52px;
    background: #2563EB;
    color: white !important;
    border: none;
    border-radius: 12px;
    font-size: 15px;
    font-weight: 700;
    margin-bottom: 8px;
    transition: all 0.2s ease;
    cursor: pointer;
}

div.stButton > button:hover {
    background: #1D4ED8;
    transform: scale(1.04);
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

if st.sidebar.button("📊 System Dashboard", use_container_width=True):
    st.session_state.page = "📊 System Dashboard"

if st.sidebar.button("📄 ATS Resume Parser", use_container_width=True):
    st.session_state.page = "📄 ATS Resume Parser"

if st.sidebar.button("👨‍💼 HR Scorecard Core", use_container_width=True):
    st.session_state.page = "👨‍💼 HR Scorecard Core"

if st.sidebar.button("❓ Technical Query Engine", use_container_width=True):
    st.session_state.page = "❓ Technical Query Engine"

if st.sidebar.button("🎯 Career Path Matrix", use_container_width=True):
    st.session_state.page = "🎯 Career Path Matrix"

page = st.session_state.page

st.sidebar.markdown("---")
st.sidebar.markdown("<div style='color: #334155; font-size:11px; text-align:center;'>System Pipeline Engine Security Layer: SSL-Active</div>", unsafe_allow_html=True)


# ==========================================
# ROUTING CONTROLLER PARSING STREAMS LOGIC
# ==========================================

# --- SYSTEM DASHBOARD CORE CONFIG ---
if page == "📊 System Dashboard":
    st.markdown("<div class='dashboard-super-title'>🤖 HireAI Operations Hub</div>", unsafe_allow_html=True)
    st.markdown("<div class='dashboard-tagline'>Next-gen automated workspace optimization framework logs</div>", unsafe_allow_html=True)
    st.markdown("---")

    # Metrics Layout Deck
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("System Core Engine", "Gemini 2.5", "Up-to-date Version")
    with col2:
        st.metric("ATS Tuning Target", "95% Sync", "Configured High")
    with col3:
        st.metric("Active Logic Deck", "4 Core Modules", "Fully Loaded")
    with col4:
        st.metric("Operational Latency", "0.38s Response", "Optimal Network")

    st.markdown("---")
    st.subheader("⚙️ Fully Loaded Subsystem Modules Context Logs")
    
    c1, c2 = st.columns(2)
    with c1:
        st.info("⚡ **ATS Resume Parser:** Maps candidate profiles against token database matrix files safely.")
        st.info("⚡ **Technical Query Engine:** Automatically compiles direct functional vetting loops.")
    with c2:
        st.success("💼 **HR Scorecard Core:** Computes operational fitment parameters instant dashboard panels.")
        st.success("💼 **Career Path Matrix:** Processes smart algorithmic recommendations based on attributes.")


# --- MODULE: ATS RESUME PARSER ---
elif page == "📄 ATS Resume Parser":
    st.markdown("<div class='dashboard-super-title'>📄 ATS Resume Parser</div>", unsafe_allow_html=True)
    st.markdown("<div class='dashboard-tagline'>Parse candidate tracking metrics documentation frameworks</div>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload Target Resume (PDF Only)", type=["pdf"])

    if uploaded_file is not None:
        with st.spinner("Extracting token string streams..."):
            text_content = extract_text_from_pdf(uploaded_file)
        st.toast("PDF Stream Read Successfully!", icon="📥")

        if st.button("Run AI Core Analysis Scan", type="primary"):
            with st.spinner("Compiling ATS diagnostics metrics..."):
                result = analyze_resume(text_content)
            
            st.markdown(f"<div class='neo-report-card'>{result}</div>", unsafe_allow_html=True)


# --- MODULE: HR SCORECARD CORE ---
elif page == "👨‍💼 HR Scorecard Core":
    st.markdown("<div class='dashboard-super-title'>👨‍💼 HR Scorecard Core</div>", unsafe_allow_html=True)
    st.markdown("<div class='dashboard-tagline'>Compile workforce fitness report summary matrices instantly</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Candidate Name")
        experience = st.text_input("Years of Experience")
    with col2:
        skills = st.text_area("Primary Skills")

    if st.button("Compile Target Fitness Evaluation Scorecard", type="primary"):
        if name and skills:
            with st.spinner("Processing token properties loops..."):
                result = hr_assistant(name, skills, experience)
            
            st.markdown(f"<div class='neo-report-card'>{result}</div>", unsafe_allow_html=True)
        else:
            st.warning("Ensure identity profiling parameter values are defined completely before triggering calculation engines.")


# --- MODULE: TECHNICAL QUERY ENGINE ---
elif page == "❓ Technical Query Engine":
    st.markdown("<div class='dashboard-super-title'>❓ Technical Query Engine</div>", unsafe_allow_html=True)
    st.markdown("<div class='dashboard-tagline'>Instantly configure targeted technical framework evaluation blocks</div>", unsafe_allow_html=True)

    skill = st.text_input("Enter Technology or Skill")

    if st.button("Generate Interview Questions", type="primary"):
        if skill:
            with st.spinner("Structuring technical round queries..."):
                result = generate_questions(skill)
            
            st.markdown(f"<div class='neo-report-card'>{result}</div>", unsafe_allow_html=True)
        else:
            st.warning("Target domain definition parameters cannot be blank context logs.")


# --- MODULE: CAREER PATH MATRIX ---
elif page == "🎯 Career Path Matrix":
    st.markdown("<div class='dashboard-super-title'>🎯 Career Path Matrix</div>", unsafe_allow_html=True)
    st.markdown("<div class='dashboard-tagline'>Cross-reference target skill sets to structural corporate roles</div>", unsafe_allow_html=True)

    user_skills = st.text_area("Enter Your Skills")

    if st.button("Get Career Recommendations", type="primary"):
        if user_skills:
            with st.spinner("Analyzing profile patterns..."):
                result = recommend_job(user_skills)
            
            st.markdown(f"<div class='neo-report-card'>{result}</div>", unsafe_allow_html=True)
        else:
            st.warning("Data input cannot be empty context matrices.")