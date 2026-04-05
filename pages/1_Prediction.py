"""
╔══════════════════════════════════════════════════════════════════╗
║              PropIQ — Property Price Predictor                   ║
║  Page  : pages/1_Prediction.py                                   ║
║  Role  : Collects property details from the user, calls the      ║
║          FastAPI prediction endpoint, and renders the estimated  ║
║          price with market context and a confidence range.       ║
╚══════════════════════════════════════════════════════════════════╝

Dependencies (must be installed):
    requests, streamlit, pandas, numpy, pickle, plotly

Environment variable used:
    API_URL  →  base URL of the FastAPI backend
                default: "http://127.0.0.1:8000"  (local dev)
                Docker : "http://api:8000"         (set in docker-compose.yml)
"""

# ── Standard library ──────────────────────────────────────────────────────────
import os
import sys
import pickle

# ── Third-party ───────────────────────────────────────────────────────────────
import requests
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# ── Internal ──────────────────────────────────────────────────────────────────
# Add project root to sys.path so Utils can be imported from any working dir
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from Utils.Styles import inject_css, inject_animated_bg, PLOTLY_THEME

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="PropIQ · Predict",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_css()
inject_animated_bg()

# ══════════════════════════════════════════════════════════════════════════════
#  CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════

# Confidence band added / subtracted from the point estimate (in Crores)
CONFIDENCE_BAND_CR = 0.22

# API base URL — reads from environment so it works both locally and in Docker
# docker-compose.yml sets:  environment: API_URL=http://api:8000
API_BASE_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# ══════════════════════════════════════════════════════════════════════════════
#  DATA LOADING
# ══════════════════════════════════════════════════════════════════════════════

@st.cache_resource
def load_reference_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load reference DataFrames used to populate form dropdowns and
    compute sector-level market averages.

    Returns
    -------
    df       : Full property DataFrame (used for dropdown options).
    price_df : Sector-level price summary (used for market context metrics).

    Note
    ----
    Uses st.cache_resource so the files are read from disk only once
    per Streamlit server session, not on every page interaction.
    """
    with open("Models/df.pkl",       "rb") as f:
        df = pickle.load(f)
    with open("Models/price_df.pkl", "rb") as f:
        price_df = pickle.load(f)
    return df, price_df


df, price_df = load_reference_data()

# ══════════════════════════════════════════════════════════════════════════════
#  API HELPER
# ══════════════════════════════════════════════════════════════════════════════

def fetch_predicted_price(input_data: dict) -> float | None:
    """
    POST property features to the FastAPI /predict endpoint and return
    the predicted price in Crores (₹).

    Parameters
    ----------
    input_data : dict
        Keys must match the Pydantic model in API/Validator/Input_Validation.py:
        property_Type, sector, bedRooms, bathrooms, balconies,
        built_up_area, servent_room, store_room, floor_category.

    Returns
    -------
    float | None
        Predicted price in Crores, or None if the request failed.

    Raises
    ------
    Displays a Streamlit error message on any network or API failure;
    does not raise to the caller.
    """
    url = f"{API_BASE_URL}/predict"
    try:
        response = requests.post(url, json=input_data, timeout=10)
        response.raise_for_status()          # raises HTTPError for 4xx / 5xx
        return float(response.json()["price"])

    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot reach the prediction API. Is the FastAPI server running?")
    except requests.exceptions.Timeout:
        st.error("⏱️ Request timed out. The API took too long to respond.")
    except requests.exceptions.HTTPError as e:
        st.error(f"🚨 API returned an error: {e.response.status_code} — {e.response.text}")
    except (KeyError, ValueError):
        st.error("⚠️ Unexpected response format from the API.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

    return None

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE HEADER
# ══════════════════════════════════════════════════════════════════════════════

st.markdown(
    '<span class="pg-label pg-label-indigo">AI Valuation Engine</span>',
    unsafe_allow_html=True,
)
st.markdown("""
<h1 style="margin:12px 0 8px">
    Property Price
    <span class="gradient-text">Predictor</span>
</h1>
<p style="color:#94a3b8;margin:0 0 22px;font-size:0.98rem;max-width:560px">
    Enter your property details below and get an instant AI-powered
    market valuation with a confidence range.
