import streamlit as st
from Utils.Styles import inject_css, inject_animated_bg

st.set_page_config(
    page_title="PropIQ — Real Estate Intelligence",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_css()
inject_animated_bg()

# ── HERO ──────────────────────────────────────────────────────────────────────
left, right = st.columns([3, 2], gap="large")

with left:
    # st.markdown('<span class="pg-label pg-label-indigo">🔴 Live Market Data</span>',
    #             unsafe_allow_html=True)
    st.markdown("""
    <h1 style="margin:14px 0 14px;line-height:1.1">
        Smart Real Estate<br>
        <span class="gradient-text">Intelligence Platform</span>
    </h1>
    <p style="font-size:1.02rem;color:#94a3b8;line-height:1.85;
        max-width:500px;margin:0 0 28px">
        AI-powered property valuation, sector analytics, smart recommendations
        and data-driven price insights — everything a buyer, seller or investor needs.
    </p>
    """, unsafe_allow_html=True)

    b1, b2, _ = st.columns([1.4, 1.3, 1])
    with b1:
        if st.button("🚀  Get a Valuation", use_container_width=True):
            st.switch_page("pages/1_Prediction.py")
    with b2:
        if st.button("📊  Explore Market", use_container_width=True):
            st.switch_page("pages/2_Analysis.py")

with right:
    st.markdown("""
    <div style="background:rgba(19,32,64,0.85);
         border:1px solid rgba(99,102,241,0.22);
         border-radius:20px;padding:26px;margin-top:6px;
         backdrop-filter:blur(10px)">
        <div class="section-label" style="margin-bottom:20px">
            Platform at a glance</div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px">
            <div class="kpi-block">
                <div class="kpi-val" style="color:#818cf8">3,600+</div>
                <div class="kpi-lbl">Properties</div>
            </div>
            <div class="kpi-block">
                <div class="kpi-val" style="color:#67e8f9">95+</div>
                <div class="kpi-lbl">Sectors</div>
            </div>
            <div class="kpi-block">
                <div class="kpi-val" style="color:#6ee7b7">90.3%</div>
                <div class="kpi-lbl">Model R²</div>
            </div>
            <div class="kpi-block">
                <div class="kpi-val"
                     style="color:#fde68a;font-size:1.25rem">₹0.4–31Cr</div>
                <div class="kpi-lbl">Price range</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── FEATURE CARDS ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">What you can do</div>',
            unsafe_allow_html=True)

cards = [
    ("🏠", "Price Predictor",      "indigo", "pages/1_Prediction.py",
     "Enter property details and get an instant AI-powered valuation with a confidence range."),
    ("📊", "Analytics Dashboard",  "cyan",   "pages/2_Analysis.py",
     "Interactive heatmaps, price distributions, BHK analysis and sector comparisons."),
    ("🤖", "Smart Recommender",    "green",  "pages/3_Recommendation.py",
     "Find nearby properties and discover similar listings using AI similarity scoring."),
    ("💡", "Price Insights",       "amber",  "pages/4_Insights.py",
     "Understand which features drive prices and by exactly how much — backed by statistics."),
]

cols = st.columns(4, gap="medium")
accent_map = {
    "indigo": "#818cf8", "cyan": "#67e8f9",
    "green":  "#6ee7b7", "amber": "#fde68a",
}
for col, (icon, title, color, page, desc) in zip(cols, cards):
    with col:
        acc = accent_map[color]
        st.markdown(f"""
        <div class="feature-nav-card">
            <div>
                <div style="font-size:2.2rem;margin-bottom:12px">{icon}</div>
                <div style="font-family:'Outfit',sans-serif;font-size:0.97rem;
                     font-weight:700;color:#f1f5f9;margin-bottom:8px">{title}</div>
                <p style="font-size:0.8rem;color:#64748b;line-height:1.6;margin:0">
                    {desc}</p>
            </div>
            
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open", key=f"nav_{title}", use_container_width=True):
            st.switch_page(page)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── HOW IT WORKS ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">How the prediction model works</div>',
            unsafe_allow_html=True)

steps = [
    ("01", "Enter property details",
     "Type, location, BHK, built-up area, floor, amenities and more"),
    ("02", "Feature engineering",
     "Pipeline auto-computes area/BHK ratio and encodes categorical variables"),
    ("03", "ML pipeline runs",
     "Preprocessor → trained regression model → log-scale price prediction"),
    ("04", "Estimate returned",
     "Predicted price with ± confidence range displayed in Crores ₹"),
]

step_cols = st.columns(4, gap="medium")
for col, (num, title, desc) in zip(step_cols, steps):
    col.markdown(f"""
    <div style="background:rgba(19,32,64,0.8);
         border:1px solid rgba(148,163,184,0.09);
         border-radius:16px;padding:24px 20px;min-height:156px;
         display:flex;flex-direction:column;justify-content:flex-start;
         backdrop-filter:blur(6px)">
        <div style="font-family:'Outfit',sans-serif;font-size:2rem;
             font-weight:800;color:rgba(99,102,241,0.22);
             line-height:1;margin-bottom:14px">{num}</div>
        <div style="font-family:'Outfit',sans-serif;font-size:0.9rem;
             font-weight:700;color:#e2e8f0;margin-bottom:7px">{title}</div>
        <div style="font-size:0.77rem;color:#64748b;line-height:1.6">{desc}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── TRUST STRIP ───────────────────────────────────────────────────────────────
# t1, t2, t3, t4 = st.columns(4, gap="medium")
# trust = [
#     ("🔒", "Private & secure",     "Your data never leaves the app"),
#     ("⚡", "Instant results",       "Predictions in under a second"),
#     ("📈", "Statistically rigorous","OLS-validated price driver analysis"),
#     ("🗺️", "Location-aware",        "Sector-level granularity in every estimate"),
# ]
# for col, (icon, title, desc) in zip([t1,t2,t3,t4], trust):
#     col.markdown(f"""
#     <div style="text-align:center;padding:20px 12px">
#         <div style="font-size:1.8rem;margin-bottom:8px">{icon}</div>
#         <div style="font-family:'Outfit',sans-serif;font-size:0.88rem;
#              font-weight:700;color:#e2e8f0;margin-bottom:4px">{title}</div>
#         <div style="font-size:0.76rem;color:#475569;line-height:1.5">{desc}</div>
#     </div>
#     """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center;color:#334155;font-size:0.74rem;
     padding:20px 0 4px;margin-top:12px">
    PropIQ · Real Estate Intelligence ·
    Built with Streamlit · scikit-learn · statsmodels · Plotly
</div>
""", unsafe_allow_html=True)