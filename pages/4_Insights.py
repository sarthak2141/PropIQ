import streamlit as st
import pickle
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from Utils.Styles import inject_css, inject_animated_bg, PLOTLY_THEME

st.set_page_config(
    page_title="PropIQ · Insights",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_css()
inject_animated_bg()

# ── Load insights ─────────────────────────────────────────────────────────────
@st.cache_data
def load_insights():
    with open("Models/insights.pkl", "rb") as f:
        return pickle.load(f)
    # return None
    # base = os.path.dirname(os.path.dirname(__file__))
    # for path in [
    #     os.path.join(base, "models", "insights.pkl"),
    #     "dataset/insights.pkl",
    #     "insights.pkl",
    # ]:
    #     if os.path.exists(path):


insights = load_insights()
if insights is None:
    st.error(
        "**insights.pkl not found.**  \n"
        "Run your Jupyter notebook to generate `models/insights.pkl` first."
    )
    st.stop()

# ── Feature metadata ──────────────────────────────────────────────────────────
LABELS = {
    "bedRoom":         "Bedrooms",
    "bathroom":        "Bathrooms",
    "built_up_area":   "Built-up Area",
    "servent room":    "Servant Room",
    "property_type":   "Property Type",
    "furnishing_type": "Furnishing",
    "luxury_category": "Luxury Category",
}
UNITS = {
    "bedRoom":         "per bedroom added",
    "bathroom":        "per bathroom added",
    "built_up_area":   "per 100 sqft added",
    "servent room":    "no room → with servant room",
    "property_type":   "flat → house",
    "furnishing_type": "per furnishing level up",
    "luxury_category": "per luxury level up",
}

# ── Build dataframe ───────────────────────────────────────────────────────────
rows = []
for key, val in insights.items():
    rows.append({
        "key":       key,
        "Feature":   LABELS.get(key, key),
        "Unit":      UNITS.get(key, "per unit"),
        "pct":       float(val.get("pct_change",      0)),
        "lakh":      float(val.get("abs_change_lakh", 0)),
        "pval":      float(val.get("p_value",         1)),
        "sig":       bool(val.get("significant",      False)),
        "ci_lo":     float(val.get("ci_low_pct",  val.get("pct_change", 0) * 0.7)),
        "ci_hi":     float(val.get("ci_high_pct", val.get("pct_change", 0) * 1.3)),
        "direction": str(val.get("direction", "increases")),
    })

if not rows:
    st.error("insights.pkl is empty or malformed.")
    st.stop()

df = pd.DataFrame(rows).sort_values("pct", ascending=False).reset_index(drop=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<span class="pg-label pg-label-amber">Price Driver Analysis</span>',
            unsafe_allow_html=True)
st.markdown("""
<h1 style="margin:12px 0 8px">
    What Drives <span class="gradient-text">Property Prices?</span>
</h1>
<p style="color:#94a3b8;max-width:620px;margin:0 0 18px;font-size:0.98rem">
    OLS regression analysis showing how each feature independently affects price,
    holding all other variables constant. Every effect is statistically tested.
</p>
""", unsafe_allow_html=True)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Driver summary cards ──────────────────────────────────────────────────────
st.markdown('<div class="section-label">Key price drivers</div>',
            unsafe_allow_html=True)

driver_cols = st.columns(len(df), gap="small")
for col, (idx, row) in zip(driver_cols, df.iterrows()):
    is_top   = idx < 3
    bg       = "rgba(22,37,72,0.9)"   if is_top else "rgba(19,32,64,0.8)"
    border   = ("rgba(99,102,241,0.45)" if is_top
                else "rgba(148,163,184,0.1)")
    val_clr  = "#6ee7b7" if row["direction"] == "increases" else "#f87171"
    arrow    = "↑"       if row["direction"] == "increases" else "↓"
    sig_html = (
        '<span style="font-size:0.62rem;color:#6ee7b7;font-weight:700">✓ sig</span>'
        if row["sig"] else
        '<span style="font-size:0.62rem;color:#f87171">✗ n/s</span>'
    )
    col.markdown(f"""
    <div style="background:{bg};border:1px solid {border};
         border-radius:14px;padding:16px 12px;text-align:center">
        <div style="font-size:0.66rem;color:#475569;margin-bottom:6px;
             overflow:hidden;text-overflow:ellipsis;white-space:nowrap">
            {row['Feature']}</div>
        <div style="font-family:'Outfit',sans-serif;font-size:1.3rem;
             font-weight:800;color:{val_clr}">
            {arrow}{abs(row['pct']):.1f}%</div>
        <div style="font-size:0.67rem;color:#475569;margin:4px 0">
            ₹{abs(row['lakh']):.1f}L / unit</div>
        {sig_html}
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Shared left-margin helper ─────────────────────────────────────────────────
# Approximates the pixel width needed so y-axis labels are never clipped.
# ~8 px per character is a safe estimate for the 12 px DM Sans font Plotly uses.
_max_label_len = max(len(str(r["Feature"])) for _, r in df.iterrows())
_left_margin   = max(120, _max_label_len * 8)

# ── Chart + table ─────────────────────────────────────────────────────────────
chart_col, table_col = st.columns([3, 2], gap="large")

with chart_col:
    st.markdown('<div class="section-label">Price impact per feature</div>',
                unsafe_allow_html=True)
    st.caption("% price change for one-unit increase.")

    bar_colors = [
        "#6ee7b7" if r["direction"] == "increases" else "#f87171"
        for _, r in df.iterrows()
    ]
    err_hi = [max(0.0, float(r["ci_hi"]) - float(r["pct"])) for _, r in df.iterrows()]
    err_lo = [max(0.0, float(r["pct"])   - float(r["ci_lo"])) for _, r in df.iterrows()]

    fig = go.Figure(go.Bar(
        y=df["Feature"], x=df["pct"],
        orientation="h",
        marker=dict(color=bar_colors, opacity=0.84, line=dict(width=0)),
        error_x=dict(
            type="data", symmetric=False,
            array=err_hi, arrayminus=err_lo,
            color="rgba(255,255,255,0.25)", thickness=1.5, width=6,
        ),
        text=[f"{'+' if r['pct']>0 else ''}{r['pct']:.1f}%"
              for _, r in df.iterrows()],
        textposition="outside",
        textfont=dict(color="#e2e8f0", size=11),
        hovertemplate=(
            "<b>%{y}</b><br>"
            "% Change: %{x:.2f}%<br>"
            "₹ Impact: ₹%{customdata:.1f}L<extra></extra>"
        ),
        customdata=df["lakh"].abs().tolist(),
    ))
    fig.add_vline(x=0, line_color="rgba(255,255,255,0.14)", line_width=1)
    lyt = dict(**PLOTLY_THEME)
    lyt.update(
        title="Feature Impact on Price %",
        height=360, showlegend=False,
        xaxis_title="% price change per unit increase",
        yaxis={**PLOTLY_THEME["yaxis"], "autorange": "reversed"},
        margin=dict(l=_left_margin, r=72, t=50, b=40),   # ← fixed
    )
    fig.update_layout(**lyt)
    st.plotly_chart(fig, use_container_width=True)

with table_col:
    st.markdown('<div class="section-label">Detailed breakdown</div>',
                unsafe_allow_html=True)
    max_pct = df["pct"].abs().max() or 1.0

    for _, row in df.iterrows():
        val_clr = "#6ee7b7" if row["direction"] == "increases" else "#f87171"
        arrow   = "↑"       if row["direction"] == "increases" else "↓"
        bar_w   = int(abs(row["pct"]) / max_pct * 100)
        sig_clr = "#6ee7b7" if row["sig"] else "#f87171"
        sig_dot = "●"       if row["sig"] else "○"

        st.markdown(f"""
        <div class="insight-row">
            <div style="display:flex;justify-content:space-between;
                 align-items:flex-start;margin-bottom:8px">
                <div>
                    <div style="font-size:0.84rem;font-weight:600;
                         color:#e2e8f0">{row['Feature']}</div>
                    <div style="font-size:0.68rem;color:#475569;margin-top:2px">
                        {row['Unit']}</div>
                </div>
                <div style="text-align:right;flex-shrink:0;margin-left:8px">
                    <div style="font-family:'Outfit',sans-serif;font-size:1rem;
                         font-weight:700;color:{val_clr}">
                        {arrow}{abs(row['pct']):.1f}%</div>
                    <div style="font-size:0.68rem;color:#475569">
                        ₹{abs(row['lakh']):.1f}L</div>
                </div>
            </div>
            <div style="height:3px;background:rgba(148,163,184,0.1);
                 border-radius:3px;margin-bottom:7px;overflow:hidden">
                <div style="height:100%;width:{bar_w}%;
                     background:{val_clr};border-radius:3px;opacity:0.72"></div>
            </div>
            <div style="display:flex;justify-content:space-between">
                <span style="font-size:0.64rem;color:#475569">
                    CI: {row['ci_lo']:.1f}% — {row['ci_hi']:.1f}%</span>
                <span style="font-size:0.64rem;color:{sig_clr};font-weight:600">
                    {sig_dot} p = {row['pval']:.4f}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Absolute ₹ impact ─────────────────────────────────────────────────────────
st.markdown(
    '<div class="section-label">Absolute impact in ₹ Lakh</div>',
    unsafe_allow_html=True)
st.caption("Rupee value added when you improve each feature by one unit")

chart_df = df.sort_values("lakh", ascending=True)
fig2 = px.bar(
    chart_df, x="lakh", y="Feature", orientation="h",
    color="lakh",
    color_continuous_scale=[[0,"#0f172a"],[0.5,"#6366f1"],[1,"#a5b4fc"]],
    text=chart_df["lakh"].apply(lambda x: f"₹{abs(x):.1f}L"),
    labels={"lakh":"₹ Lakh impact","Feature":""},
)
fig2.update_traces(textposition="outside", textfont_color="#e2e8f0")
lyt2 = dict(**PLOTLY_THEME)
lyt2.update(
title="Feature Impact on Price",
    height=300, showlegend=False, coloraxis_showscale=False,
    margin=dict(l=_left_margin, r=80, t=50, b=40,),       # ← fixed
)
fig2.update_layout(**lyt2)
st.plotly_chart(fig2, use_container_width=True)

# # ── Methodology ───────────────────────────────────────────────────────────────
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
# with st.container(border=True):
#     st.markdown("""
#     <div style="font-size:0.78rem;color:#ffffff;text-transform:uppercase;
#          letter-spacing:0.1em;font-weight:900;margin-bottom:10px">
#          Methodology</div>
#     <div class="info-box">
#         <p>
#             Effects estimated via
#             <strong style="color:#818cf8">OLS regression</strong>
#             (R² = 0.846, 3,639 observations) on StandardScaled features with
#             log1p-transformed price target.
#             Per-unit formula:
#             <code>% change = (exp(β / σ) − 1) × 100</code>
#             where σ is the feature's original standard deviation.
#             Confidence intervals are 95% OLS bounds.
#             <strong>Significant</strong> = p-value &lt; 0.05.
#             Absolute ₹ estimates use the dataset median price as reference.
#         </p>
#     </div>
#     """, unsafe_allow_html=True)