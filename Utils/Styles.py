# ═══════════════════════════════════════════════════════════════════
#  PropIQ — Design System
#  Utils/Styles.py
#  Fonts   : Outfit (headings) + DM Sans (body)
#  Palette : Indigo primary · Cyan secondary · Emerald success
#            Amber warning  · Rose danger
#  Background: deep navy #0f172a — readable in daylight on any screen
# ═══════════════════════════════════════════════════════════════════

# ── Plotly theme ─────────────────────────────────────────────────────────────
PLOTLY_THEME = dict(
    paper_bgcolor="rgba(15,23,42,1)",
    plot_bgcolor="rgba(19,32,64,1)",
    font=dict(color="#94a3b8", family="DM Sans, sans-serif", size=12),
    xaxis=dict(
        gridcolor="rgba(148,163,184,0.08)",
        color="#94a3b8",
        linecolor="rgba(148,163,184,0.1)",
        zerolinecolor="rgba(148,163,184,0.1)",
    ),
    yaxis=dict(
        gridcolor="rgba(148,163,184,0.08)",
        color="#94a3b8",
        linecolor="rgba(148,163,184,0.1)",
        zerolinecolor="rgba(148,163,184,0.1)",
    ),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#94a3b8")),
    margin=dict(l=0, r=0, t=36, b=0),
    title_font=dict(color="#e2e8f0", size=13, family="DM Sans, sans-serif"),
    coloraxis_colorbar=dict(
        tickfont=dict(color="#94a3b8"),
        title=dict(font=dict(color="#94a3b8")),  # ← correct for new Plotly
    ),
)

# ── CSS (no JS — safe for st.markdown) ───────────────────────────────────────
BASE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Reset ──────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
}

/* ── App background ─────────────────────────── */
.stApp {
    background-color: #0f172a !important;
    color: #e2e8f0 !important;
}

/* Content must sit above canvas (z-index 0) */
.stApp > div,
.main > div,
.block-container,
section.main > div {
    position: relative !important;
    z-index: 2 !important;
}

/* ── Sidebar ────────────────────────────────── */
# [data-testid="stSidebar"] {
#     background: rgba(8,14,28,0.96) !important;
#     border-right: 1px solid rgba(99,102,241,0.22) !important;
#     box-shadow: 4px 0 30px rgba(0,0,0,0.45) !important;
#     backdrop-filter: blur(14px) !important;
#     position: relative !important;
#     z-index: 100 !important;
# }
[data-testid="stSidebar"] {
    background: rgba(8,14,28,0.96) !important;
    border-right: 1px solid rgba(99,102,241,0.22) !important;
    box-shadow: 4px 0 30px rgba(0,0,0,0.45) !important;
    backdrop-filter: blur(14px) !important;
    position: relative !important;
    z-index: 100 !important;

    /* ✅ FIX SCROLL */
    height: 100vh !important;
    overflow-y: auto !important;
    scroll-behavior: smooth;
}



