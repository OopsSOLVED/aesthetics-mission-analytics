"""
╔══════════════════════════════════════════════════════════════════════════════╗
║          AESTHETICS MISSION Interior Designing Company                      ║
║          Business Analytics Dashboard                                      ║
║                                                                            ║
║  Requirements:  pip install -r requirements.txt                            ║
║  Run:           streamlit run app.py                                       ║
║  Optional GPU:  pip install diffusers[torch] transformers torch            ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# ─────────────────────────────────────────────────────────────────────────────
# IMPORTS
# ─────────────────────────────────────────────────────────────────────────────
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster, HeatMap
import yaml
import streamlit_authenticator as stauth
from datetime import datetime, timedelta
import warnings
import io
import base64
import calendar

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AESTHETICS MISSION | Business Analytics",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM CSS – GLOBAL STYLES
# ─────────────────────────────────────────────────────────────────────────────
GLOBAL_CSS = """
<style>
    /* ── Google Fonts ─────────────────────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Outfit:wght@300;400;500;600;700;800&display=swap');

    /* ── Root Variables ───────────────────────────────────────────────────── */
    :root {
        --primary: #667eea;
        --secondary: #764ba2;
        --accent: #f093fb;
        --success: #2ecc71;
        --danger: #e74c3c;
        --warning: #f39c12;
        --info: #3498db;
        --dark-bg: #0f0f23;
        --card-bg: rgba(255,255,255,0.06);
        --glass: rgba(255,255,255,0.08);
        --text-primary: #ffffff;
        --text-secondary: #b8b8d0;
        --gradient-1: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --gradient-2: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --gradient-3: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --gradient-4: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        --gradient-5: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        --gradient-6: linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%);
    }

    /* ── Global Styles ────────────────────────────────────────────────────── */
    .stApp {
        font-family: 'Inter', sans-serif;
    }

    /* ── Hide default Streamlit elements ──────────────────────────────────── */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ── Sidebar ──────────────────────────────────────────────────────────── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        border-right: 1px solid rgba(102, 126, 234, 0.3);
    }

    [data-testid="stSidebar"] .stMarkdown {
        color: #e0e0ff;
    }

    /* ── Metric Cards ─────────────────────────────────────────────────────── */
    .metric-card {
        background: var(--card-bg);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 20px;
        padding: 24px;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }

    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        border-radius: 20px 20px 0 0;
    }

    .metric-card:hover {
        transform: translateY(-6px);
        border-color: rgba(102, 126, 234, 0.5);
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.2);
    }

    .metric-card .metric-icon {
        font-size: 2.5rem;
        margin-bottom: 8px;
    }

    .metric-card .metric-value {
        font-family: 'Outfit', sans-serif;
        font-size: 2.2rem;
        font-weight: 800;
        background: var(--gradient-1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 4px 0;
    }

    .metric-card .metric-label {
        font-size: 0.9rem;
        color: var(--text-secondary);
        font-weight: 500;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }

    /* ── Gradient Cards for different metrics ─────────────────────────────── */
    .grad-1::before { background: var(--gradient-1); }
    .grad-2::before { background: var(--gradient-2); }
    .grad-3::before { background: var(--gradient-3); }
    .grad-4::before { background: var(--gradient-4); }

    .grad-1 .metric-value { background: var(--gradient-1); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .grad-2 .metric-value { background: var(--gradient-2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .grad-3 .metric-value { background: var(--gradient-3); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .grad-4 .metric-value { background: var(--gradient-4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }

    /* ── Section Headers ──────────────────────────────────────────────────── */
    .section-header {
        font-family: 'Outfit', sans-serif;
        font-size: 1.6rem;
        font-weight: 700;
        background: var(--gradient-1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 30px 0 15px 0;
        padding-bottom: 10px;
        border-bottom: 2px solid rgba(102, 126, 234, 0.3);
    }

    /* ── Insight Box ──────────────────────────────────────────────────────── */
    .insight-box {
        background: linear-gradient(135deg, rgba(102,126,234,0.15), rgba(118,75,162,0.15));
        border: 1px solid rgba(102,126,234,0.3);
        border-left: 4px solid #667eea;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        font-size: 1rem;
        line-height: 1.7;
        color: #e0e0ff;
    }

    .insight-box strong {
        color: #f093fb;
    }

    /* ── Dashboard Header ─────────────────────────────────────────────────── */
    .dashboard-header {
        background: var(--gradient-1);
        border-radius: 20px;
        padding: 30px 40px;
        margin-bottom: 25px;
        position: relative;
        overflow: hidden;
    }

    .dashboard-header::after {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 300px;
        height: 300px;
        border-radius: 50%;
        background: rgba(255,255,255,0.08);
    }

    .dashboard-header h1 {
        font-family: 'Outfit', sans-serif;
        color: white;
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
    }

    .dashboard-header p {
        color: rgba(255,255,255,0.85);
        font-size: 1rem;
        margin: 5px 0 0 0;
    }

    /* ── Tabs ──────────────────────────────────────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255,255,255,0.03);
        padding: 8px;
        border-radius: 16px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
    }

    /* ── Expander ─────────────────────────────────────────────────────────── */
    .streamlit-expanderHeader {
        font-family: 'Outfit', sans-serif;
        font-weight: 600;
        font-size: 1.1rem;
    }

    /* ── Plotly Charts Container ──────────────────────────────────────────── */
    .plot-container {
        background: var(--card-bg);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 15px;
        margin: 10px 0;
    }

    /* ── Strategy Box ─────────────────────────────────────────────────────── */
    .strategy-box {
        background: linear-gradient(135deg, rgba(67, 233, 123, 0.12), rgba(56, 249, 215, 0.12));
        border: 1px solid rgba(67, 233, 123, 0.3);
        border-left: 4px solid #43e97b;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        color: #e0ffe0;
        line-height: 1.7;
    }

    .strategy-box strong {
        color: #43e97b;
    }

    /* ── Warning Box ──────────────────────────────────────────────────────── */
    .warning-box {
        background: linear-gradient(135deg, rgba(243, 156, 18, 0.12), rgba(241, 196, 15, 0.12));
        border: 1px solid rgba(243, 156, 18, 0.3);
        border-left: 4px solid #f39c12;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        color: #fff3cd;
        line-height: 1.7;
    }

    /* ── Login Styles ─────────────────────────────────────────────────────── */
    .login-container {
        max-width: 480px;
        margin: 0 auto;
        padding: 50px 40px;
        background: rgba(255,255,255,0.06);
        backdrop-filter: blur(30px);
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 28px;
        box-shadow: 0 30px 80px rgba(0,0,0,0.4);
    }

    .login-logo {
        text-align: center;
        font-size: 4rem;
        margin-bottom: 10px;
    }

    .login-title {
        text-align: center;
        font-family: 'Outfit', sans-serif;
        font-size: 2rem;
        font-weight: 800;
        background: var(--gradient-1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }

    .login-subtitle {
        text-align: center;
        color: var(--text-secondary);
        font-size: 0.95rem;
        margin-bottom: 30px;
    }

    /* ── Full page gradient background ────────────────────────────────────── */
    .full-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a3e 30%, #2d1b69 60%, #0f3460 100%);
        z-index: -1;
    }

    /* ── Animated orbs ────────────────────────────────────────────────────── */
    .orb {
        position: fixed;
        border-radius: 50%;
        filter: blur(80px);
        opacity: 0.4;
        z-index: -1;
        animation: float 8s ease-in-out infinite;
    }

    .orb-1 {
        width: 400px; height: 400px;
        background: #667eea;
        top: -100px; left: -100px;
        animation-delay: 0s;
    }

    .orb-2 {
        width: 350px; height: 350px;
        background: #764ba2;
        bottom: -100px; right: -100px;
        animation-delay: 2s;
    }

    .orb-3 {
        width: 250px; height: 250px;
        background: #f093fb;
        top: 50%; left: 60%;
        animation-delay: 4s;
    }

    @keyframes float {
        0%, 100% { transform: translate(0, 0) scale(1); }
        33% { transform: translate(30px, -30px) scale(1.05); }
        66% { transform: translate(-20px, 20px) scale(0.95); }
    }

    /* ── Map Container ────────────────────────────────────────────────────── */
    .map-container {
        border-radius: 16px;
        overflow: hidden;
        border: 2px solid rgba(102,126,234,0.3);
    }

    /* ── Download Button ──────────────────────────────────────────────────── */
    .download-btn {
        display: inline-block;
        padding: 10px 24px;
        background: var(--gradient-1);
        color: white;
        border-radius: 10px;
        text-decoration: none;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .download-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(102,126,234,0.3);
    }
</style>
"""

# ─────────────────────────────────────────────────────────────────────────────
# INJECT CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# BACKGROUND VISUALS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="full-bg"></div>
<div class="orb orb-1"></div>
<div class="orb orb-2"></div>
<div class="orb orb-3"></div>
""", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═════════════════════════════════════════════════════════════════════════════

def generate_sample_data(n=500):
    """Generate realistic sample dataset for demo purposes."""
    np.random.seed(42)

    cities = ["Kozhikode", "Kochi", "Thiruvananthapuram", "Thrissur", "Kannur",
              "Palakkad", "Alappuzha", "Kollam", "Kottayam", "Malappuram"]
    city_coords = {
        "Kozhikode": (11.2588, 75.7804), "Kochi": (9.9312, 76.2673),
        "Thiruvananthapuram": (8.5241, 76.9366), "Thrissur": (10.5276, 76.2144),
        "Kannur": (11.8745, 75.3704), "Palakkad": (10.7867, 76.6548),
        "Alappuzha": (9.4981, 76.3388), "Kollam": (8.8932, 76.6141),
        "Kottayam": (9.5916, 76.5222), "Malappuram": (11.0510, 76.0711),
    }
    sources = ["Google Ads", "Facebook", "Instagram", "Referral", "Website",
               "Walk-in", "WhatsApp", "JustDial", "IndiaMART", "YouTube"]
    departments = ["Residential", "Commercial", "Modular Kitchen",
                   "Office Interiors", "Renovation"]
    persons = ["Arun K", "Priya M", "Rahul S", "Sneha B", "Vijay R",
               "Divya N", "Ajith P", "Meera T", "Suresh L", "Anjali D"]
    work_types = ["Modern Kitchen", "Traditional Living Room", "Office Cabin",
                  "Bedroom Design", "Bathroom Renovation", "Full Home Interior",
                  "Modular Wardrobe", "False Ceiling", "Commercial Space", "Pooja Room"]
    business_types = ["Individual", "Small Business", "Corporate", "Builder",
                      "Architect Referral"]
    stages = ["Won", "Lost", "Follow-up", "Negotiation", "Site Visit",
              "Quotation Sent", "Design Phase"]

    dates = pd.date_range(start="2023-01-01", end="2025-12-31", periods=n)
    chosen_cities = np.random.choice(cities, n)

    data = {
        "sl_no": range(1, n + 1),
        "date": dates,
        "source_of_leads": np.random.choice(sources, n, p=[0.2, 0.15, 0.12, 0.15, 0.1, 0.08, 0.07, 0.05, 0.05, 0.03]),
        "department": np.random.choice(departments, n, p=[0.35, 0.2, 0.2, 0.15, 0.1]),
        "alloted_person": np.random.choice(persons, n),
        "contact_no": [f"9{np.random.randint(100000000, 999999999)}" for _ in range(n)],
        "customer_name": [f"Customer_{i}" for i in range(1, n + 1)],
        "customer_business_name": [f"Business_{i}" if np.random.random() > 0.4 else "" for i in range(1, n + 1)],
        "business_type": np.random.choice(business_types, n),
        "latitude": [city_coords[c][0] + np.random.uniform(-0.05, 0.05) for c in chosen_cities],
        "longitude": [city_coords[c][1] + np.random.uniform(-0.05, 0.05) for c in chosen_cities],
        "city": chosen_cities,
        "work_requirement": np.random.choice(work_types, n),
        "year": [d.year for d in dates],
        "month": [d.month for d in dates],
        "phone_valid": np.random.choice([True, False], n, p=[0.92, 0.08]),
        "is_duplicate_lead": np.random.choice([True, False], n, p=[0.07, 0.93]),
        "stage_clean_norm": np.random.choice(stages, n, p=[0.25, 0.2, 0.15, 0.12, 0.1, 0.1, 0.08]),
        "final_lead_stage": np.random.choice(stages, n, p=[0.28, 0.18, 0.14, 0.12, 0.1, 0.1, 0.08]),
    }

    df = pd.DataFrame(data)
    # Revenue: higher for Won leads, zero for some Lost
    revenue = []
    for _, row in df.iterrows():
        if row["final_lead_stage"] == "Won":
            revenue.append(np.random.randint(50000, 2500000))
        elif row["final_lead_stage"] == "Lost":
            revenue.append(0)
        else:
            revenue.append(np.random.choice([0, np.random.randint(10000, 500000)]))
    df["Revenue"] = revenue

    return df


def clean_data(df):
    """Auto-clean the uploaded dataset."""
    df = df.copy()

    # Handle nulls
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].fillna("Unknown")
    for col in df.select_dtypes(include=["number"]).columns:
        df[col] = df[col].fillna(0)

    # Parse date
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df["year"] = df["date"].dt.year
        df["month"] = df["date"].dt.month
        df["month_name"] = df["date"].dt.strftime("%b %Y")

    # Revenue to numeric
    if "Revenue" in df.columns:
        df["Revenue"] = pd.to_numeric(df["Revenue"], errors="coerce").fillna(0)

    # Remove duplicates based on contact_no if available
    if "is_duplicate_lead" in df.columns:
        dup_count = df["is_duplicate_lead"].sum() if df["is_duplicate_lead"].dtype == bool else 0
    else:
        dup_count = 0

    return df, dup_count


def render_metric_card(icon, value, label, grad_class="grad-1"):
    """Render a beautiful metric card."""
    return f"""
    <div class="metric-card {grad_class}">
        <div class="metric-icon">{icon}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """


def plotly_theme(fig, title=""):
    """Apply consistent dark theme to Plotly charts."""
    fig.update_layout(
        title=dict(text=title, font=dict(family="Outfit", size=20, color="#e0e0ff")),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#b8b8d0"),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            bordercolor="rgba(255,255,255,0.1)",
            font=dict(color="#e0e0ff"),
        ),
        xaxis=dict(gridcolor="rgba(255,255,255,0.06)", zerolinecolor="rgba(255,255,255,0.1)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.06)", zerolinecolor="rgba(255,255,255,0.1)"),
        margin=dict(l=40, r=40, t=60, b=40),
        hoverlabel=dict(bgcolor="#1a1a2e", font_size=13, font_family="Inter"),
    )
    return fig


def format_inr(amount):
    """Format number as Indian Rupees."""
    if amount >= 10000000:
        return f"₹{amount / 10000000:.2f} Cr"
    elif amount >= 100000:
        return f"₹{amount / 100000:.2f} L"
    elif amount >= 1000:
        return f"₹{amount / 1000:.1f} K"
    else:
        return f"₹{amount:,.0f}"


# ═════════════════════════════════════════════════════════════════════════════
# AUTHENTICATION CONFIG (YAML-based, compatible with streamlit-authenticator)
# ═════════════════════════════════════════════════════════════════════════════

# --- YAML Config (can also be saved as config.yaml) ---
AUTH_YAML_CONFIG = """
credentials:
  usernames:
    admin:
      email: admin@aestheticsmission.com
      name: Manager
      password: '{hashed_password}'
cookie:
  expiry_days: 1
  key: aesthetics_mission_auth_key_2024
  name: aesthetics_auth_cookie
"""

VALID_USERNAME = "admin"
VALID_PASSWORD = "aesthetics123"
VALID_NAME = "Manager"


# ═════════════════════════════════════════════════════════════════════════════
# LOGIN PAGE
# ═════════════════════════════════════════════════════════════════════════════

def render_login_page():
    """Render the beautiful login page with robust authentication."""

    # Center the login form
    col1, col2, col3 = st.columns([1, 1.5, 1])

    with col2:
        st.markdown("""
        <div style="text-align:center; margin-top: 40px;">
            <div class="login-logo">🏠</div>
            <div class="login-title">AESTHETICS MISSION</div>
            <div class="login-subtitle">Interior Designing Company<br>
            <span style="font-size:0.8rem; color: rgba(255,255,255,0.5);">
                Manager Analytics Portal
            </span></div>
        </div>
        """, unsafe_allow_html=True)

        authenticator = None

        # Try streamlit-authenticator first (handles cookies, proper hashing)
        try:
            hashed_pw = stauth.Hasher([VALID_PASSWORD]).generate()[0]
            config = yaml.safe_load(AUTH_YAML_CONFIG.format(hashed_password=hashed_pw))

            authenticator = stauth.Authenticate(
                config["credentials"],
                config["cookie"]["name"],
                config["cookie"]["key"],
                config["cookie"]["expiry_days"],
            )

            # v0.4.x API: login() sets session state and returns None
            try:
                result = authenticator.login(
                    location="main",
                    fields={
                        "Form name": "🔐 Login to Dashboard",
                        "Username": "Username",
                        "Password": "Password",
                        "Login": "Sign In →",
                    },
                )
                # v0.3.x returns a tuple
                if isinstance(result, tuple):
                    _name, _status, _uname = result
                    st.session_state["name"] = _name
                    st.session_state["authentication_status"] = _status
                    st.session_state["username"] = _uname
            except TypeError:
                # v0.4.x: login() with no return / different signature
                try:
                    authenticator.login(location="main")
                except Exception:
                    authenticator.login()

        except Exception:
            # ── Manual Fallback Login ─────────────────────────────────────
            authenticator = None
            st.markdown("---")
            with st.form("login_form", clear_on_submit=False):
                st.markdown("""
                <div style="text-align:center; font-family: 'Outfit'; font-size: 1.2rem;
                            font-weight: 600; color: #667eea; margin-bottom: 15px;">
                    🔐 Login to Dashboard
                </div>
                """, unsafe_allow_html=True)
                username_input = st.text_input("👤 Username", placeholder="Enter username")
                password_input = st.text_input("🔑 Password", type="password", placeholder="Enter password")
                submitted = st.form_submit_button("🚀 Sign In →", use_container_width=True, type="primary")

            if submitted:
                if username_input == VALID_USERNAME and password_input == VALID_PASSWORD:
                    st.session_state["authentication_status"] = True
                    st.session_state["name"] = VALID_NAME
                    st.session_state["username"] = VALID_USERNAME
                    st.rerun()
                elif username_input or password_input:
                    st.error("❌ Invalid username or password")

        # Read authentication status from session state
        authentication_status = st.session_state.get("authentication_status")
        name = st.session_state.get("name")
        username = st.session_state.get("username")

        if authentication_status is False:
            st.error("❌ Username or password is incorrect")
        elif authentication_status is None:
            st.markdown("""
            <div style="text-align:center; margin-top:15px; color: rgba(255,255,255,0.5); font-size:0.85rem;">
                Demo → Username: <code>admin</code> | Password: <code>aesthetics123</code>
            </div>
            """, unsafe_allow_html=True)

        return authentication_status, name, username, authenticator


# ═════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═════════════════════════════════════════════════════════════════════════════

def render_sidebar(authenticator):
    """Render the sidebar with file upload and options."""
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center; padding: 20px 0;">
            <div style="font-size: 3rem;">🏠</div>
            <div style="font-family: 'Outfit', sans-serif; font-size: 1.3rem; font-weight: 700;
                        background: linear-gradient(135deg, #667eea, #764ba2);
                        -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                AESTHETICS MISSION
            </div>
            <div style="font-size: 0.75rem; color: rgba(255,255,255,0.5); margin-top: 3px;">
                Business Analytics Dashboard
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # Logout button
        if authenticator:
            try:
                authenticator.logout("🚪 Logout", "sidebar")
            except Exception:
                if st.button("🚪 Logout", use_container_width=True):
                    st.session_state["authentication_status"] = None
                    st.session_state["name"] = None
                    st.session_state["username"] = None
                    st.rerun()
        else:
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state["authentication_status"] = None
                st.session_state["name"] = None
                st.session_state["username"] = None
                st.rerun()

        st.markdown("---")

        # File Upload
        st.markdown("### 📁 Data Upload")
        uploaded_file = st.file_uploader(
            "Upload CSV or Excel file",
            type=["csv", "xlsx", "xls"],
            help="Upload your leads dataset with the required columns",
        )

        use_sample = st.checkbox("📊 Use Sample Data", value=True,
                                 help="Use demo data to explore the dashboard")

        st.markdown("---")

        # Theme toggle
        st.markdown("### 🎨 Preferences")
        dark_mode = st.toggle("🌙 Dark Theme", value=True)

        st.markdown("---")

        # Info
        st.markdown("""
        <div style="background: rgba(102,126,234,0.1); border-radius: 12px; padding: 15px;
                    border: 1px solid rgba(102,126,234,0.2); margin-top: 10px;">
            <div style="font-weight: 600; color: #667eea; margin-bottom: 5px;">ℹ️ Required Columns</div>
            <div style="font-size: 0.7rem; color: rgba(255,255,255,0.5); line-height: 1.8;">
                sl_no, date, source_of_leads, department, alloted_person, contact_no,
                customer_name, customer_business_name, business_type, latitude, longitude,
                city, work_requirement, year, month, phone_valid, is_duplicate_lead,
                stage_clean_norm, final_lead_stage, Revenue
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("""
        <div style="text-align:center; font-size:0.7rem; color: rgba(255,255,255,0.3); padding: 10px;">
            © 2025 AESTHETICS MISSION<br>Built with ❤️ for Interior Excellence
        </div>
        """, unsafe_allow_html=True)

    return uploaded_file, use_sample, dark_mode


# ═════════════════════════════════════════════════════════════════════════════
# KPI SECTION
# ═════════════════════════════════════════════════════════════════════════════

def render_kpis(df):
    """Render the KPI metric cards."""
    total_leads = len(df)
    total_revenue = df["Revenue"].sum()
    converted = df[df["final_lead_stage"] != "Lost"]
    conversion_rate = (len(converted) / total_leads * 100) if total_leads > 0 else 0
    avg_revenue_city = df.groupby("city")["Revenue"].mean().mean() if "city" in df.columns else 0

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(render_metric_card("📊", f"{total_leads:,}", "Total Leads", "grad-1"),
                    unsafe_allow_html=True)
    with c2:
        st.markdown(render_metric_card("💰", format_inr(total_revenue), "Total Revenue", "grad-2"),
                    unsafe_allow_html=True)
    with c3:
        st.markdown(render_metric_card("🎯", f"{conversion_rate:.1f}%", "Conversion Rate", "grad-3"),
                    unsafe_allow_html=True)
    with c4:
        st.markdown(render_metric_card("🏙️", format_inr(avg_revenue_city), "Avg Revenue / City", "grad-4"),
                    unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Sub-KPIs row
    sc1, sc2, sc3, sc4, sc5 = st.columns(5)

    top_source = df.groupby("source_of_leads")["Revenue"].sum().idxmax() if len(df) > 0 else "N/A"
    top_city = df.groupby("city")["Revenue"].sum().idxmax() if len(df) > 0 else "N/A"
    top_person = df.groupby("alloted_person")["Revenue"].sum().idxmax() if len(df) > 0 else "N/A"
    won_leads = len(df[df["final_lead_stage"] == "Won"])
    avg_deal = df[df["Revenue"] > 0]["Revenue"].mean() if len(df[df["Revenue"] > 0]) > 0 else 0

    with sc1:
        st.metric("🏆 Top Source", top_source)
    with sc2:
        st.metric("🌟 Top City", top_city)
    with sc3:
        st.metric("👤 Top Performer", top_person)
    with sc4:
        st.metric("✅ Won Leads", f"{won_leads:,}")
    with sc5:
        st.metric("💎 Avg Deal Size", format_inr(avg_deal))


# ═════════════════════════════════════════════════════════════════════════════
# CHARTS SECTION
# ═════════════════════════════════════════════════════════════════════════════

def render_charts(df):
    """Render interactive Plotly charts."""

    st.markdown('<div class="section-header">📈 Interactive Analytics</div>', unsafe_allow_html=True)

    # ── Row 1: Revenue Bar Charts ─────────────────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        rev_source = df.groupby("source_of_leads")["Revenue"].sum().reset_index()
        rev_source = rev_source.sort_values("Revenue", ascending=True)
        fig = px.bar(
            rev_source, x="Revenue", y="source_of_leads", orientation="h",
            color="Revenue",
            color_continuous_scale=["#667eea", "#764ba2", "#f093fb"],
            text=rev_source["Revenue"].apply(lambda x: format_inr(x)),
        )
        fig.update_traces(textposition="outside", textfont_size=11)
        fig = plotly_theme(fig, "💼 Revenue by Lead Source")
        fig.update_layout(height=450, showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        rev_btype = df.groupby("business_type")["Revenue"].sum().reset_index()
        rev_btype = rev_btype.sort_values("Revenue", ascending=True)
        fig = px.bar(
            rev_btype, x="Revenue", y="business_type", orientation="h",
            color="Revenue",
            color_continuous_scale=["#4facfe", "#00f2fe", "#43e97b"],
            text=rev_btype["Revenue"].apply(lambda x: format_inr(x)),
        )
        fig.update_traces(textposition="outside", textfont_size=11)
        fig = plotly_theme(fig, "🏢 Revenue by Business Type")
        fig.update_layout(height=450, showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    # ── Row 2: Pie Charts ─────────────────────────────────────────────────
    col3, col4 = st.columns(2)

    with col3:
        dept_leads = df["department"].value_counts().reset_index()
        dept_leads.columns = ["department", "count"]
        fig = px.pie(
            dept_leads, values="count", names="department",
            color_discrete_sequence=["#667eea", "#764ba2", "#f093fb", "#f5576c", "#4facfe"],
            hole=0.45,
        )
        fig.update_traces(textposition="inside", textinfo="percent+label",
                          textfont_size=12, pull=[0.05] * len(dept_leads))
        fig = plotly_theme(fig, "🏗️ Leads by Department")
        fig.update_layout(height=420)
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        stage_leads = df["final_lead_stage"].value_counts().reset_index()
        stage_leads.columns = ["stage", "count"]
        fig = px.pie(
            stage_leads, values="count", names="stage",
            color_discrete_sequence=["#43e97b", "#fa709a", "#fee140", "#4facfe",
                                     "#f093fb", "#38f9d7", "#a18cd1"],
            hole=0.45,
        )
        fig.update_traces(textposition="inside", textinfo="percent+label", textfont_size=12)
        fig = plotly_theme(fig, "🎯 Leads by Final Stage")
        fig.update_layout(height=420)
        st.plotly_chart(fig, use_container_width=True)

    # ── Row 3: Monthly Revenue Trend ──────────────────────────────────────
    st.markdown('<div class="section-header">📉 Revenue Trends</div>', unsafe_allow_html=True)

    if "date" in df.columns:
        monthly_rev = df.groupby(df["date"].dt.to_period("M")).agg(
            Revenue=("Revenue", "sum"),
            Leads=("sl_no", "count"),
        ).reset_index()
        monthly_rev["date"] = monthly_rev["date"].astype(str)

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Scatter(
                x=monthly_rev["date"], y=monthly_rev["Revenue"],
                mode="lines+markers",
                name="Revenue",
                line=dict(color="#667eea", width=3, shape="spline"),
                marker=dict(size=8, color="#667eea", line=dict(width=2, color="white")),
                fill="tozeroy",
                fillcolor="rgba(102,126,234,0.1)",
            ),
            secondary_y=False,
        )
        fig.add_trace(
            go.Bar(
                x=monthly_rev["date"], y=monthly_rev["Leads"],
                name="Lead Count",
                marker_color="rgba(240,147,251,0.4)",
                marker_line_color="#f093fb",
                marker_line_width=1,
            ),
            secondary_y=True,
        )
        fig = plotly_theme(fig, "📈 Monthly Revenue & Lead Trend")
        fig.update_yaxes(title_text="Revenue (₹)", secondary_y=False, gridcolor="rgba(255,255,255,0.06)")
        fig.update_yaxes(title_text="Lead Count", secondary_y=True, gridcolor="rgba(255,255,255,0.06)")
        fig.update_layout(height=450, barmode="overlay")
        st.plotly_chart(fig, use_container_width=True)

    # ── Row 4: Performance Heatmap ────────────────────────────────────────
    st.markdown('<div class="section-header">🔥 Team Performance Heatmap</div>', unsafe_allow_html=True)

    if "month" in df.columns and "alloted_person" in df.columns:
        heatmap_data = df.pivot_table(
            values="Revenue", index="alloted_person",
            columns="month", aggfunc="sum", fill_value=0
        )
        month_names = {i: calendar.month_abbr[i] for i in range(1, 13)}
        heatmap_data.columns = [month_names.get(c, c) for c in heatmap_data.columns]

        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data.values,
            x=heatmap_data.columns,
            y=heatmap_data.index,
            colorscale=[
                [0, "#0f0f23"],
                [0.25, "#1a1a3e"],
                [0.5, "#667eea"],
                [0.75, "#f093fb"],
                [1, "#f5576c"],
            ],
            colorbar=dict(title="Revenue", tickprefix="₹"),
            hoverongaps=False,
            hovertemplate="Person: %{y}<br>Month: %{x}<br>Revenue: ₹%{z:,.0f}<extra></extra>",
        ))
        fig = plotly_theme(fig, "👥 Alloted Person × Month Revenue")
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)


# ═════════════════════════════════════════════════════════════════════════════
# MAP SECTION
# ═════════════════════════════════════════════════════════════════════════════

def render_map(df):
    """Render Folium map with customer locations."""
    st.markdown('<div class="section-header">🗺️ Customer Location Map</div>', unsafe_allow_html=True)

    # Filters
    fc1, fc2 = st.columns(2)
    with fc1:
        stage_filter = st.multiselect(
            "🎯 Filter by Lead Stage",
            options=df["final_lead_stage"].unique().tolist(),
            default=df["final_lead_stage"].unique().tolist(),
            key="map_stage_filter",
        )
    with fc2:
        btype_filter = st.multiselect(
            "🏢 Filter by Business Type",
            options=df["business_type"].unique().tolist(),
            default=df["business_type"].unique().tolist(),
            key="map_btype_filter",
        )

    filtered = df[
        (df["final_lead_stage"].isin(stage_filter)) &
        (df["business_type"].isin(btype_filter))
    ]

    if len(filtered) == 0:
        st.warning("⚠️ No data matches the selected filters.")
        return

    # Check for valid lat/long
    map_df = filtered.dropna(subset=["latitude", "longitude"])
    map_df = map_df[(map_df["latitude"] != 0) & (map_df["longitude"] != 0)]

    if len(map_df) == 0:
        st.warning("⚠️ No valid location data available.")
        return

    # Create map
    center_lat = map_df["latitude"].mean()
    center_lon = map_df["longitude"].mean()

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=8,
        tiles="CartoDB dark_matter",
    )

    # Marker clusters
    marker_cluster = MarkerCluster(name="Customer Locations").add_to(m)

    stage_colors = {
        "Won": "green", "Lost": "red", "Follow-up": "orange",
        "Negotiation": "blue", "Site Visit": "purple",
        "Quotation Sent": "cadetblue", "Design Phase": "pink",
    }

    for _, row in map_df.iterrows():
        popup_html = f"""
        <div style="font-family: 'Inter', sans-serif; min-width: 200px; padding: 10px;">
            <h4 style="color: #667eea; margin: 0 0 8px 0;">{row.get('customer_name', 'N/A')}</h4>
            <p style="margin: 3px 0;"><b>Business:</b> {row.get('customer_business_name', 'N/A')}</p>
            <p style="margin: 3px 0;"><b>City:</b> {row.get('city', 'N/A')}</p>
            <p style="margin: 3px 0;"><b>Revenue:</b> ₹{row.get('Revenue', 0):,.0f}</p>
            <p style="margin: 3px 0;"><b>Stage:</b> {row.get('final_lead_stage', 'N/A')}</p>
            <p style="margin: 3px 0;"><b>Type:</b> {row.get('business_type', 'N/A')}</p>
        </div>
        """
        color = stage_colors.get(row.get("final_lead_stage", ""), "gray")
        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=folium.Popup(popup_html, max_width=300),
            icon=folium.Icon(color=color, icon="home", prefix="fa"),
        ).add_to(marker_cluster)

    # Heatmap overlay
    heat_data = map_df[["latitude", "longitude", "Revenue"]].values.tolist()
    HeatMap(
        heat_data,
        name="Revenue Heatmap",
        min_opacity=0.3,
        radius=25,
        blur=20,
        gradient={0.2: "#667eea", 0.5: "#f093fb", 0.8: "#f5576c", 1: "#fee140"},
    ).add_to(m)

    folium.LayerControl().add_to(m)

    # Display map
    st.markdown('<div class="map-container">', unsafe_allow_html=True)
    st_folium(m, width=None, height=550, returned_objects=[])
    st.markdown('</div>', unsafe_allow_html=True)

    # Map stats
    mc1, mc2, mc3 = st.columns(3)
    with mc1:
        st.metric("📍 Locations Shown", f"{len(map_df):,}")
    with mc2:
        city_count = map_df["city"].nunique()
        st.metric("🏙️ Cities Covered", f"{city_count}")
    with mc3:
        total_map_rev = map_df["Revenue"].sum()
        st.metric("💰 Filtered Revenue", format_inr(total_map_rev))


# ═════════════════════════════════════════════════════════════════════════════
# FORECASTING SECTION
# ═════════════════════════════════════════════════════════════════════════════

def render_forecasting(df):
    """Revenue forecasting using Prophet."""
    st.markdown('<div class="section-header">🔮 Revenue Forecasting & Insights</div>', unsafe_allow_html=True)

    try:
        from prophet import Prophet

        if "date" not in df.columns:
            st.error("❌ Date column required for forecasting.")
            return

        # Prepare time series
        ts = df.groupby(df["date"].dt.to_period("M"))["Revenue"].sum().reset_index()
        ts["date"] = ts["date"].dt.to_timestamp()
        ts.columns = ["ds", "y"]
        ts = ts.sort_values("ds")

        if len(ts) < 6:
            st.warning("⚠️ Need at least 6 months of data for accurate forecasting.")
            return

        with st.spinner("🔮 Training forecasting model... Please wait..."):
            # Train Prophet
            model = Prophet(
                yearly_seasonality=True,
                weekly_seasonality=False,
                daily_seasonality=False,
                changepoint_prior_scale=0.05,
                seasonality_mode="multiplicative",
            )
            model.fit(ts)

            # Forecast next 5 months
            future = model.make_future_dataframe(periods=5, freq="MS")
            forecast = model.predict(future)

        # ── Forecast Plot ──────────────────────────────────────────────────
        fig = go.Figure()

        # Historical data
        fig.add_trace(go.Scatter(
            x=ts["ds"], y=ts["y"],
            mode="lines+markers",
            name="Historical Revenue",
            line=dict(color="#667eea", width=3),
            marker=dict(size=7, color="#667eea", line=dict(width=2, color="white")),
        ))

        # Forecast
        forecast_future = forecast[forecast["ds"] > ts["ds"].max()]
        fig.add_trace(go.Scatter(
            x=forecast_future["ds"], y=forecast_future["yhat"],
            mode="lines+markers",
            name="Forecasted Revenue",
            line=dict(color="#f093fb", width=3, dash="dash"),
            marker=dict(size=9, color="#f093fb", symbol="diamond",
                        line=dict(width=2, color="white")),
        ))

        # Confidence interval
        fig.add_trace(go.Scatter(
            x=pd.concat([forecast_future["ds"], forecast_future["ds"][::-1]]),
            y=pd.concat([forecast_future["yhat_upper"], forecast_future["yhat_lower"][::-1]]),
            fill="toself",
            fillcolor="rgba(240,147,251,0.15)",
            line=dict(color="rgba(0,0,0,0)"),
            name="Confidence Interval",
            hoverinfo="skip",
        ))

        fig = plotly_theme(fig, "📊 Revenue Forecast – Next 5 Months")
        fig.update_layout(height=500)
        fig.update_yaxes(title_text="Revenue (₹)")
        fig.update_xaxes(title_text="Month")
        st.plotly_chart(fig, use_container_width=True)

        # ── Business Insights ──────────────────────────────────────────────
        st.markdown('<div class="section-header">💡 Business Insights (Manager Summary)</div>',
                    unsafe_allow_html=True)

        # Calculate growth
        last_historical = ts["y"].iloc[-1]
        last_forecast = forecast_future["yhat"].iloc[-1] if len(forecast_future) > 0 else last_historical
        growth_pct = ((last_forecast - last_historical) / last_historical * 100) if last_historical > 0 else 0

        # Top source
        top_source = df.groupby("source_of_leads")["Revenue"].sum().idxmax()
        top_source_rev = df.groupby("source_of_leads")["Revenue"].sum().max()

        # Top cities
        top_cities = df.groupby("city")["Revenue"].sum().nlargest(3)
        top_cities_str = ", ".join(top_cities.index.tolist())

        # Low performer
        person_rev = df.groupby("alloted_person")["Revenue"].sum()
        low_performer = person_rev.idxmin()
        top_performer = person_rev.idxmax()
        improvement_potential = (person_rev.max() - person_rev.min()) / person_rev.max() * 100

        col_i1, col_i2 = st.columns(2)

        with col_i1:
            growth_emoji = "📈" if growth_pct > 0 else "📉"
            st.markdown(f"""
            <div class="insight-box">
                <div style="font-size:1.3rem; font-weight:700; margin-bottom:10px;">
                    {growth_emoji} Revenue Forecast
                </div>
                <strong>Expected growth: {growth_pct:+.1f}%</strong> over the next 5 months.<br><br>
                Focus on <strong>{top_source}</strong> which generates the highest revenue
                (₹{top_source_rev:,.0f}). Increasing investment in this channel could
                yield an additional <strong>{format_inr(top_source_rev * 0.15)}</strong> in revenue.
            </div>
            """, unsafe_allow_html=True)

        with col_i2:
            st.markdown(f"""
            <div class="strategy-box">
                <div style="font-size:1.3rem; font-weight:700; margin-bottom:10px;">
                    🎯 Strategic Recommendations
                </div>
                <strong>Target high-potential cities:</strong> {top_cities_str}.<br><br>
                <strong>Training opportunity:</strong> Upskill <strong>{low_performer}</strong>
                to match <strong>{top_performer}</strong>'s performance. This could boost
                team efficiency by <strong>{improvement_potential:.0f}%</strong>.<br><br>
                <strong>Action:</strong> Allocate 60% of marketing budget to top 3 cities.
            </div>
            """, unsafe_allow_html=True)

        # Additional Insights
        st.markdown("""
        <div class="warning-box">
            <div style="font-size:1.3rem; font-weight:700; margin-bottom:10px;">
                ⚡ Quick Actions for This Month
            </div>
            <strong>1.</strong> Review all "Follow-up" and "Negotiation" leads – potential quick wins.<br>
            <strong>2.</strong> Schedule site visits for "Quotation Sent" leads within 48 hours.<br>
            <strong>3.</strong> Run a retargeting campaign on leads from the top-performing source.<br>
            <strong>4.</strong> Monthly review meeting with all alloted persons to share best practices.
        </div>
        """, unsafe_allow_html=True)

        # Forecast table
        with st.expander("📊 Detailed Forecast Table"):
            forecast_display = forecast_future[["ds", "yhat", "yhat_lower", "yhat_upper"]].copy()
            forecast_display.columns = ["Month", "Predicted Revenue", "Lower Bound", "Upper Bound"]
            forecast_display["Month"] = forecast_display["Month"].dt.strftime("%B %Y")
            for col in ["Predicted Revenue", "Lower Bound", "Upper Bound"]:
                forecast_display[col] = forecast_display[col].apply(lambda x: f"₹{x:,.0f}")
            st.dataframe(forecast_display, use_container_width=True, hide_index=True)

    except ImportError:
        st.error("❌ Prophet is not installed. Install it with: `pip install prophet`")
    except Exception as e:
        st.error(f"❌ Forecasting error: {str(e)}")
        st.info("💡 Ensure your dataset has enough date and revenue data for forecasting.")


# ═════════════════════════════════════════════════════════════════════════════
# INTERIOR DESIGN AI SECTION
# ═════════════════════════════════════════════════════════════════════════════

def generate_image_pollinations(prompt, width=768, height=768, seed=None):
    """Generate an image using Pollinations.ai free API (no key needed)."""
    import requests
    import urllib.parse
    import random

    if seed is None:
        seed = random.randint(1, 999999)

    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&seed={seed}&nologo=true"

    try:
        response = requests.get(url, timeout=120)
        if response.status_code == 200 and len(response.content) > 1000:
            return response.content, seed
        else:
            return None, seed
    except Exception:
        return None, seed


def render_interior_design():
    """AI-powered interior design image generation."""
    st.markdown('<div class="section-header">🎨 AI Interior Design Generator</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box">
        <strong>🤖 Powered by AI:</strong> Enter a design requirement and generate stunning interior
        design concepts using advanced AI models. Perfect for client presentations and mood boards.<br><br>
        <span style="color: #43e97b;">✅ Free • No API Key Required • Instant Results</span>
    </div>
    """, unsafe_allow_html=True)

    # Input
    design_prompt = st.text_input(
        "✏️ Enter customer requirement",
        placeholder="e.g., Modern minimalist kitchen with white marble countertops",
        help="Describe the interior design style and room type",
    )

    col_opt1, col_opt2, col_opt3 = st.columns(3)
    with col_opt1:
        num_images = st.selectbox("🖼️ Number of designs", [1, 2, 3, 4], index=1)
    with col_opt2:
        style_preset = st.selectbox("🎨 Style", [
            "Modern", "Traditional Kerala", "Minimalist", "Luxury",
            "Scandinavian", "Industrial", "Mediterranean", "Contemporary",
        ])
    with col_opt3:
        room_type = st.selectbox("🏠 Room Type", [
            "Living Room", "Kitchen", "Bedroom", "Bathroom",
            "Office", "Pooja Room", "Dining Room", "Balcony",
        ])

    full_prompt = (
        f"{style_preset} {room_type} interior design, {design_prompt}, "
        f"professional interior photography, 8k, ultra realistic, highly detailed, "
        f"beautiful natural lighting, architectural digest style, award winning design, "
        f"luxury interiors, photorealistic render"
    )

    if st.button("🚀 Generate Designs", use_container_width=True, type="primary"):
        if not design_prompt:
            st.warning("⚠️ Please enter a design requirement first.")
            return

        st.markdown(f"""
        <div class="section-header">
            ✨ Generating Designs for: "{design_prompt}"
        </div>
        """, unsafe_allow_html=True)

        import random

        cols = st.columns(min(num_images, 2))
        progress_bar = st.progress(0, text="🎨 Generating AI designs...")
        generated_count = 0

        for i in range(num_images):
            seed = random.randint(1, 999999)
            progress_bar.progress(
                (i) / num_images,
                text=f"🎨 Generating design {i + 1} of {num_images}..."
            )

            image_bytes, used_seed = generate_image_pollinations(
                full_prompt, width=768, height=768, seed=seed
            )

            if image_bytes:
                generated_count += 1
                with cols[i % len(cols)]:
                    st.image(
                        image_bytes,
                        caption=f"Design {i + 1}: {style_preset} {room_type} (seed: {used_seed})",
                        use_container_width=True,
                    )
                    st.download_button(
                        label=f"📥 Download Design {i + 1}",
                        data=image_bytes,
                        file_name=f"aesthetics_design_{i + 1}_{room_type.lower().replace(' ', '_')}.png",
                        mime="image/png",
                        use_container_width=True,
                        key=f"dl_design_{i}_{seed}",
                    )
            else:
                with cols[i % len(cols)]:
                    st.error(f"❌ Design {i + 1} generation failed. Try again.")

        progress_bar.progress(1.0, text=f"✅ Generated {generated_count}/{num_images} designs!")

        if generated_count > 0:
            st.markdown("""
            <div class="strategy-box">
                <strong>💡 Tips:</strong><br>
                • Click <strong>Generate</strong> again with the same prompt for different variations<br>
                • Be more specific in your description for better results<br>
                • Try different style presets and room types for diverse concepts<br>
                • Download and use these in client presentations and mood boards
            </div>
            """, unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# DATA EXPLORER
# ═════════════════════════════════════════════════════════════════════════════

def render_data_explorer(df):
    """Data exploration and summary section."""
    st.markdown('<div class="section-header">🔍 Data Explorer</div>', unsafe_allow_html=True)

    tab_a, tab_b, tab_c = st.tabs(["📋 Data Table", "📊 Summary Stats", "🔄 Data Quality"])

    with tab_a:
        # Search
        search = st.text_input("🔍 Search data...", placeholder="Type customer name, city, etc.")
        display_df = df.copy()
        if search:
            mask = display_df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)
            display_df = display_df[mask]

        st.dataframe(display_df, use_container_width=True, height=400)
        st.caption(f"Showing {len(display_df):,} of {len(df):,} records")

    with tab_b:
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.markdown("#### 📊 Numerical Summary")
            st.dataframe(df.describe().round(2), use_container_width=True)
        with col_s2:
            st.markdown("#### 📝 Column Types")
            dtype_df = pd.DataFrame({
                "Column": df.columns,
                "Type": df.dtypes.values,
                "Non-Null": df.notnull().sum().values,
                "Unique": [df[col].nunique() for col in df.columns],
            })
            st.dataframe(dtype_df, use_container_width=True, hide_index=True)

    with tab_c:
        # Data quality metrics
        total_cells = df.size
        null_cells = df.isnull().sum().sum()
        quality_pct = ((total_cells - null_cells) / total_cells * 100) if total_cells > 0 else 0

        qc1, qc2, qc3, qc4 = st.columns(4)
        with qc1:
            st.metric("📋 Total Records", f"{len(df):,}")
        with qc2:
            st.metric("✅ Data Quality", f"{quality_pct:.1f}%")
        with qc3:
            dup_count = df["is_duplicate_lead"].sum() if "is_duplicate_lead" in df.columns else 0
            st.metric("🔄 Duplicates", f"{dup_count:,}")
        with qc4:
            phone_valid = df["phone_valid"].sum() if "phone_valid" in df.columns else len(df)
            st.metric("📱 Valid Phones", f"{phone_valid:,}")

        # Null heatmap
        null_pct = (df.isnull().sum() / len(df) * 100).reset_index()
        null_pct.columns = ["Column", "Null %"]
        null_pct = null_pct.sort_values("Null %", ascending=False)

        fig = px.bar(
            null_pct, x="Column", y="Null %",
            color="Null %",
            color_continuous_scale=["#43e97b", "#fee140", "#f5576c"],
        )
        fig = plotly_theme(fig, "🔍 Missing Data by Column")
        fig.update_layout(height=350, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)


# ═════════════════════════════════════════════════════════════════════════════
# MAIN APPLICATION
# ═════════════════════════════════════════════════════════════════════════════

def main():
    """Main application entry point."""

    # ── Initialize Session State ──────────────────────────────────────────
    if "authentication_status" not in st.session_state:
        st.session_state["authentication_status"] = None
    if "data" not in st.session_state:
        st.session_state["data"] = None

    auth_status = st.session_state.get("authentication_status")

    # ── Login Flow ────────────────────────────────────────────────────────
    if auth_status is not True:
        auth_status, name, username, authenticator = render_login_page()
        if auth_status is True:
            st.rerun()
        return

    # ── Authenticated: Dashboard ──────────────────────────────────────────
    name = st.session_state.get("name", "Manager")

    # Sidebar
    uploaded_file, use_sample, dark_mode = render_sidebar(None)

    # ── Load Data ─────────────────────────────────────────────────────────
    df = None

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            df, dup_count = clean_data(df)
            st.session_state["data"] = df
            st.toast(f"✅ Loaded {len(df):,} records | {dup_count} duplicates found", icon="📊")
        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}")

    if use_sample and df is None:
        df = generate_sample_data(500)
        df, dup_count = clean_data(df)
        st.session_state["data"] = df

    if df is None:
        df = st.session_state.get("data")

    # ── Dashboard Header ──────────────────────────────────────────────────
    st.markdown(f"""
    <div class="dashboard-header">
        <h1>🏠 Welcome, {name}</h1>
        <p>AESTHETICS MISSION Interior Designing — Business Analytics Dashboard</p>
    </div>
    """, unsafe_allow_html=True)

    if df is None:
        st.info("📁 Please upload a dataset or enable 'Use Sample Data' in the sidebar.")
        return

    # ── Main Tabs ─────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Dashboard",
        "🗺️ Map View",
        "🔮 Forecasting",
        "🎨 AI Designer",
        "🔍 Data Explorer",
    ])

    with tab1:
        render_kpis(df)
        st.markdown("<br>", unsafe_allow_html=True)
        render_charts(df)

    with tab2:
        render_map(df)

    with tab3:
        render_forecasting(df)

    with tab4:
        render_interior_design()

    with tab5:
        render_data_explorer(df)

    # ── Footer ────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 20px; color: rgba(255,255,255,0.3); font-size: 0.85rem;">
        <strong>🏠 AESTHETICS MISSION</strong> Interior Designing Company<br>
        Business Analytics Dashboard v2.0 | Crafted with ❤️<br>
        <span style="font-size: 0.7rem;">
            Powered by Streamlit • Plotly • Prophet • Folium • AI
        </span>
    </div>
    """, unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# RUN
# ═════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    main()
