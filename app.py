import streamlit as st
import re
import csv
import io
from datetime import datetime
from typing import Optional, Tuple
import random

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

st.set_page_config(
    page_title="WizKlub - STEM Programs",
    page_icon="W",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# =============================================================================
# CSS - FULLY THEMED DARK + VIBRANT DESIGN
# =============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* ===== DARK THEME BASE ===== */
    .stApp {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(180deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
        min-height: 100vh;
    }

    /* Force all default text to light */
    .stApp, .stApp p, .stApp span, .stApp label, .stApp div,
    .stApp h1, .stApp h2, .stApp h3, .stMarkdownContainer p {
        color: #e2e8f0 !important;
    }

    /* ===== HEADER WITH GLOW ===== */
    .wz-header {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #a855f7 100%);
        padding: 2rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 0 40px rgba(124, 58, 237, 0.3);
        position: relative;
        overflow: hidden;
    }
    .wz-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(ellipse, rgba(255,255,255,0.08) 0%, transparent 70%);
        animation: headerGlow 6s ease-in-out infinite;
    }
    @keyframes headerGlow {
        0%, 100% { transform: translateX(-20%) translateY(-20%); }
        50% { transform: translateX(20%) translateY(20%); }
    }
    .wz-header h1 {
        color: #ffffff !important;
        font-size: 1.8rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.02em;
        position: relative;
        z-index: 1;
    }
    .wz-header p {
        color: rgba(255,255,255,0.85) !important;
        font-size: 0.95rem;
        margin: 0.4rem 0 0 0;
        position: relative;
        z-index: 1;
    }

    /* ===== STATS BAR ===== */
    .wz-stats {
        display: flex;
        gap: 0.6rem;
        margin: 0 0 1.5rem 0;
        justify-content: center;
        flex-wrap: wrap;
    }
    .wz-stat {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 0.7rem 1.1rem;
        text-align: center;
        min-width: 100px;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    .wz-stat:hover {
        background: rgba(255,255,255,0.1);
        border-color: rgba(124,58,237,0.5);
        transform: translateY(-2px);
    }
    .wz-stat-num {
        font-size: 1.15rem;
        font-weight: 800;
        color: #a78bfa !important;
        display: block;
    }
    .wz-stat-lbl {
        font-size: 0.6rem;
        color: #94a3b8 !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        display: block;
        margin-top: 0.1rem;
    }

    /* ===== STEP TRACKER ===== */
    .wz-steps {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0;
        margin: 1rem auto 0.4rem auto;
        max-width: 550px;
    }
    .wz-dot {
        width: 34px;
        height: 34px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.7rem;
        font-weight: 700;
        flex-shrink: 0;
        transition: all 0.3s ease;
    }
    .wz-dot.done {
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        color: white !important;
        box-shadow: 0 0 12px rgba(124,58,237,0.4);
    }
    .wz-dot.now {
        background: rgba(124,58,237,0.15);
        color: #a78bfa !important;
        border: 2.5px solid #7c3aed;
        box-shadow: 0 0 16px rgba(124,58,237,0.3);
        animation: dotPulse 2s ease-in-out infinite;
    }
    @keyframes dotPulse {
        0%, 100% { box-shadow: 0 0 16px rgba(124,58,237,0.3); }
        50% { box-shadow: 0 0 24px rgba(124,58,237,0.6); }
    }
    .wz-dot.later {
        background: rgba(255,255,255,0.06);
        color: #475569 !important;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .wz-line {
        height: 2px;
        flex-grow: 1;
        min-width: 10px;
        max-width: 35px;
        transition: all 0.3s ease;
    }
    .wz-line.done {
        background: linear-gradient(90deg, #4f46e5, #7c3aed);
        box-shadow: 0 0 6px rgba(124,58,237,0.3);
    }
    .wz-line.later {
        background: rgba(255,255,255,0.08);
    }
    .wz-step-info {
        text-align: center;
        margin: 0.5rem 0 1.25rem 0;
        font-size: 0.8rem;
        color: #94a3b8 !important;
    }
    .wz-step-info strong {
        color: #a78bfa !important;
        font-weight: 700;
    }

    /* ===== MESSAGE BUBBLES ===== */
    .wz-msg-bot {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 2px 18px 18px 18px;
        padding: 1rem 1.25rem;
        margin: 0.75rem 0;
        font-size: 0.9rem;
        line-height: 1.65;
        color: #e2e8f0 !important;
        max-width: 88%;
        backdrop-filter: blur(10px);
        position: relative;
    }
    .wz-msg-bot::before {
        content: 'W';
        position: absolute;
        top: -8px;
        left: -8px;
        width: 22px;
        height: 22px;
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.55rem;
        font-weight: 800;
        color: white !important;
        line-height: 22px;
        text-align: center;
    }
    .wz-msg-user {
        background: linear-gradient(135deg, #4f46e5, #6d28d9);
        color: white !important;
        border-radius: 18px 2px 18px 18px;
        padding: 0.75rem 1.25rem;
        margin: 0.5rem 0;
        font-size: 0.88rem;
        line-height: 1.5;
        max-width: 65%;
        margin-left: auto;
        text-align: right;
        box-shadow: 0 4px 16px rgba(79,70,229,0.25);
    }

    /* ===== ROLE CARDS ===== */
    .wz-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 1.75rem 1.25rem;
        text-align: center;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
        cursor: pointer;
    }
    .wz-card:hover {
        background: rgba(124,58,237,0.1);
        border-color: rgba(124,58,237,0.5);
        box-shadow: 0 0 30px rgba(124,58,237,0.15);
        transform: translateY(-3px);
    }
    .wz-card-icon {
        width: 50px;
        height: 50px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 0.75rem auto;
        font-size: 1.4rem;
        font-weight: 800;
    }
    .wz-card-icon.parent {
        background: linear-gradient(135deg, #3b82f6, #2563eb);
        color: white !important;
    }
    .wz-card-icon.school {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white !important;
    }
    .wz-card-title {
        font-size: 1rem;
        font-weight: 700;
        color: #f1f5f9 !important;
        margin-bottom: 0.3rem;
    }
    .wz-card-desc {
        font-size: 0.78rem;
        color: #94a3b8 !important;
    }

    /* ===== INPUT STYLING ===== */
    .stSelectbox > div > div,
    .stMultiSelect > div > div,
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.07) !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        color: #e2e8f0 !important;
        border-radius: 10px !important;
    }
    .stSelectbox > div > div:hover,
    .stMultiSelect > div > div:hover,
    .stTextInput > div > div > input:hover {
        border-color: rgba(124,58,237,0.5) !important;
    }
    .stSelectbox > div > div:focus-within,
    .stMultiSelect > div > div:focus-within,
    .stTextInput > div > div > input:focus {
        border-color: #7c3aed !important;
        box-shadow: 0 0 12px rgba(124,58,237,0.2) !important;
    }

    /* Selectbox dropdown text */
    .stSelectbox [data-baseweb="select"] span,
    .stSelectbox [data-baseweb="select"] div {
        color: #e2e8f0 !important;
    }

    /* Multiselect tags */
    .stMultiSelect [data-baseweb="tag"] {
        background: rgba(124,58,237,0.3) !important;
        color: #e2e8f0 !important;
        border: 1px solid rgba(124,58,237,0.5) !important;
        border-radius: 8px !important;
    }

    /* Radio buttons */
    .stRadio > div {
        background: rgba(255,255,255,0.03);
        border-radius: 12px;
        padding: 0.5rem;
    }
    .stRadio label {
        color: #e2e8f0 !important;
        padding: 0.4rem 0.5rem;
        border-radius: 8px;
        transition: all 0.2s ease;
    }
    .stRadio label:hover {
        background: rgba(124,58,237,0.1);
    }
    .stRadio [data-testid="stMarkdownContainer"] p {
        color: #e2e8f0 !important;
    }

    /* Input labels */
    .stSelectbox label, .stMultiSelect label, .stTextInput label,
    .stRadio label, .stTextInput span {
        color: #cbd5e1 !important;
        font-weight: 600;
        font-size: 0.85rem;
    }

    /* Input placeholder */
    .stTextInput input::placeholder {
        color: #64748b !important;
    }

    /* ===== BUTTONS ===== */
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        padding: 0.5rem 1.25rem;
        font-size: 0.85rem;
        transition: all 0.2s ease;
        border: none !important;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
    }

    /* Primary button */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
        color: white !important;
        box-shadow: 0 4px 16px rgba(124,58,237,0.3);
    }
    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 6px 24px rgba(124,58,237,0.5);
    }

    /* Secondary / default button */
    .stButton > button[kind="secondary"],
    .stButton > button:not([kind="primary"]) {
        background: rgba(255,255,255,0.08) !important;
        color: #e2e8f0 !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
    }
    .stButton > button[kind="secondary"]:hover,
    .stButton > button:not([kind="primary"]):hover {
        background: rgba(255,255,255,0.15) !important;
        border-color: rgba(124,58,237,0.4) !important;
    }

    /* ===== BADGES ===== */
    .wz-badge-high {
        background: linear-gradient(135deg, #059669, #10b981);
        color: white !important;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 700;
        display: inline-block;
        box-shadow: 0 0 16px rgba(16,185,129,0.3);
    }
    .wz-badge-med {
        background: linear-gradient(135deg, #d97706, #f59e0b);
        color: white !important;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 700;
        display: inline-block;
        box-shadow: 0 0 16px rgba(245,158,11,0.3);
    }
    .wz-badge-low {
        background: linear-gradient(135deg, #dc2626, #ef4444);
        color: white !important;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 700;
        display: inline-block;
        box-shadow: 0 0 16px rgba(239,68,68,0.3);
    }

    /* ===== URGENCY ===== */
    .wz-urgency {
        background: rgba(251,191,36,0.1);
        border: 1px solid rgba(251,191,36,0.3);
        border-radius: 12px;
        padding: 0.85rem 1.25rem;
        text-align: center;
        margin: 0.75rem 0;
        font-weight: 600;
        color: #fbbf24 !important;
        font-size: 0.85rem;
    }

    /* ===== SOCIAL PROOF ===== */
    .wz-proof {
        background: rgba(34,197,94,0.08);
        border-left: 3px solid #22c55e;
        padding: 0.7rem 1rem;
        margin: 0.5rem 0;
        font-size: 0.82rem;
        color: #86efac !important;
        border-radius: 0 10px 10px 0;
    }

    /* ===== TESTIMONIAL ===== */
    .wz-quote {
        background: rgba(139,92,246,0.08);
        border-left: 3px solid #8b5cf6;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        font-style: italic;
        color: #c4b5fd !important;
        font-size: 0.82rem;
        border-radius: 0 10px 10px 0;
    }

    /* ===== DONE CARD ===== */
    .wz-done {
        background: rgba(34,197,94,0.08);
        border: 1px solid rgba(34,197,94,0.25);
        border-radius: 14px;
        padding: 1.25rem;
        text-align: center;
        margin: 1rem 0;
    }
    .wz-done-title {
        font-size: 1.15rem;
        font-weight: 800;
        color: #4ade80 !important;
    }
    .wz-done-sub {
        font-size: 0.82rem;
        color: #86efac !important;
        margin-top: 0.2rem;
    }

    /* ===== WARNING ===== */
    .stAlert {
        background: rgba(251,191,36,0.1) !important;
        border: 1px solid rgba(251,191,36,0.3) !important;
        border-radius: 10px !important;
    }
    .stAlert p {
        color: #fbbf24 !important;
    }

    /* ===== FOOTER ===== */
    .wz-footer {
        text-align: center;
        padding: 1.5rem 0 1rem 0;
        font-size: 0.75rem;
    }
    .wz-footer p {
        color: #475569 !important;
    }
    .wz-footer a {
        color: #7c3aed !important;
        text-decoration: none;
    }

    /* ===== CHAT INPUT ===== */
    .stChatInput {
        background: transparent !important;
    }
    .stChatInput textarea {
        background: rgba(255,255,255,0.07) !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        color: #e2e8f0 !important;
        border-radius: 12px !important;
    }
    .stChatInput textarea:focus {
        border-color: #7c3aed !important;
    }

    /* ===== SIDEBAR ===== */
    section[data-testid="stSidebar"] {
        background: #1a1a2e !important;
    }
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #e2e8f0 !important;
    }
    section[data-testid="stSidebar"] [data-testid="stMetricValue"] {
        color: #a78bfa !important;
    }
    section[data-testid="stSidebar"] [data-testid="stMetricLabel"] p {
        color: #94a3b8 !important;
    }
    section[data-testid="stSidebar"] .stTextInput input {
        background: rgba(255,255,255,0.07) !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        color: #e2e8f0 !important;
    }
    section[data-testid="stSidebar"] .streamlit-expanderHeader {
        color: #e2e8f0 !important;
    }

    /* ===== DIVIDER ===== */
    hr {
        border-color: rgba(255,255,255,0.08) !important;
    }

    /* ===== HIDE DEFAULTS ===== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .block-container {
        padding-top: 2rem;
        max-width: 720px;
    }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# CONSTANTS
# =============================================================================

PARENT_GRADES = ["Pre-K / KG","Grade 1","Grade 2","Grade 3","Grade 4","Grade 5",
                 "Grade 6","Grade 7","Grade 8","Grade 9","Grade 10","Grade 11","Grade 12"]

LEARNING_GOALS = ["Critical Thinking and Problem Solving","Coding and Programming",
    "Science and Experimentation","Mathematics Excellence","Creative and Design Thinking",
    "Competition Preparation (Olympiad etc.)","Overall Academic Improvement",
    "AI and Robotics","Focus and Concentration","Other"]

CHALLENGES = ["Child lacks interest in studies","Difficulty in problem-solving",
    "Too much screen time (unproductive)","Not performing well in school",
    "Wants to learn beyond school curriculum","Looking for structured STEM program",
    "Child is gifted and needs advanced content","Other"]

SCHOOL_TYPES = ["CBSE","ICSE","State Board","International (IB/Cambridge)",
    "Private","Government","Montessori","Other"]

STUDENT_RANGES = ["Less than 100","100 - 300","300 - 500","500 - 1000",
    "1000 - 2000","2000 - 5000","5000+"]

DECISION_TIMELINES = ["Immediately (within 1 month)","This quarter (1-3 months)",
    "Next academic session","Just exploring options"]

BUDGET_OPTIONS = ["Not a concern - want the best for my child",
    "Moderate - value for money matters","Tight budget - looking for affordable options",
    "Need to discuss with family first"]

SOCIAL_PROOFS = ["Over 50,000 students across India learn with WizKlub.",
    "3x improvement in logical thinking within 3 months.",
    "98% of parents recommend WizKlub.","500+ schools across 15 cities trust WizKlub.",
    "40% higher scores in competitive exams."]

URGENCY_MESSAGES = ["Limited slots this month. Book your free demo today.",
    "Free assessment worth Rs.999 when you book this week.",
    "Only 5 demo slots left for your area.",
    "First month FREE for demos booked before month-end."]

TIER1_CITIES = ["bangalore","mumbai","delhi","hyderabad","chennai",
    "pune","kolkata","bengaluru","noida","gurgaon","gurugram"]

PARENT_STEP_IDS = ["parent_grade","parent_goals","parent_challenges","parent_city",
    "parent_budget","lead_capture_name","lead_capture_email","lead_capture_phone"]

SCHOOL_STEP_IDS = ["school_name","school_students","school_type","school_timeline",
    "school_city","lead_capture_name","lead_capture_email","lead_capture_phone"]

PARENT_STAGES = ["role_selection"] + PARENT_STEP_IDS
SCHOOL_STAGES = ["role_selection"] + SCHOOL_STEP_IDS

STEP_INFO = {
    "parent_grade":"Step 1 of 8 -- Select your child's grade",
    "parent_goals":"Step 2 of 8 -- What should your child learn?",
    "parent_challenges":"Step 3 of 8 -- Current challenges",
    "parent_city":"Step 4 of 8 -- Your location",
    "parent_budget":"Step 5 of 8 -- Budget preference",
    "lead_capture_name":"Step 6 of 8 -- Your name",
    "lead_capture_email":"Step 7 of 8 -- Your email",
    "lead_capture_phone":"Step 8 of 8 -- Your phone",
    "school_name":"Step 1 of 8 -- School name",
    "school_students":"Step 2 of 8 -- Student count",
    "school_type":"Step 3 of 8 -- Board type",
    "school_timeline":"Step 4 of 8 -- Timeline",
    "school_city":"Step 5 of 8 -- Location",
}


# =============================================================================
# SESSION STATE
# =============================================================================

def init_session_state():
    defaults = {
        "messages":[],"current_stage":"welcome","user_type":None,
        "conversation_started":False,"qualification_complete":False,
        "parent_data":{"grade":None,"learning_goals":[],"challenges":[],
                       "city":None,"budget_sensitivity":None},
        "school_data":{"school_name":None,"student_count":None,
                       "school_type":None,"decision_timeline":None,"city":None},
        "lead_data":{"name":None,"email":None,"phone":None},
        "lead_score":0,"lead_intent":"Unknown",
        "metrics":{"total_conversations":0,"leads_captured":0,"demo_requests":0,
                   "high_intent_count":0,"medium_intent_count":0,"low_intent_count":0},
        "leads_database":[],"show_admin":False,"demo_booked":False,
        "openai_key":None,"use_ai":False,
    }
    for k,v in defaults.items():
        if k not in st.session_state: st.session_state[k]=v

init_session_state()


# =============================================================================
# RENDERERS
# =============================================================================

def render_messages():
    for msg in st.session_state.messages:
        c = msg["content"].replace("\n","<br>")
        if msg["role"]=="assistant":
            st.markdown(f'<div class="wz-msg-bot">{c}</div>',unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="wz-msg-user">{c}</div>',unsafe_allow_html=True)


def render_steps():
    stage = st.session_state.current_stage
    ut = st.session_state.user_type
    if stage in ("welcome","role_selection","completed","free_chat"): return
    ids = PARENT_STEP_IDS if ut=="parent" else SCHOOL_STEP_IDS if ut=="school" else None
    if not ids: return
    stages = PARENT_STAGES if ut=="parent" else SCHOOL_STAGES
    ci = stages.index(stage)-1 if stage in stages else 0

    dots=""
    for i in range(len(ids)):
        if i<ci: dots+=f'<div class="wz-dot done">&#10003;</div>'
        elif i==ci: dots+=f'<div class="wz-dot now">{i+1}</div>'
        else: dots+=f'<div class="wz-dot later">{i+1}</div>'
        if i<len(ids)-1:
            dots+=f'<div class="wz-line {"done" if i<ci else "later"}"></div>'

    st.markdown(f'<div class="wz-steps">{dots}</div>',unsafe_allow_html=True)
    if stage in STEP_INFO:
        st.markdown(f'<div class="wz-step-info"><strong>{STEP_INFO[stage]}</strong></div>',
                    unsafe_allow_html=True)


def render_stats():
    if st.session_state.current_stage in ("welcome","role_selection"):
        st.markdown("""<div class="wz-stats">
            <div class="wz-stat"><span class="wz-stat-num">50,000+</span><span class="wz-stat-lbl">Students</span></div>
            <div class="wz-stat"><span class="wz-stat-num">500+</span><span class="wz-stat-lbl">Schools</span></div>
            <div class="wz-stat"><span class="wz-stat-num">15+</span><span class="wz-stat-lbl">Cities</span></div>
            <div class="wz-stat"><span class="wz-stat-num">98%</span><span class="wz-stat-lbl">Approval</span></div>
        </div>""",unsafe_allow_html=True)


# =============================================================================
# NAVIGATION
# =============================================================================

def go_back():
    s = st.session_state.current_stage
    ut = st.session_state.user_type
    stages = PARENT_STAGES if ut=="parent" else SCHOOL_STAGES if ut=="school" else ["role_selection"]
    if s in stages:
        i = stages.index(s)
        if i>0:
            p = stages[i-1]
            if len(st.session_state.messages)>=2:
                st.session_state.messages.pop(); st.session_state.messages.pop()
            elif st.session_state.messages: st.session_state.messages.pop()
            clear_data(s)
            if p=="role_selection":
                st.session_state.user_type=None
                if len(st.session_state.messages)>=2:
                    st.session_state.messages.pop(); st.session_state.messages.pop()
            st.session_state.current_stage=p
        else: reset_all()
    else: reset_all()


def clear_data(s):
    m={"parent_grade":("parent_data","grade",None),"parent_goals":("parent_data","learning_goals",[]),
       "parent_challenges":("parent_data","challenges",[]),"parent_city":("parent_data","city",None),
       "parent_budget":("parent_data","budget_sensitivity",None),
       "school_name":("school_data","school_name",None),"school_students":("school_data","student_count",None),
       "school_type":("school_data","school_type",None),"school_timeline":("school_data","decision_timeline",None),
       "school_city":("school_data","city",None),"lead_capture_name":("lead_data","name",None),
       "lead_capture_email":("lead_data","email",None),"lead_capture_phone":("lead_data","phone",None)}
    if s in m: c,k,d=m[s]; st.session_state[c][k]=d


def reset_all():
    keep={k:st.session_state.get(k) for k in ["leads_database","metrics","openai_key","use_ai","show_admin"]}
    for k in ["messages","current_stage","user_type","conversation_started","qualification_complete",
              "parent_data","school_data","lead_data","lead_score","lead_intent","demo_booked"]:
        if k in st.session_state: del st.session_state[k]
    for k,v in keep.items():
        if v is not None: st.session_state[k]=v
    init_session_state()


# =============================================================================
# HELPERS
# =============================================================================

def validate_email(e): return bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',e.strip()))
def validate_phone(p):
    c=re.sub(r'[\s\-\(\)\+]','',p.strip())
    return (c.startswith('91') and len(c)==12) or (len(c)==10 and c.isdigit())
def format_phone(p):
    c=re.sub(r'[\s\-\(\)\+]','',p.strip())
    if len(c)==10: return f"+91-{c}"
    if c.startswith('91') and len(c)==12: return f"+{c[:2]}-{c[2:]}"
    return p.strip()
def ts(): return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
def bot(c): st.session_state.messages.append({"role":"assistant","content":c,"timestamp":ts()})
def usr(c): st.session_state.messages.append({"role":"user","content":c,"timestamp":ts()})
def proof(): return random.choice(SOCIAL_PROOFS)
def urgency(): return random.choice(URGENCY_MESSAGES)
def grade_num(s):
    if not s: return None
    m=re.search(r'\d+',s)
    if m: return int(m.group())
    if "pre" in s.lower() or "kg" in s.lower(): return 0
    return None
def student_num(s):
    return {"Less than 100":50,"100 - 300":200,"300 - 500":400,"500 - 1000":750,
            "1000 - 2000":1500,"2000 - 5000":3500,"5000+":6000}.get(s,0)
def tier1(c): return any(x in c.lower() for x in TIER1_CITIES) if c else False


# =============================================================================
# LEAD SCORING
# =============================================================================

def calc_score():
    s=0
    if st.session_state.user_type=="parent":
        d=st.session_state.parent_data
        gn=grade_num(d.get("grade",""))
        if gn is not None:
            if 3<=gn<=8:s+=25
            elif 1<=gn<=2:s+=15
            elif 9<=gn<=10:s+=18
            else:s+=8
        for g in d.get("learning_goals",[]):
            if any(k in g.lower() for k in ["critical thinking","coding","competition","ai and robotics","problem solving"]):s+=8
            else:s+=4
        if len(d.get("learning_goals",[]))>=3:s+=5
        for c in d.get("challenges",[]):
            if any(k in c.lower() for k in ["lacks interest","problem-solving","not performing","gifted","beyond school"]):s+=7
            else:s+=3
        if tier1(d.get("city","")):s+=10
        elif d.get("city"):s+=5
        b=d.get("budget_sensitivity","")
        if "not a concern" in b.lower():s+=10
        elif "moderate" in b.lower():s+=6
        elif "tight" in b.lower():s+=2
        elif b:s+=3
    elif st.session_state.user_type=="school":
        d=st.session_state.school_data
        sn=student_num(d.get("student_count",""))
        if sn>=2000:s+=30
        elif sn>=1000:s+=25
        elif sn>=500:s+=20
        elif sn>=300:s+=15
        elif sn>=100:s+=10
        else:s+=5
        if any(t in d.get("school_type","").lower() for t in ["international","ib","cambridge","private","icse"]):s+=15
        else:s+=8
        tl=d.get("decision_timeline","")
        if "immediately" in tl.lower() or "1 month" in tl.lower():s+=30
        elif "quarter" in tl.lower():s+=20
        elif "next" in tl.lower():s+=10
        elif "exploring" in tl.lower():s+=5
        if d.get("school_name"):s+=5
        if tier1(d.get("city","")):s+=8
        elif d.get("city"):s+=4
    ld=st.session_state.lead_data
    if ld.get("name"):s+=3
    if ld.get("email"):s+=5
    if ld.get("phone"):s+=5
    s=min(s,100)
    return s,("High Intent" if s>=70 else "Medium Intent" if s>=40 else "Low Intent")


def save_lead():
    sc,intent=calc_score()
    st.session_state.lead_score=sc; st.session_state.lead_intent=intent
    lead={"timestamp":ts(),"user_type":st.session_state.user_type,
          "name":st.session_state.lead_data.get("name",""),
          "email":st.session_state.lead_data.get("email",""),
          "phone":st.session_state.lead_data.get("phone",""),
          "score":sc,"intent":intent,"demo_booked":False}
    if st.session_state.user_type=="parent":
        lead.update({"grade":st.session_state.parent_data.get("grade",""),
            "learning_goals":", ".join(st.session_state.parent_data.get("learning_goals",[])),
            "challenges":", ".join(st.session_state.parent_data.get("challenges",[])),
            "city":st.session_state.parent_data.get("city",""),
            "budget_sensitivity":st.session_state.parent_data.get("budget_sensitivity","")})
    else:
        lead.update({"school_name":st.session_state.school_data.get("school_name",""),
            "student_count":st.session_state.school_data.get("student_count",""),
            "school_type":st.session_state.school_data.get("school_type",""),
            "decision_timeline":st.session_state.school_data.get("decision_timeline",""),
            "city":st.session_state.school_data.get("city","")})
    st.session_state.leads_database.append(lead)
    st.session_state.metrics["leads_captured"]+=1
    if "High" in intent:st.session_state.metrics["high_intent_count"]+=1
    elif "Medium" in intent:st.session_state.metrics["medium_intent_count"]+=1
    else:st.session_state.metrics["low_intent_count"]+=1

def export_csv():
    if not st.session_state.leads_database: return ""
    o=io.StringIO()
    w=csv.DictWriter(o,fieldnames=list(st.session_state.leads_database[0].keys()))
    w.writeheader()
    for l in st.session_state.leads_database:w.writerow(l)
    return o.getvalue()


# =============================================================================
# CONVERSATION
# =============================================================================

def do_welcome():
    if not st.session_state.conversation_started:
        st.session_state.conversation_started=True
        st.session_state.metrics["total_conversations"]+=1
        bot("Welcome to WizKlub!\n\nI will help you find the perfect STEM program.\nPlease tell me who you are:")
        st.session_state.current_stage="role_selection"

def do_role(r):
    st.session_state.user_type=r
    if r=="parent":
        usr("I am a Parent"); bot("Great. Let me find the best program for your child.\n\nWhat grade is your child in?")
        st.session_state.current_stage="parent_grade"
    else:
        usr("I represent a School"); bot("Excellent. WizKlub partners with 500+ schools.\n\nWhat is your school name?")
        st.session_state.current_stage="school_name"

def do_parent(inp=None,sel=None):
    s=st.session_state.current_stage
    if s=="parent_grade" and sel:
        st.session_state.parent_data["grade"]=sel; usr(sel)
        gn=grade_num(sel)
        bot(f"{sel} is {'a golden period for critical thinking' if gn and 3<=gn<=8 else 'a great time to build foundations'}.\n\nWhat are your child's learning goals?")
        st.session_state.current_stage="parent_goals"
    elif s=="parent_goals" and sel:
        st.session_state.parent_data["learning_goals"]=sel; usr(", ".join(sel))
        bot(f"Excellent choices. {proof()}\n\nWhat challenges is your child facing?")
        st.session_state.current_stage="parent_challenges"
    elif s=="parent_challenges" and sel:
        st.session_state.parent_data["challenges"]=sel; usr(", ".join(sel))
        bot("Understood. Our programs address these with proven results.\n\nWhich city are you in?")
        st.session_state.current_stage="parent_city"
    elif s=="parent_city" and inp:
        st.session_state.parent_data["city"]=inp.strip(); usr(inp.strip())
        bot(f"We have learners in {inp.strip()}.\n\nWhat is your budget preference?")
        st.session_state.current_stage="parent_budget"
    elif s=="parent_budget" and sel:
        st.session_state.parent_data["budget_sensitivity"]=sel; usr(sel)
        bot("Thank you. Almost done.\n\nWhat is your name?")
        st.session_state.current_stage="lead_capture_name"

def do_school(inp=None,sel=None):
    s=st.session_state.current_stage
    if s=="school_name" and inp:
        st.session_state.school_data["school_name"]=inp.strip(); usr(inp.strip())
        bot(f"Great to connect with {inp.strip()}.\n\nHow many students?")
        st.session_state.current_stage="school_students"
    elif s=="school_students" and sel:
        st.session_state.school_data["student_count"]=sel; usr(sel)
        n=student_num(sel)
        bot(f"Excellent.{' Schools your size see 35% improvement.' if n>=500 else ''}\n\nWhat board?")
        st.session_state.current_stage="school_type"
    elif s=="school_type" and sel:
        st.session_state.school_data["school_type"]=sel; usr(sel)
        bot("Modules ready for your board.\n\nImplementation timeline?")
        st.session_state.current_stage="school_timeline"
    elif s=="school_timeline" and sel:
        st.session_state.school_data["decision_timeline"]=sel; usr(sel)
        u=" Special packages this quarter." if "immediately" in sel.lower() or "quarter" in sel.lower() else ""
        bot(f"Noted.{u}\n\nSchool city?"); st.session_state.current_stage="school_city"
    elif s=="school_city" and inp:
        st.session_state.school_data["city"]=inp.strip(); usr(inp.strip())
        bot("Perfect. Connecting you with our team.\n\nYour name?")
        st.session_state.current_stage="lead_capture_name"

def do_lead(inp):
    s=st.session_state.current_stage
    if s=="lead_capture_name":
        if inp and len(inp.strip())>=2:
            st.session_state.lead_data["name"]=inp.strip(); usr(inp.strip())
            bot(f"Nice to meet you, {inp.strip().split()[0]}.\n\nYour email?")
            st.session_state.current_stage="lead_capture_email"
        else: bot("Please enter at least 2 characters.")
    elif s=="lead_capture_email":
        if inp and validate_email(inp):
            st.session_state.lead_data["email"]=inp.strip(); usr(inp.strip())
            bot("Got it.\n\nPhone number?"); st.session_state.current_stage="lead_capture_phone"
        else: bot("Invalid email. Example: name@email.com")
    elif s=="lead_capture_phone":
        if inp and validate_phone(inp):
            st.session_state.lead_data["phone"]=format_phone(inp); usr(format_phone(inp))
            save_lead(); st.session_state.qualification_complete=True
            st.session_state.current_stage="conversion_offer"; do_offer()
        else: bot("Invalid phone. Example: 9876543210")

def do_offer():
    sc=st.session_state.lead_score; intent=st.session_state.lead_intent
    nm=st.session_state.lead_data.get("name","").split()[0]; ut=st.session_state.user_type
    if "High" in intent:
        if ut=="parent":
            gr=st.session_state.parent_data.get("grade","")
            bot(f"Fantastic, {nm}. Your child is a great match.\n\nRecommended: {gr} STEM Excellence Program\n\n"
                f"FREE Demo includes:\n-- 45-min interactive session\n-- Assessment worth Rs.999\n"
                f"-- Expert consultation\n-- Custom roadmap\n\n{urgency()}")
        else:
            sn=st.session_state.school_data.get("school_name","your school")
            bot(f"Wonderful, {nm}. {sn} is a great fit.\n\nWe offer:\n-- Free pilot for 2 classes\n"
                f"-- ROI projection\n-- Custom curriculum\n-- Teacher training\n\nOur Director will call within 24 hours.")
    elif "Medium" in intent:
        bot(f"Thank you, {nm}.\n\n1. Book a free demo\n2. Request callback\n3. Get brochure\n\n{proof()}")
    else:
        bot(f"Thank you, {nm}. We will send our brochure.\n\n{proof()}")
    st.session_state.current_stage="completed"

def do_chat(inp):
    usr(inp)
    faq={"price":"Pricing varies. Book a demo for details.","cost":"Pricing varies. Book a demo.",
         "schedule":"Flexible weekday and weekend.","online":"Both online and offline.",
         "offline":"Centers in Bangalore, Mumbai, Delhi.","different":"Thinking skills, not rote learning.",
         "tuition":"Not tuition. Core thinking skills.","age":"Pre-K to Grade 12.",
         "result":"Improvement within 3 months."}
    r=None
    for k,v in faq.items():
        if k in inp.lower():r=v;break
    bot(r or "Great question. Book a demo or request a callback?")


# =============================================================================
# ADMIN
# =============================================================================

def do_admin():
    with st.sidebar:
        st.markdown("### Admin Dashboard")
        pw=st.text_input("Password",type="password",key="adm_pw")
        if pw=="wizklub2024":st.session_state.show_admin=True
        elif pw:st.warning("Wrong password");st.session_state.show_admin=False
        if not st.session_state.show_admin:return
        st.markdown("---")
        m=st.session_state.metrics;tl=m["leads_captured"]
        c1,c2=st.columns(2)
        with c1:st.metric("Chats",m["total_conversations"]);st.metric("High",m["high_intent_count"])
        with c2:st.metric("Leads",tl);st.metric("Med",m["medium_intent_count"])
        if m["total_conversations"]>0:st.metric("Conv%",f"{(tl/m['total_conversations'])*100:.1f}%")
        st.metric("Demos",m["demo_requests"]);st.metric("Low",m["low_intent_count"])
        if st.session_state.leads_database:
            st.markdown("---")
            for l in reversed(st.session_state.leads_database):
                tag="[H]" if "High" in l["intent"] else "[M]" if "Medium" in l["intent"] else "[L]"
                with st.expander(f"{tag} {l['name']} - {l['score']}"):
                    st.write(f"**{l['user_type'].title()}** | {l['email']} | {l['phone']}")
                    st.write(f"**Demo:** {'Yes' if l['demo_booked'] else 'No'} | {l['timestamp']}")
            cd=export_csv()
            if cd:st.download_button("Download CSV",cd,f"leads_{datetime.now().strftime('%Y%m%d')}.csv","text/csv",use_container_width=True)
        st.markdown("---")
        ak=st.text_input("OpenAI Key",type="password",key="ai_k")
        if ak:st.session_state.openai_key=ak;st.session_state.use_ai=True
        else:st.session_state.use_ai=False
        if st.button("Reset All",use_container_width=True):
            for k in list(st.session_state.keys()):del st.session_state[k]
            st.rerun()


# =============================================================================
# ACTIONS
# =============================================================================

def show_actions():
    intent=st.session_state.lead_intent;sc=st.session_state.lead_score
    st.markdown('<div class="wz-done"><div class="wz-done-title">All Done</div>'
                '<div class="wz-done-sub">Your personalized recommendation</div></div>',unsafe_allow_html=True)
    if "High" in intent:bc,lb="wz-badge-high",f"HIGH INTENT -- Score: {sc}/100"
    elif "Medium" in intent:bc,lb="wz-badge-med",f"MEDIUM INTENT -- Score: {sc}/100"
    else:bc,lb="wz-badge-low",f"EXPLORING -- Score: {sc}/100"
    st.markdown(f'<div style="text-align:center;margin:0.75rem 0"><span class="{bc}">{lb}</span></div>',unsafe_allow_html=True)

    if "High" in intent:
        st.markdown(f'<div class="wz-urgency">{urgency()}</div>',unsafe_allow_html=True)
        c1,c2=st.columns(2)
        with c1:
            if st.button("Book FREE Demo",use_container_width=True,type="primary",key="d_h"):
                st.session_state.demo_booked=True;st.session_state.metrics["demo_requests"]+=1
                if st.session_state.leads_database:st.session_state.leads_database[-1]["demo_booked"]=True
                n=st.session_state.lead_data["name"].split()[0];e=st.session_state.lead_data["email"];p=st.session_state.lead_data["phone"]
                bot(f"Demo Confirmed!\n\n{n}, details:\nLink: https://calendly.com/wizklub-demo\nEmail: {e}\nPhone: {p}\n\nSee you soon.");st.rerun()
        with c2:
            if st.button("Request Callback",use_container_width=True,key="c_h"):
                bot(f"We will call {st.session_state.lead_data['phone']} within 2 hours.");st.rerun()
    elif "Medium" in intent:
        c1,c2,c3=st.columns(3)
        with c1:
            if st.button("Book Demo",use_container_width=True,type="primary",key="d_m"):
                st.session_state.demo_booked=True;st.session_state.metrics["demo_requests"]+=1
                if st.session_state.leads_database:st.session_state.leads_database[-1]["demo_booked"]=True
                bot("Demo: https://calendly.com/wizklub-demo");st.rerun()
        with c2:
            if st.button("Callback",use_container_width=True,key="c_m"):
                bot(f"Calling {st.session_state.lead_data['phone']} within 24h.");st.rerun()
        with c3:
            if st.button("Brochure",use_container_width=True,key="b_m"):
                bot(f"Sent to {st.session_state.lead_data['email']}.");st.rerun()
    else:
        c1,c2=st.columns(2)
        with c1:
            if st.button("Get Brochure",use_container_width=True,type="primary",key="b_l"):
                bot(f"Sent to {st.session_state.lead_data['email']}.\n\n{proof()}");st.rerun()
        with c2:
            if st.button("Ask Question",use_container_width=True,key="q_l"):
                bot("What would you like to know?");st.session_state.current_stage="free_chat";st.rerun()
    if not st.session_state.demo_booked:
        st.markdown(f'<div class="wz-proof">{proof()}</div>',unsafe_allow_html=True)
        st.markdown('<div class="wz-quote">"My daughter now solves puzzles for fun. Magical."'
                    '<br><strong>-- Anita R., Bangalore</strong></div>',unsafe_allow_html=True)


# =============================================================================
# STAGE UI
# =============================================================================

def show_ui():
    s=st.session_state.current_stage

    if s not in ("welcome","role_selection","completed","free_chat"):
        c1,c2,c3=st.columns([1,1,4])
        with c1:
            if st.button("< Back",key="bk"): go_back();st.rerun()
        with c2:
            if st.button("Restart",key="rs"): reset_all();st.rerun()

    if s=="role_selection":
        c1,c2=st.columns(2)
        with c1:
            st.markdown('<div class="wz-card"><div class="wz-card-icon parent">P</div>'
                        '<div class="wz-card-title">I am a Parent</div>'
                        '<div class="wz-card-desc">Find STEM programs for my child</div></div>',unsafe_allow_html=True)
            if st.button("Select Parent",use_container_width=True,type="primary",key="rp"):do_role("parent");st.rerun()
        with c2:
            st.markdown('<div class="wz-card"><div class="wz-card-icon school">S</div>'
                        '<div class="wz-card-title">I represent a School</div>'
                        '<div class="wz-card-desc">Explore partnership programs</div></div>',unsafe_allow_html=True)
            if st.button("Select School",use_container_width=True,key="rs2"):do_role("school");st.rerun()

    elif s=="parent_grade":
        v=st.selectbox("Child's grade:",["-- Select --"]+PARENT_GRADES,key="pg")
        if st.button("Continue",type="primary",key="pgb"):
            if v!="-- Select --":do_parent(sel=v);st.rerun()
            else:st.warning("Select a grade.")
    elif s=="parent_goals":
        v=st.multiselect("Learning goals:",LEARNING_GOALS,key="pgl")
        if st.button("Continue",type="primary",key="pglb"):
            if v:do_parent(sel=v);st.rerun()
            else:st.warning("Select at least one.")
    elif s=="parent_challenges":
        v=st.multiselect("Challenges:",CHALLENGES,key="pc")
        if st.button("Continue",type="primary",key="pcb"):
            if v:do_parent(sel=v);st.rerun()
            else:st.warning("Select at least one.")
    elif s=="parent_city":
        v=st.text_input("Your city:",key="pci",placeholder="e.g., Bangalore")
        if st.button("Continue",type="primary",key="pcib"):
            if v and len(v.strip())>=2:do_parent(inp=v);st.rerun()
            else:st.warning("Enter city.")
    elif s=="parent_budget":
        v=st.radio("Budget preference:",BUDGET_OPTIONS,key="pb")
        if st.button("Continue",type="primary",key="pbb"):
            if v:do_parent(sel=v);st.rerun()
    elif s=="school_name":
        v=st.text_input("School name:",key="sni",placeholder="e.g., Delhi Public School")
        if st.button("Continue",type="primary",key="snb"):
            if v and len(v.strip())>=2:do_school(inp=v);st.rerun()
            else:st.warning("Enter school name.")
    elif s=="school_students":
        v=st.selectbox("Students:",["-- Select --"]+STUDENT_RANGES,key="ssi")
        if st.button("Continue",type="primary",key="ssb"):
            if v!="-- Select --":do_school(sel=v);st.rerun()
            else:st.warning("Select count.")
    elif s=="school_type":
        v=st.selectbox("Board:",["-- Select --"]+SCHOOL_TYPES,key="sti")
        if st.button("Continue",type="primary",key="stb"):
            if v!="-- Select --":do_school(sel=v);st.rerun()
            else:st.warning("Select type.")
    elif s=="school_timeline":
        v=st.radio("Timeline:",DECISION_TIMELINES,key="tli")
        if st.button("Continue",type="primary",key="tlb"):
            if v:do_school(sel=v);st.rerun()
    elif s=="school_city":
        v=st.text_input("City:",key="sci",placeholder="e.g., Mumbai")
        if st.button("Continue",type="primary",key="scb"):
            if v and len(v.strip())>=2:do_school(inp=v);st.rerun()
            else:st.warning("Enter city.")
    elif s=="lead_capture_name":
        v=st.text_input("Your name:",key="ni",placeholder="e.g., Priya Sharma")
        if st.button("Continue",type="primary",key="nb"):
            if v:do_lead(v);st.rerun()
    elif s=="lead_capture_email":
        v=st.text_input("Email:",key="ei",placeholder="e.g., priya@email.com")
        if st.button("Continue",type="primary",key="eb"):
            if v:do_lead(v);st.rerun()
    elif s=="lead_capture_phone":
        v=st.text_input("Phone:",key="pi",placeholder="e.g., 9876543210")
        if st.button("Continue",type="primary",key="ppb"):
            if v:do_lead(v);st.rerun()
    elif s=="completed":
        show_actions()


# =============================================================================
# MAIN
# =============================================================================

def main():
    do_admin()
    st.markdown('<div class="wz-header"><h1>WizKlub</h1>'
                '<p>Personalized STEM Programs for Children and Schools</p></div>',unsafe_allow_html=True)
    render_stats()
    render_steps()
    do_welcome()
    render_messages()
    show_ui()
    if st.session_state.current_stage=="free_chat":
        v=st.chat_input("Ask anything...",key="fi")
        if v:do_chat(v);st.rerun()
    if st.session_state.current_stage in ("completed","free_chat"):
        st.markdown("---")
        if st.button("Start New Conversation",use_container_width=True,key="nc"):reset_all();st.rerun()
    st.markdown('<div class="wz-footer"><p>WizKlub | <a href="https://wizklub.com">wizklub.com</a> | '
                'hello@wizklub.com | 1800-XXX-XXXX</p></div>',unsafe_allow_html=True)

if __name__=="__main__":
    main()