[data-testid="stSidebar"]::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg,
        #6366f1 0%, #06b6d4 35%, #a78bfa 65%, #6366f1 100%);
    background-size: 200% 100%;
    animation: sidebarShimmer 3.5s linear infinite;
}
@keyframes sidebarShimmer {
    0%   { background-position: 200% 0; }
    100% { background-position: -200% 0; }
}
[data-testid="stSidebarNav"] a {
    border-radius: 10px !important;
    margin: 2px 10px !important;
    padding: 10px 14px !important;
    transition: all 0.2s ease !important;
}
[data-testid="stSidebarNav"] a span {
    color: #475569 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
}
[data-testid="stSidebarNav"] a:hover { background: rgba(99,102,241,0.12) !important; }
[data-testid="stSidebarNav"] a:hover span { color: #a5b4fc !important; }
[data-testid="stSidebarNav"] a[aria-current="page"] {
    background: rgba(99,102,241,0.18) !important;
    border: 1px solid rgba(99,102,241,0.3) !important;
}
[data-testid="stSidebarNav"] a[aria-current="page"] span {
    color: #818cf8 !important;
    font-weight: 700 !important;
}

/* ── Top header ─────────────────────────────── */
header[data-testid="stHeader"] {
    background: rgba(8,14,28,0.88) !important;
    backdrop-filter: blur(16px) !important;
    border-bottom: 1px solid rgba(99,102,241,0.14) !important;
    position: relative !important;
    z-index: 100 !important;
}

/* ── Typography ─────────────────────────────── */
h1, h2, h3, h4, h5 {
    font-family: 'Outfit', sans-serif !important;
    color: #f1f5f9 !important;
    letter-spacing: -0.02em !important;
}
h1 { font-size: 2.5rem !important; font-weight: 800 !important; line-height: 1.12 !important; }
h2 { font-size: 1.55rem !important; font-weight: 700 !important; line-height: 1.25 !important; }
h3 { font-size: 1.1rem  !important; font-weight: 600 !important; }
p  { color: #94a3b8 !important; line-height: 1.75 !important; }
label { color: #64748b !important; }
strong { color: #e2e8f0 !important; }

/* ── Layout ─────────────────────────────────── */
.block-container {
    padding-top: 2.5rem !important;
    padding-bottom: 3rem !important;
    max-width: 1280px !important;
}

/* ── st.container(border=True) ──────────────── */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(19,32,64,0.82) !important;
    border: 1px solid rgba(99,102,241,0.22) !important;
    border-radius: 18px !important;
    padding: 8px 10px !important;
    box-shadow: 0 4px 28px rgba(0,0,0,0.3) !important;
    backdrop-filter: blur(10px) !important;
    transition: border-color 0.25s !important;
}
[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: rgba(99,102,241,0.38) !important;
}

/* ── Input labels ───────────────────────────── */
.stSelectbox > label,
.stNumberInput > label,
.stSlider > label,
.stMultiSelect > label,
.stTextInput > label {
    color: #64748b !important;
    font-size: 0.71rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.09em !important;
    margin-bottom: 4px !important;
}

/* ── Selectbox ──────────────────────────────── */
.stSelectbox [data-baseweb="select"] > div {
    background: rgba(15,23,42,0.9) !important;
    border: 1px solid rgba(148,163,184,0.15) !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    min-height: 46px !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stSelectbox [data-baseweb="select"] > div:hover {
    border-color: rgba(99,102,241,0.5) !important;
}
.stSelectbox [data-baseweb="select"] > div:focus-within {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
}

/* ── Number input ───────────────────────────── */
.stNumberInput [data-testid="stNumberInputContainer"],
.stNumberInput input,
.stTextInput input {
    background: rgba(15,23,42,0.9) !important;
    border: 1px solid rgba(148,163,184,0.15) !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    min-height: 46px !important;
}
.stNumberInput input:focus, .stTextInput input:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
}
.stNumberInput button {
    background: rgba(99,102,241,0.18) !important;
    color: #a5b4fc !important;
    border: none !important;
    border-radius: 8px !important;
}
.stNumberInput button:hover { background: rgba(99,102,241,0.32) !important; }

/* ── Dropdown popover ───────────────────────── */
[data-baseweb="popover"], [data-baseweb="menu"] {
    background: #1e293b !important;
    border: 1px solid rgba(99,102,241,0.25) !important;
    border-radius: 12px !important;
    box-shadow: 0 8px 40px rgba(0,0,0,0.55) !important;
}
[data-baseweb="menu"] li {
    color: #cbd5e1 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.88rem !important;
    border-radius: 8px !important;
    margin: 2px 4px !important;
}
[data-baseweb="menu"] li:hover,
[data-baseweb="menu"] li[aria-selected="true"] {
    background: rgba(99,102,241,0.18) !important;
    color: #a5b4fc !important;
}

/* ── Slider ─────────────────────────────────── */
[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] {
    background: #6366f1 !important;
    border: 2px solid #a5b4fc !important;
    box-shadow: 0 0 0 4px rgba(99,102,241,0.25) !important;
}

/* ── Multiselect ────────────────────────────── */
.stMultiSelect [data-baseweb="select"] > div {
    background: rgba(15,23,42,0.9) !important;
    border: 1px solid rgba(148,163,184,0.15) !important;
    border-radius: 12px !important;
}
.stMultiSelect [data-baseweb="tag"] {
    background: rgba(99,102,241,0.22) !important;
    color: #a5b4fc !important;
    border: 1px solid rgba(99,102,241,0.35) !important;
    border-radius: 8px !important;
    font-size: 0.78rem !important;
}
.stMultiSelect [data-baseweb="tag"] span { color: #a5b4fc !important; }

/* ── Buttons ────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.02em !important;
    padding: 0.6rem 1.4rem !important;
    width: 100% !important;
    min-height: 46px !important;
    transition: all 0.22s cubic-bezier(0.4,0,0.2,1) !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #818cf8 0%, #6366f1 100%) !important;
    box-shadow: 0 6px 30px rgba(99,102,241,0.5), 0 2px 8px rgba(0,0,0,0.3) !important;
    transform: translateY(-2px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Tabs ───────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(15,23,42,0.88) !important;
    border-radius: 14px !important;
    padding: 5px !important;
    gap: 3px !important;
    border: 1px solid rgba(148,163,184,0.1) !important;
    backdrop-filter: blur(8px) !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px !important;
    color: #64748b !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    padding: 8px 20px !important;
    transition: all 0.2s !important;
}
.stTabs [data-baseweb="tab"]:hover { color: #94a3b8 !important; }
.stTabs [aria-selected="true"] {
    background: rgba(99,102,241,0.2) !important;
    color: #a5b4fc !important;
    font-weight: 600 !important;
}
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }
.stTabs [data-baseweb="tab-panel"] { padding-top: 24px !important; }

/* ── Native metrics ─────────────────────────── */
[data-testid="stMetric"] {
    background: rgba(19,32,64,0.8) !important;
    border: 1px solid rgba(99,102,241,0.18) !important;
    border-radius: 16px !important;
    padding: 20px 22px !important;
    backdrop-filter: blur(8px) !important;
    transition: border-color 0.2s, transform 0.2s !important;
}
[data-testid="stMetric"]:hover {
    border-color: rgba(99,102,241,0.38) !important;
    transform: translateY(-2px) !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Outfit', sans-serif !important;
    color: #f1f5f9 !important;
    font-size: 1.65rem !important;
    font-weight: 700 !important;
}
[data-testid="stMetricLabel"] {
    color: #64748b !important;
    font-size: 0.72rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    font-weight: 600 !important;
}

/* ── Alerts ─────────────────────────────────── */
[data-testid="stSuccess"] {
    background: rgba(16,185,129,0.1) !important;
    border: 1px solid rgba(16,185,129,0.28) !important;
    border-radius: 12px !important;
    color: #6ee7b7 !important;
}
[data-testid="stInfo"] {
    background: rgba(99,102,241,0.1) !important;
    border: 1px solid rgba(99,102,241,0.28) !important;
    border-radius: 12px !important;
    color: #a5b4fc !important;
}
[data-testid="stWarning"] {
    background: rgba(245,158,11,0.1) !important;
    border: 1px solid rgba(245,158,11,0.28) !important;
    border-radius: 12px !important;
    color: #fde68a !important;
}
[data-testid="stError"] {
    background: rgba(239,68,68,0.1) !important;
    border: 1px solid rgba(239,68,68,0.28) !important;
    border-radius: 12px !important;
    color: #fca5a5 !important;
}

/* ── Expander ───────────────────────────────── */
.stExpander {
    background: rgba(19,32,64,0.8) !important;
    border: 1px solid rgba(99,102,241,0.18) !important;
    border-radius: 14px !important;
}

/* ── Scrollbar ──────────────────────────────── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: rgba(99,102,241,0.28);
    border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover { background: rgba(99,102,241,0.5); }

/* ── Misc ───────────────────────────────────── */
hr { border-color: rgba(148,163,184,0.1) !important; }
.stCaption { color: #475569 !important; font-size: 0.78rem !important; }
code {
    background: rgba(99,102,241,0.14) !important;
    color: #a5b4fc !important;
    padding: 2px 8px !important;
    border-radius: 6px !important;
    font-size: 0.82rem !important;
    border: 1px solid rgba(99,102,241,0.22) !important;
}

/* ─────────────────────────────────────────────
   REUSABLE HTML DISPLAY COMPONENTS
   (only use in st.markdown — no widgets inside)
───────────────────────────────────────────── */

/* Page label / badge */
.pg-label {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 5px 13px;
    border-radius: 30px;
    margin-bottom: 12px;
}
.pg-label-indigo {
    background: rgba(99,102,241,0.14);
    color: #a5b4fc;
    border: 1px solid rgba(99,102,241,0.32);
}
.pg-label-cyan {
    background: rgba(6,182,212,0.12);
    color: #67e8f9;
    border: 1px solid rgba(6,182,212,0.28);
}
.pg-label-green {
    background: rgba(16,185,129,0.12);
    color: #6ee7b7;
    border: 1px solid rgba(16,185,129,0.28);
}
.pg-label-amber {
    background: rgba(245,158,11,0.12);
    color: #fde68a;
    border: 1px solid rgba(245,158,11,0.28);
}

/* Section label with line */
.section-label {
    font-size: 0.78rem;
    font-weight: 800;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #94A3B8;
    margin-bottom: 14px;
    margin-top: 4px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(148,163,184,0.1);
    border-radius: 1px;
}

/* Divider */
.divider {
    height: 1px;
    background: linear-gradient(90deg,
        transparent 0%,
        rgba(99,102,241,0.35) 25%,
        rgba(6,182,212,0.25) 75%,
        transparent 100%);
    margin: 30px 0;
    border-radius: 1px;
}

/* KPI block */
.kpi-block {
    background: rgba(19,32,64,0.82);
    border: 1px solid rgba(99,102,241,0.16);
    border-radius: 16px;
    padding: 20px 16px;
    text-align: center;
    backdrop-filter: blur(8px);
    transition: border-color 0.2s, transform 0.2s;
}
.kpi-block:hover {
    border-color: rgba(99,102,241,0.35);
    transform: translateY(-2px);
}
.kpi-val {
    font-family: 'Outfit', sans-serif;
    font-size: 1.7rem;
    font-weight: 700;
    line-height: 1.1;
}
.kpi-lbl {
    font-size: 0.68rem;
    color: #475569;
    margin-top: 5px;
    text-transform: uppercase;
    letter-spacing: 0.09em;
    font-weight: 600;
}

/* Big result price */
.result-price { text-align: center; padding: 32px 0 20px; }
.result-price .eyebrow {
    font-size: 0.7rem;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-weight: 600;
    margin-bottom: 10px;
}
.result-price .amount {
    font-family: 'Outfit', sans-serif;
    font-size: 3.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #818cf8 0%, #06b6d4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1;
    letter-spacing: -0.03em;
}
.result-price .range {
    font-size: 0.88rem;
    color: #475569;
    margin-top: 10px;
}

/* Insight row card */
.insight-row {
    background: rgba(15,23,42,0.85);
    border: 1px solid rgba(148,163,184,0.1);
    border-radius: 14px;
    padding: 14px 16px;
    margin-bottom: 8px;
    backdrop-filter: blur(6px);
    transition: border-color 0.2s;
}
.insight-row:hover { border-color: rgba(99,102,241,0.28); }

/* Similarity bar track */
.rec-bar-track {
    height: 4px;
    background: rgba(148,163,184,0.1);
    border-radius: 4px;
    margin-top: 8px;
    overflow: hidden;
}

/* Feature nav card (Home page) */
.feature-nav-card {
    background: rgba(19,32,64,0.82);
    border: 1px solid rgba(99,102,241,0.16);
    border-radius: 18px;
    padding: 24px 20px;
    min-height: 200px;
    display: flex;
    flex-direction: column;
    backdrop-filter: blur(8px);
    transition: all 0.22s cubic-bezier(0.4,0,0.2,1);
    margin-bottom:16px;
}
.feature-nav-card:hover {
    border-color: rgba(99,102,241,0.42);
    transform: translateY(-4px);
    box-shadow: 0 14px 44px rgba(0,0,0,0.35);
}

/* Gradient text helper */
.gradient-text {
    background: linear-gradient(135deg, #818cf8 0%, #06b6d4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Info / methodology box */
.info-box {
    background: rgba(99,102,241,0.07);
    border: 1px solid rgba(99,102,241,0.2);
    border-left: 3px solid #6366f1;
    border-radius: 0 12px 12px 0;
    padding: 16px 20px;
    margin-bottom:20px;
    font-size: 0.94rem
}
.info-box p {
    color: #94a3b8 !important;
    font-size: 0.94rem !important;
    margin: 0 !important;
    line-height: 1.75 !important;
}

/* ═══════════════════════════════════════════════════════
   RESPONSIVE & ZOOM-SAFE ADDITIONS
   – fixes card overflow / misalignment at any zoom level
   – breakpoints: 1280 · 1024 · 768 · 480 px
   ═══════════════════════════════════════════════════════ */

/* Prevent horizontal bleed at any zoom */
html, body {
    overflow-x: hidden !important;
    max-width: 100vw !important;
}
.stApp {
    overflow-x: hidden !important;
    max-width: 100vw !important;
}

/* Block container: fluid padding so it never clips */
.block-container {
    padding-left:  clamp(0.75rem, 3vw, 3rem) !important;
    padding-right: clamp(0.75rem, 3vw, 3rem) !important;
    max-width: min(1280px, 100%) !important;
    width: 100% !important;
    box-sizing: border-box !important;
}

/* Columns: allow wrap instead of overflow */
[data-testid="stHorizontalBlock"] {
    flex-wrap: wrap !important;
    gap: 12px !important;
    width: 100% !important;
    overflow: visible !important;
}
[data-testid="column"] {
    min-width: 0 !important;          /* critical – stops flex blow-out */
    flex-shrink: 1 !important;
    overflow: visible !important;
}

/* ── Feature nav cards ── */
.feature-nav-card {
    min-height: auto !important;      /* was 200px – blows out on zoom */
    height: auto !important;
    word-break: break-word !important;
    overflow: hidden !important;
    box-sizing: border-box !important;
    width: 100% !important;
}

/* ── KPI block ── */
.kpi-block {
    box-sizing: border-box !important;
    word-break: break-word !important;
    overflow: hidden !important;
    width: 100% !important;
}
.kpi-val {
    font-size: clamp(1.1rem, 2.8vw, 1.7rem) !important;
    word-break: break-all !important;
}

/* ── Result price ── */
.result-price .amount {
    font-size: clamp(1.8rem, 5vw, 3.2rem) !important;
}

/* ── Typography – fluid so zoom never clips text ── */
h1 { font-size: clamp(1.5rem, 3.8vw, 2.5rem)  !important; }
h2 { font-size: clamp(1.1rem, 2.2vw, 1.55rem) !important; }
h3 { font-size: clamp(0.95rem, 1.6vw, 1.1rem) !important; }

/* ── Metrics ── */
[data-testid="stMetric"] {
    box-sizing: border-box !important;
    overflow: hidden !important;
    word-break: break-word !important;
    min-width: 0 !important;
}
[data-testid="stMetricValue"] {
    font-size: clamp(1.1rem, 2.5vw, 1.65rem) !important;
}

/* ── Insight row ── */
.insight-row {
    box-sizing: border-box !important;
    overflow: hidden !important;
    word-break: break-word !important;
    width: 100% !important;
}

/* ══ BREAKPOINT: ≤ 1024 px (tablets / heavy zoom) ══════ */
@media screen and (max-width: 1024px) {
    .block-container {
        padding-left:  1.25rem !important;
        padding-right: 1.25rem !important;
    }
    .feature-nav-card {
        padding: 18px 16px !important;
    }
}

/* ══ BREAKPOINT: ≤ 768 px (small tablets / portrait) ════ */
@media screen and (max-width: 768px) {
    .block-container {
        padding-left:  0.85rem !important;
        padding-right: 0.85rem !important;
        padding-top:   1.5rem !important;
    }
    .feature-nav-card {
        padding: 14px 12px !important;
        border-radius: 14px !important;
        margin-bottom: 10px !important;
    }
    .kpi-block {
        padding: 14px 10px !important;
        border-radius: 12px !important;
    }
    .result-price { padding: 20px 0 14px !important; }
    .result-price .amount { font-size: 2rem !important; }
    [data-testid="stMetric"] {
        padding: 14px 14px !important;
        border-radius: 12px !important;
    }
    /* Sidebar stays usable */
    [data-testid="stSidebar"] { min-width: 200px !important;overflow-y: auto !important; }
}
/* Inner scroll fix (VERY IMPORTANT) */
# [data-testid="stSidebar"] > div {
#     height: 100% !important;
#     overflow-y: auto !important;
#     padding-bottom: 80px !important;
# }

/* ══ BREAKPOINT: ≤ 480 px (phones) ════════════════════ */
@media screen and (max-width: 480px) {
    .block-container {
        padding-left:  0.5rem !important;
        padding-right: 0.5rem !important;
    }
    h1 { font-size: 1.3rem !important; }
    h2 { font-size: 1.05rem !important; }
    .feature-nav-card { padding: 12px !important; }
    .kpi-block        { padding: 12px 8px !important; }
    .kpi-val          { font-size: 1.1rem !important; }
    .result-price .amount { font-size: 1.6rem !important; }
    .pg-label { font-size: 0.62rem !important; padding: 4px 10px !important; }
}

/* ══ HIGH-ZOOM SAFETY (> 125 %) ════════════════════════
   When browser zoom goes above ~125 % viewport width
   effectively drops below 768 px — the above breakpoints
   already handle it, but these rules add extra safety.    */
@media screen and (max-width: 900px) {
    [data-testid="stHorizontalBlock"] { flex-wrap: wrap !important; }
    [data-testid="column"] { flex-basis: auto !important; min-width: 0 !important; }
}

</style>
"""

# ── 3-D animated background (uses components.v1.html → JS runs correctly) ────
_BG_JS = """
<!DOCTYPE html>
<html>
<head>
<style>
  html,body{margin:0;padding:0;background:transparent;overflow:hidden;}
  canvas{display:block;}
</style>
</head>
<body>
<canvas id="c"></canvas>
<script>
// Inject canvas into PARENT document (Streamlit page)
(function(){
  var pd = window.parent.document;

  // Remove any previous canvas we injected
  var old = pd.getElementById('propiq-bg-canvas');
  if(old) old.remove();

  // Create canvas in parent document
  var cv = pd.createElement('canvas');
  cv.id  = 'propiq-bg-canvas';
  cv.style.cssText = [
    'position:fixed','top:0','left:0',
    'width:100vw','height:100vh',
    'z-index:0','pointer-events:none',
    'opacity:0.7'
  ].join(';');
  pd.body.appendChild(cv);

  var ctx = cv.getContext('2d');
  var W, H, T = 0;
  var MX = 0, MY = 0;

  function resize(){
    W = cv.width  = pd.documentElement.clientWidth  || window.parent.innerWidth;
    H = cv.height = pd.documentElement.clientHeight || window.parent.innerHeight;
  }
  resize();
  window.parent.addEventListener('resize', resize);
  pd.addEventListener('mousemove', function(e){ MX=e.clientX; MY=e.clientY; });

  /* ─ Palette ─ */
  var C = {
    indigo : [99,102,241],
    cyan   : [6,182,212],
    violet : [139,92,246],
    emerald: [16,185,129],
    rose   : [244,63,94]
  };

  /* ─ Orbs ─ */
  var orbs = [
    {nx:0.12,ny:0.18,r:340,c:C.indigo, s:0.19},
    {nx:0.88,ny:0.80,r:300,c:C.cyan,   s:0.23},
    {nx:0.55,ny:0.42,r:220,c:C.violet, s:0.29},
    {nx:0.25,ny:0.85,r:190,c:C.emerald,s:0.17}
  ];

  /* ─ Icosahedron geometry ─ */
  var PHI = (1+Math.sqrt(5))/2;
  var IV  = [
    [-1,PHI,0],[1,PHI,0],[-1,-PHI,0],[1,-PHI,0],
    [0,-1,PHI],[0,1,PHI],[0,-1,-PHI],[0,1,-PHI],
    [PHI,0,-1],[PHI,0,1],[-PHI,0,-1],[-PHI,0,1]
  ].map(function(v){
    var l=Math.sqrt(v[0]*v[0]+v[1]*v[1]+v[2]*v[2]);
    return[v[0]/l,v[1]/l,v[2]/l];
  });
  var IE = [
    [0,1],[0,5],[0,7],[0,10],[0,11],
    [1,5],[1,7],[1,8],[1,9],
    [2,3],[2,6],[2,10],[2,11],[2,4],
    [3,4],[3,6],[3,8],[3,9],
    [4,5],[4,9],[4,11],[5,9],[5,11],
    [6,7],[6,8],[6,10],
    [7,8],[7,10],[8,9],[10,11]
  ];

  /* ─ Particles ─ */
  var PAL = [
    [99,102,241],[129,140,248],[6,182,212],
    [103,232,249],[165,180,252],[52,211,153]
  ];
  var pts = [];
  for(var i=0;i<75;i++){
    var pc = PAL[Math.floor(Math.random()*PAL.length)];
    pts.push({
      x:Math.random(), y:Math.random(),
      vx:(Math.random()-.5)*0.00014,
      vy:(Math.random()-.5)*0.00014,
      r:Math.random()*1.5+0.5,
      c:pc, ph:Math.random()*Math.PI*2
    });
  }

  /* ─ 3-D projection ─ */
  function project(v,rY,rX,cx,cy,sc){
    var x=v[0],y=v[1],z=v[2];
    var tx=x*Math.cos(rY)+z*Math.sin(rY);
    var tz=-x*Math.sin(rY)+z*Math.cos(rY);
    x=tx; z=tz;
    var ty=y*Math.cos(rX)-z*Math.sin(rX);
    tz=y*Math.sin(rX)+z*Math.cos(rX);
    y=ty; z=tz;
    var f=3.8; var pz=f/(f+z);
    return[cx+x*sc*pz, cy+y*sc*pz, pz];
  }

  /* ─ Draw icosahedron ─ */
  function drawIco(t,cx,cy,sc,speed){
    var rY=t*speed*0.9;
    var rX=t*speed*0.55;
    var pj=IV.map(function(v){return project(v,rY,rX,cx,cy,sc);});

    IE.forEach(function(e){
      var a=pj[e[0]], b=pj[e[1]];
      var alpha=((a[2]+b[2])/2)*0.28;
      var g=ctx.createLinearGradient(a[0],a[1],b[0],b[1]);
      g.addColorStop(0,'rgba(129,140,248,'+alpha+')');
      g.addColorStop(1,'rgba(6,182,212,'+alpha+')');
      ctx.beginPath(); ctx.moveTo(a[0],a[1]); ctx.lineTo(b[0],b[1]);
      ctx.strokeStyle=g; ctx.lineWidth=1; ctx.stroke();
    });

    /* Glowing vertex dots */
    pj.forEach(function(p){
      var gr=ctx.createRadialGradient(p[0],p[1],0,p[0],p[1],p[2]*10);
      gr.addColorStop(0,'rgba(129,140,248,'+(p[2]*0.8)+')');
      gr.addColorStop(0.5,'rgba(99,102,241,'+(p[2]*0.3)+')');
      gr.addColorStop(1,'rgba(99,102,241,0)');
      ctx.beginPath(); ctx.arc(p[0],p[1],p[2]*10,0,Math.PI*2);
      ctx.fillStyle=gr; ctx.fill();

      ctx.beginPath(); ctx.arc(p[0],p[1],p[2]*2.8,0,Math.PI*2);
      ctx.fillStyle='rgba(165,180,252,'+(p[2]*0.9)+')'; ctx.fill();
    });

    /* Outer glow halo */
    var hgr=ctx.createRadialGradient(cx,cy,0,cx,cy,sc*1.6);
    hgr.addColorStop(0,'rgba(99,102,241,0.07)');
    hgr.addColorStop(0.6,'rgba(6,182,212,0.04)');
    hgr.addColorStop(1,'rgba(6,182,212,0)');
    ctx.beginPath(); ctx.arc(cx,cy,sc*1.6,0,Math.PI*2);
    ctx.fillStyle=hgr; ctx.fill();
  }

  /* ─ Draw orbs ─ */
  function drawOrbs(t){
    orbs.forEach(function(o){
      var ox=W*(o.nx+Math.sin(t*o.s)*0.04);
      var oy=H*(o.ny+Math.cos(t*o.s*0.8)*0.035);
      var g=ctx.createRadialGradient(ox,oy,0,ox,oy,o.r);
      g.addColorStop(0,'rgba('+o.c[0]+','+o.c[1]+','+o.c[2]+',0.22)');
      g.addColorStop(0.5,'rgba('+o.c[0]+','+o.c[1]+','+o.c[2]+',0.07)');
      g.addColorStop(1,'rgba('+o.c[0]+','+o.c[1]+','+o.c[2]+',0)');
      ctx.beginPath(); ctx.arc(ox,oy,o.r,0,Math.PI*2);
      ctx.fillStyle=g; ctx.fill();
    });
  }

  /* ─ Light rays ─ */
  function drawRays(t){
    var cx=W*0.5+Math.sin(t*0.18)*W*0.1;
    var cy=-60;
    for(var i=0;i<8;i++){
      var ang=(i/8)*Math.PI*0.75-Math.PI*0.375+Math.sin(t*0.12+i)*0.07;
      var ex=cx+Math.sin(ang)*H*1.5;
      var ey=cy+Math.cos(ang)*H*1.5;
      var a=0.016+0.01*Math.sin(t*0.35+i*1.2);
      var g=ctx.createLinearGradient(cx,cy,ex,ey);
      g.addColorStop(0,'rgba(129,140,248,'+(a*3)+')');
      g.addColorStop(0.45,'rgba(99,102,241,'+a+')');
      g.addColorStop(1,'rgba(6,182,212,0)');
      ctx.beginPath(); ctx.moveTo(cx,cy); ctx.lineTo(ex,ey);
      ctx.strokeStyle=g; ctx.lineWidth=28+i*7; ctx.stroke();
    }
  }

  /* ─ Hex grid ─ */
  function drawHex(t){
    var S=50;
    var cols=Math.ceil(W/(S*1.732))+2;
    var rows=Math.ceil(H/(S*1.5))+2;
    for(var r=-1;r<rows;r++){
      for(var c=-1;c<cols;c++){
        var hx=c*S*1.732+(r%2===0?0:S*0.866);
        var hy=r*S*1.5;
        var w=Math.sin(hx*0.007+t*0.55)*Math.cos(hy*0.007+t*0.38);
        var a=0.022+0.016*w;
        ctx.beginPath();
        for(var k=0;k<6;k++){
          var ang=(Math.PI/3)*k-Math.PI/6;
          var px=hx+S*0.86*Math.cos(ang);
          var py=hy+S*0.86*Math.sin(ang);
          k===0?ctx.moveTo(px,py):ctx.lineTo(px,py);
        }
        ctx.closePath();
        ctx.strokeStyle='rgba(99,102,241,'+a+')';
        ctx.lineWidth=0.6; ctx.stroke();
        if(w>0.72){
          ctx.fillStyle='rgba(99,102,241,'+(a*0.35)+')';
          ctx.fill();
        }
      }
    }
  }

  /* ─ Particles ─ */
  function drawPts(t){
    /* Connection lines */
    for(var i=0;i<pts.length;i++){
      for(var j=i+1;j<pts.length;j++){
        var dx=(pts[i].x-pts[j].x)*W;
        var dy=(pts[i].y-pts[j].y)*H;
        var d=Math.sqrt(dx*dx+dy*dy);
        if(d<130){
          ctx.beginPath();
          ctx.moveTo(pts[i].x*W,pts[i].y*H);
          ctx.lineTo(pts[j].x*W,pts[j].y*H);
          ctx.strokeStyle='rgba(129,140,248,'+((1-d/130)*0.15)+')';
          ctx.lineWidth=0.5; ctx.stroke();
        }
      }
    }
    /* Dots */
    pts.forEach(function(p){
      p.ph+=0.017;
      p.x=(p.x+p.vx+1)%1;
      p.y=(p.y+p.vy+1)%1;
      var mx=p.x*W-MX, my=p.y*H-MY;
      var md=Math.sqrt(mx*mx+my*my);
      if(md<110&&md>0){p.vx+=(mx/md)*0.00004;p.vy+=(my/md)*0.00004;}
      p.vx*=0.998; p.vy*=0.998;
      var al=0.45+0.3*Math.sin(p.ph);
      var rr=p.r*(1+0.2*Math.sin(p.ph));
      ctx.beginPath();
      ctx.arc(p.x*W,p.y*H,rr,0,Math.PI*2);
      ctx.fillStyle='rgba('+p.c[0]+','+p.c[1]+','+p.c[2]+','+al+')';
      ctx.fill();
      /* Glow */
      var gr=ctx.createRadialGradient(p.x*W,p.y*H,0,p.x*W,p.y*H,rr*8);
      gr.addColorStop(0,'rgba('+p.c[0]+','+p.c[1]+','+p.c[2]+',0.12)');
      gr.addColorStop(1,'rgba('+p.c[0]+','+p.c[1]+','+p.c[2]+',0)');
      ctx.beginPath();
      ctx.arc(p.x*W,p.y*H,rr*8,0,Math.PI*2);
      ctx.fillStyle=gr; ctx.fill();
    });
  }

  /* ─ Scan line ─ */
  function drawScan(t){
    var y=(t*26)%H;
    var g=ctx.createLinearGradient(0,y-55,0,y+55);
    g.addColorStop(0,'rgba(99,102,241,0)');
    g.addColorStop(0.5,'rgba(99,102,241,0.032)');
    g.addColorStop(1,'rgba(99,102,241,0)');
    ctx.fillStyle=g; ctx.fillRect(0,y-55,W,110);
  }

  /* ─ Main loop ─ */
  function loop(ts){
    T = ts*0.001;
    ctx.clearRect(0,0,W,H);

    /* Base fill */
    ctx.fillStyle='#0f172a';
    ctx.fillRect(0,0,W,H);

    drawOrbs(T);
    drawRays(T);
    drawHex(T);

    /* Two icosahedra — different sizes, speeds, positions */
    drawIco(T, W*0.80, H*0.20, Math.min(W,H)*0.115, 1.0);
    drawIco(T, W*0.12, H*0.78, Math.min(W,H)*0.072, 0.7);

    drawPts(T);
    drawScan(T);

    requestAnimationFrame(loop);
  }

  requestAnimationFrame(loop);
})();
</script>
</body>
</html>
"""


# ── Public API ────────────────────────────────────────────────────────────────

def inject_css():
    """Inject global CSS styles. Call immediately after set_page_config."""
    import streamlit as st
    st.markdown(BASE_CSS, unsafe_allow_html=True)


def inject_animated_bg():
    """
    Inject the 3-D animated canvas background.
    Uses st.components.v1.html so JavaScript actually executes.
    The canvas is injected into window.parent.document (the real Streamlit page).
    height=0 makes the iframe invisible.
    """
    import streamlit.components.v1 as components
    components.html(_BG_JS, height=0, scrolling=False)