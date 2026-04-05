import streamlit as st
import pandas as pd
import pickle
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from Utils.Styles import inject_css,inject_animated_bg

st.set_page_config(page_title="PropIQ · Recommend", page_icon="🤖", layout="wide")
inject_css()
inject_animated_bg()

# ── LOAD DATA ───────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    with open("Models/location_df.pkl", "rb") as f:
        loc = pickle.load(f)
    with open("Models/cosine_sim1.pkl", "rb") as f:
        cs1 = pickle.load(f)
    with open("Models/cosine_sim2.pkl", "rb") as f:
        cs2 = pickle.load(f)
    with open("Models/cosine_sim3.pkl", "rb") as f:
        cs3 = pickle.load(f)
    return loc, cs1, cs2, cs3

location_df, cosine_sim1, cosine_sim2, cosine_sim3 = load_data()

# ── SESSION STATE ────────────────────────────────────────────────────────────
if "result_df"    not in st.session_state: st.session_state.result_df    = None
if "active_card"  not in st.session_state: st.session_state.active_card  = None

# ── HELPERS ──────────────────────────────────────────────────────────────────
def recommend(property_name, top_n=5):
    scores = list(enumerate(
        (0.5 * cosine_sim1 + 0.8 * cosine_sim2 + cosine_sim3)
        [location_df.index.get_loc(property_name)]
    ))
    top = sorted(scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
    return pd.DataFrame({
        "Property": location_df.index[[i[0] for i in top]].tolist(),
        "Score":    [round(i[1], 3) for i in top],
    })

# ── PAGE HEADER ──────────────────────────────────────────────────────────────
st.markdown(
    '<span class="pg-label pg-label-green">AI Similarity Engine</span>',
    unsafe_allow_html=True,
)
st.markdown("""
<h1 style="margin:12px 0 8px">
    Smart Property <span class="gradient-text">Recommender</span>
</h1>
<p style="color:#94a3b8;margin:0 0 20px;font-size:0.98rem;max-width:560px">
    Find properties near your target location and discover similar
    listings using cosine similarity scoring.
</p>
""", unsafe_allow_html=True)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)


# ── SEARCH FORM ──────────────────────────────────────────────────────────────
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("""
<div style="font-family:'Syne',sans-serif;font-size:0.72rem;color:#7c8db5;
     text-transform:uppercase;letter-spacing:0.12em;font-weight:600;margin-bottom:15px">
    Search Parameters
</div>""", unsafe_allow_html=True)

sc1, sc2, sc3 = st.columns([3, 2, 1], gap="medium")
with sc1:
    select_location = st.selectbox("📍 Target Location",
                                   sorted(location_df.columns.tolist()))
with sc2:
    radius = st.slider("📏 Search Radius (km)", 1, 50, 5)
with sc3:
    st.markdown("<br>" , unsafe_allow_html=True)
    search_clicked = st.button("🔍 Search", use_container_width=True)
st.markdown("""
    <div style="margin-bottom:30px"></div>""", unsafe_allow_html=True)

# ── SEARCH LOGIC ─────────────────────────────────────────────────────────────
if search_clicked:
    result_ser = location_df[
        location_df[select_location] < radius * 1000
    ][select_location].sort_values()

    if len(result_ser) == 0:
        st.markdown("""
        <div class="card" style="text-align:center;padding:40px">
            <div style="font-size:2rem;margin-bottom:12px">🔍</div>
            <div style="color:#eef2ff;font-size:1rem;font-weight:600">No properties found</div>
            <div class="muted">Try increasing the search radius</div>
        </div>""", unsafe_allow_html=True)
        st.session_state.result_df   = None
    else:
        rdf = result_ser.reset_index()
        rdf.columns = ["Property", "Distance"]
        rdf["Distance"] = (rdf["Distance"] / 1000).round(2)
        st.session_state.result_df   = rdf
        st.session_state.active_card = None

# ── RESULTS ──────────────────────────────────────────────────────────────────
if st.session_state.result_df is not None:
    rdf = st.session_state.result_df

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:20px">
        <div style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:700;color:#eef2ff">
            Nearby Properties
        </div>
        <span class="tag tag-gold">{len(rdf)} found</span>
        <span class="muted">within {radius} km of {select_location}</span>
    </div>""", unsafe_allow_html=True)

    col_a, col_b = st.columns(2, gap="medium")

    for i, row in rdf.iterrows():
        prop_name = row["Property"]
        distance  = row["Distance"]
        is_active = st.session_state.active_card == prop_name
        border    = "rgba(212,168,67,0.4)" if is_active else "rgba(255,255,255,0.06)"

        with (col_a if i % 2 == 0 else col_b):
            st.markdown(f"""
            <div class="card-sm" style="border-color:{border};margin-bottom:10px">
                <div style="display:flex;justify-content:space-between;align-items:center">
                    <div>
                        <div style="font-size:0.95rem;font-weight:600;color:#eef2ff">
                            🏠 {prop_name}
                        </div>
                        <div style="font-size:0.78rem;color:#38bdf8;margin-top:3px">
                            📏 {distance} km away
                        </div>
                    </div>
                    <span class="tag {'tag-gold' if is_active else 'tag-cyan'}">
                        {'Active' if is_active else 'Nearby'}
                    </span>
                </div>
            </div>""", unsafe_allow_html=True)

            btn_label = "▲ Hide Similar" if is_active else "✨ Show Similar"
            if st.button(btn_label, key=f"btn_{i}", use_container_width=True):
                st.session_state.active_card = (
                    None if is_active else prop_name
                )
                st.rerun()

            if is_active:
                rec_df = recommend(prop_name)
                st.markdown("""
                <div style="margin-top:8px;margin-bottom:4px;font-size:0.72rem;color:#7c8db5;
                     text-transform:uppercase;letter-spacing:0.08em;font-weight:600">
                    Similar properties
                </div>""", unsafe_allow_html=True)
                for _, r in rec_df.iterrows():
                    pct = int(r["Score"] * 100)
                    st.markdown(f"""
                    <div style="background:#0c1220;border:1px solid rgba(255,255,255,0.06);
                         border-radius:10px;padding:10px 14px;margin-bottom:6px">
                        <div style="display:flex;justify-content:space-between;
                             align-items:center;margin-bottom:6px">
                            <span style="font-size:0.85rem;color:#eef2ff">🏠 {r['Property']}</span>
                            <span style="font-size:0.78rem;color:#d4a843;font-weight:600">
                                {r['Score']} match
                            </span>
                        </div>
                        <div style="height:4px;background:rgba(255,255,255,0.06);border-radius:3px">
                            <div style="height:100%;width:{pct}%;
                                 background:linear-gradient(90deg,#d4a843,#f5d38a);
                                 border-radius:3px"></div>
                        </div>
                    </div>""", unsafe_allow_html=True)