</p>
""", unsafe_allow_html=True)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  INPUT FORM
# ══════════════════════════════════════════════════════════════════════════════

st.markdown(
    '<div class="section-label">Property details</div>',
    unsafe_allow_html=True,
)

with st.container(border=True):
    col_location, col_config, col_area = st.columns(3, gap="large")

    # ── Column 1: Location & property type ───────────────────────────────────
    with col_location:
        st.markdown("**📍 Location & Type**")

        property_type = st.selectbox(
            "Property type",
            options=["flat", "house"],
        )
        sector = st.selectbox(
            "Sector",
            options=sorted(df["sector"].unique().tolist()),
        )
        floor_category = st.selectbox(
            "Floor",
            options=sorted(df["floor_category"].unique().tolist()),
        )

    # ── Column 2: BHK configuration ──────────────────────────────────────────
    with col_config:
        st.markdown("**🛏 Configuration**")

        bedrooms = int(st.selectbox(
            "Bedrooms",
            options=sorted(df["bedRoom"].unique().tolist()),
        ))
        bathroom = float(st.selectbox(
            "Bathrooms",
            options=sorted(df["bathroom"].unique().tolist()),
        ))
        balcony = st.selectbox(
            "Balconies",
            options=sorted(df["balcony"].unique().tolist()),
        )

    # ── Column 3: Area & bonus rooms ─────────────────────────────────────────
    with col_area:
        st.markdown("**📐 Area & Amenities**")

        built_up_area = float(st.number_input(
            "Built-up area (sqft)",
            min_value=100.0,
            step=50.0,
            value=1200.0,
        ))
        servant_room = float(st.selectbox(
            "Servant room",
            options=[0.0, 1.0],
            format_func=lambda x: "✅ Yes" if x == 1.0 else "❌ No",
        ))
        store_room = float(st.selectbox(
            "Store room",
            options=[0.0, 1.0],
            format_func=lambda x: "✅ Yes" if x == 1.0 else "❌ No",
        ))

# ── Predict button (centred) ──────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
_, btn_col, _ = st.columns([2, 1.5, 2])
with btn_col:
    predict_clicked = st.button("🚀  Estimate Price", use_container_width=True)
st.markdown("<div style='margin-bottom:40px'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PREDICTION & RESULTS
# ══════════════════════════════════════════════════════════════════════════════

if predict_clicked:

    # ── Basic client-side validation ─────────────────────────────────────────
    if built_up_area < 100:
        st.error("Please enter a valid built-up area (minimum 100 sqft).")
        st.stop()

    # ── Build the payload that matches the Pydantic model ────────────────────
    # Field names must exactly match predict_IP_validation in
    # API/Validator/Input_Validation.py
    payload = {
        "property_Type": property_type,
        "sector":        sector,
        "bedRooms":      bedrooms,
        "bathrooms":     int(bathroom),
        "balconies":     str(balcony),
        "built_up_area": built_up_area,
        "servent_room":  int(servant_room),
        "store_room":    int(store_room),
        "floor_category": floor_category,
    }

    # ── Call FastAPI ──────────────────────────────────────────────────────────
    with st.spinner("Calculating estimate…"):
        base_price = fetch_predicted_price(payload)

    if base_price is None:
        # Error already shown inside fetch_predicted_price
        st.stop()

    # ── Confidence range ──────────────────────────────────────────────────────
    price_low  = max(0.0, base_price - CONFIDENCE_BAND_CR)
    price_high = base_price + CONFIDENCE_BAND_CR

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ── Headline price display ────────────────────────────────────────────────
    st.markdown(f"""
    <div class="result-price">
        <div class="eyebrow">Estimated Market Value</div>
        <div class="amount">₹ {base_price:.2f} Cr</div>
        <div class="range">
            Confidence range &nbsp;·&nbsp;
            ₹{price_low:.2f} Cr — ₹{price_high:.2f} Cr
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Three estimate cards ──────────────────────────────────────────────────
    col_low, col_mid, col_high = st.columns(3, gap="medium")

    estimate_cards = [
        (col_low,  "Lower estimate", price_low,  "#f87171", "rgba(248,113,113,0.2)", "Conservative"),
        (col_mid,  "Expected price", base_price, "#818cf8", "rgba(99,102,241,0.3)",  "Model prediction"),
        (col_high, "Upper estimate", price_high, "#67e8f9", "rgba(6,182,212,0.2)",   "Optimistic"),
    ]

    for col, label, val, text_clr, border_clr, note in estimate_cards:
        col.markdown(f"""
        <div class="kpi-block" style="border-color:{border_clr}">
            <div style="font-size:0.68rem;color:#475569;text-transform:uppercase;
                 letter-spacing:0.09em;margin-bottom:7px">{label}</div>
            <div class="kpi-val" style="color:{text_clr}">₹{val:.2f} Cr</div>
            <div style="font-size:0.73rem;color:#475569;margin-top:5px">{note}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    #  MARKET CONTEXT
    # ══════════════════════════════════════════════════════════════════════════

    # Compute sector-level statistics for the selected sector
    sector_prices = price_df[price_df["sector"] == sector]["price"]
    avg_sector    = float(sector_prices.mean()) if len(sector_prices) > 0 else base_price
    price_per_sqft = (base_price * 1e7 / built_up_area) if built_up_area > 0 else 0.0
    diff_pct       = ((base_price - avg_sector) / avg_sector * 100) if avg_sector > 0 else 0.0
    is_above_avg   = base_price >= avg_sector

    ctx_col, chart_col = st.columns([3, 2], gap="large")

    # ── Context metrics ───────────────────────────────────────────────────────
    with ctx_col:
        st.markdown(
            '<div class="section-label">Market context</div>',
            unsafe_allow_html=True,
        )
        with st.container(border=True):
            metric_left, metric_right = st.columns(2)
            metric_left.metric("Sector avg price", f"₹{avg_sector:.2f} Cr")
            metric_right.metric("Price per sqft",  f"₹{price_per_sqft:,.0f}")

            vs_color = "#6ee7b7" if is_above_avg else "#f87171"
            vs_arrow = "↑ above" if is_above_avg else "↓ below"

            st.markdown(f"""
            <div style="background:rgba(15,23,42,0.9);
                 border:1px solid rgba(148,163,184,0.12);
                 border-radius:12px;padding:16px 20px;margin-top:6px; margin-bottom:10px;">
                <div style="font-size:0.68rem;color:#475569;text-transform:uppercase;
                     letter-spacing:0.09em;margin-bottom:8px">vs sector average</div>
                <span style="font-family:'Outfit',sans-serif;font-size:1.65rem;
                      font-weight:800;color:{vs_color}">
                    {abs(diff_pct):.1f}% {vs_arrow}
                </span>
                <span style="font-size:0.82rem;color:#64748b;margin-left:10px">
                    the {sector} average
                </span>
            </div>
            """, unsafe_allow_html=True)

    # ── Price range bar chart ─────────────────────────────────────────────────
    with chart_col:
        st.markdown(
            '<div class="section-label">Price range chart</div>',
            unsafe_allow_html=True,
        )

        fig_bar = go.Figure(go.Bar(
            x=["Lower", "Expected", "Upper"],
            y=[price_low, base_price, price_high],
            marker_color=["#f87171", "#818cf8", "#67e8f9"],
            text=[f"₹{v:.2f}Cr" for v in [price_low, base_price, price_high]],
            textposition="outside",
            textfont=dict(color="#e2e8f0", size=11),
        ))

        # Sector average reference line
        if avg_sector > 0:
            fig_bar.add_hline(
                y=avg_sector,
                line_dash="dot",
                line_color="rgba(255,255,255,0.22)",
                annotation_text=f"Sector avg ₹{avg_sector:.2f}Cr",
                annotation_font_color="#94a3b8",
                annotation_font_size=10,
            )

        bar_layout = dict(**PLOTLY_THEME)
        bar_layout.update(
            title="Price range",
            height=265,
            showlegend=False,
            yaxis_title="Price (Cr ₹)",
            yaxis_range=[0, price_high * 1.3],
        )
        fig_bar.update_layout(**bar_layout)
        st.plotly_chart(fig_bar, use_container_width=True)

    # ══════════════════════════════════════════════════════════════════════════
    #  PROPERTY SUMMARY STRIP
    # ══════════════════════════════════════════════════════════════════════════

    st.markdown(
        '<div class="section-label" style="margin-top:6px">Property summary</div>',
        unsafe_allow_html=True,
    )

    # Key-value pairs shown in the summary row
    summary_fields = {
        "Type":         property_type.title(),
        "Sector":       sector,
        "Bedrooms":     int(bedrooms),
        "Bathrooms":    int(bathroom),
        "Area":         f"{built_up_area:,.0f} sqft",
        "Floor":        floor_category,
        "Servant room": "Yes" if servant_room == 1.0 else "No",
        "Store room":   "Yes" if store_room   == 1.0 else "No",
    }

    with st.container(border=True):
        summary_cols = st.columns(len(summary_fields))
        for col, (label, value) in zip(summary_cols, summary_fields.items()):
            col.markdown(f"""
            <div style="text-align:center;padding:6px 0">
                <div style="font-size:0.62rem;color:#475569;text-transform:uppercase;
                     letter-spacing:0.07em;margin-bottom:20px">{label}</div>
                <div style="font-size:0.88rem;font-weight:600;color:#e2e8f0">{value}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:50px'></div>", unsafe_allow_html=True)