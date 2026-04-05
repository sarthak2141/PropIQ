import streamlit as st
import pandas as pd
import pickle
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from Utils.Styles import inject_css, inject_animated_bg, PLOTLY_THEME

st.set_page_config(
    page_title="PropIQ · Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_css()
inject_animated_bg()

# ── Load ──────────────────────────────────────────────────────────────────────
@st.cache_data
def load():
    df       = pd.read_csv("Models/data_viz1.csv")
    features = pickle.load(open("Models/All_feature_text.pkl", "rb"))
    sectors  = pickle.load(open("Models/sector_feature.pkl",   "rb"))
    return df, features, sectors

new_df, All_feature, sectors = load()

def safe_sort(s):
    try:    return int(s.strip().split()[-1])
    except: return 9999

# ── Sidebar filters ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="section-label" style="margin-top:18px">Filters</div>',
                unsafe_allow_html=True)
    prop_filter = st.multiselect(
        "Property type",
        options=new_df["property_type"].unique().tolist(),
        default=new_df["property_type"].unique().tolist(),
    )
    p_min = float(new_df["price"].min())
    p_max = float(new_df["price"].max())
    price_range = st.slider("Price range (Cr ₹)", p_min, p_max, (p_min, p_max))
    s_opts = sorted(new_df["sector"].unique().tolist(), key=safe_sort)
    sector_filter = st.multiselect("Sector", options=s_opts, default=s_opts)

if not prop_filter:  prop_filter  = new_df["property_type"].unique().tolist()
if not sector_filter: sector_filter = new_df["sector"].unique().tolist()

filtered = new_df[
    new_df["property_type"].isin(prop_filter) &
    new_df["sector"].isin(sector_filter) &
    new_df["price"].between(price_range[0], price_range[1])
].copy()

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<span class="pg-label pg-label-cyan">Market Intelligence</span>',
            unsafe_allow_html=True)
st.markdown("""
<h1 style="margin:12px 0 8px">
    Analytics <span class="gradient-text">Dashboard</span>
</h1>
<p style="color:#94a3b8;margin:0 0 20px;font-size:0.98rem">
    Real-time market intelligence. Use the sidebar to filter by type, price and sector.
</p>
""", unsafe_allow_html=True)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

if len(filtered) == 0:
    st.warning("No properties match the current filters. Try widening your selection.")
    st.stop()

# ── KPI strip ─────────────────────────────────────────────────────────────────
top_sec = filtered.groupby("sector")["price"].mean().idxmax()
kpis = [
    ("Avg price",   f"₹{filtered['price'].mean():.2f} Cr",        "#818cf8"),
    ("Avg ₹/sqft",  f"₹{filtered['price_per_sqft'].mean():,.0f}", "#67e8f9"),
    ("Properties",  f"{filtered.shape[0]:,}",                      "#6ee7b7"),
    ("Sectors",     f"{filtered['sector'].nunique()}",              "#fde68a"),
    ("Top sector",  top_sec,                                        "#818cf8"),
]
cols5 = st.columns(5, gap="small")
for col, (lbl, val, clr) in zip(cols5, kpis):
    col.markdown(f"""
    <div class="kpi-block">
        <div style="font-size:0.80rem;color:#FFFFFF;text-transform:uppercase;
             letter-spacing:0.09em;margin-bottom:5px">{lbl}</div>
        <div style="font-family:'Outfit',sans-serif;font-size:1.15rem;
             font-weight:700;color:{clr};line-height:1.2">{val}</div>
    </div>
    """, unsafe_allow_html=True)

# st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab"] {
        font-size: 30px;
        font-weight: 800;
        color:"#FFFFFF" 
    }
    </style>
""", unsafe_allow_html=True)
# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "📍  Map & Sectors",
    "📈  Price Analysis",
    "🧾  BHK & Features",
])

# ══════════ TAB 1 ══════════
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)

    if "latitude" in filtered.columns and "longitude" in filtered.columns:
        grp = filtered.groupby("sector")[
            ["price_per_sqft","built_up_area","latitude","longitude"]
        ].mean().dropna()
        if len(grp) > 0:
            fig_map = px.scatter_mapbox(
                grp, lat="latitude", lon="longitude",
                color="price_per_sqft", size="built_up_area",
                color_continuous_scale=[[0,"#0f172a"],[0.5,"#6366f1"],[1,"#f87171"]],
                zoom=10, mapbox_style="carto-positron",
                hover_name=grp.index, height=460,
                labels={"price_per_sqft":"₹/sqft"},
            )
            fig_map.update_layout(**{**PLOTLY_THEME,
                "title":"Price-per-sqft hotspots by sector",
                "margin":dict(l=0,r=0,t=40,b=0)})
            st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.info("Map not available — latitude/longitude columns not found in dataset.")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Top 10 sectors by average price</div>',
                unsafe_allow_html=True)

    bl, br = st.columns(2, gap="large")
    for col, ptype, scale, title in [
        (bl, "flat",  [[0,"#0f172a"],[1,"#818cf8"]], "Flats"),
        (br, "house", [[0,"#0f172a"],[1,"#67e8f9"]], "Houses"),
    ]:
        with col:
            sub = filtered[filtered["property_type"] == ptype]
            if len(sub) == 0:
                st.caption(f"No {ptype} data for current filters.")
                continue
            top = (sub.groupby("sector")["price"].mean()
                   .sort_values(ascending=False).head(10).reset_index())
            fig = px.bar(top, x="price", y="sector", orientation="h",
                         color="price", color_continuous_scale=scale,
                         labels={"price":"Avg Price (Cr ₹)","sector":""},
                         title=title)
            fig.update_layout(**{**PLOTLY_THEME, "height":340,
                "showlegend":False, "coloraxis_showscale":False,
                "yaxis":{**PLOTLY_THEME["yaxis"],"autorange":"reversed"}})
            st.plotly_chart(fig, use_container_width=True)
st.markdown('<div style="margin-bottom:40px;"></div>', unsafe_allow_html=True)  # extra spacing
# ══════════ TAB 2 ══════════
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)

    fig_sc = px.scatter(
        filtered, x="built_up_area", y="price", color="bedRoom",
        trendline="ols", opacity=0.65,
        color_continuous_scale=[[0,"#1e3a6e"],[0.5,"#6366f1"],[1,"#f87171"]],
        labels={"built_up_area":"Built-up area (sqft)",
                "price":"Price (Cr ₹)","bedRoom":"BHK"},
        title="Area vs Price — coloured by BHK",
    )
    fig_sc.update_traces(marker=dict(size=8), selector=dict(mode="markers"))
    fig_sc.update_traces(line=dict(color="#818cf8",width=2),
                         selector=dict(mode="lines"))
    fig_sc.update_layout(**{**PLOTLY_THEME,"height":380})
    st.plotly_chart(fig_sc, use_container_width=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    lc, rc = st.columns(2, gap="large")

    with lc:
        fig_v = px.violin(filtered, x="property_type", y="price",
                          color="property_type", box=True,
                          color_discrete_map={"flat":"#818cf8","house":"#67e8f9"},
                          labels={"price":"Price (Cr ₹)","property_type":""},
                          title="Price distribution by property type")
        fig_v.update_layout(**{**PLOTLY_THEME,"height":360,"showlegend":False})
        st.plotly_chart(fig_v, use_container_width=True)

    with rc:
        b4 = filtered[filtered["bedRoom"] <= 4]
        if len(b4) > 0:
            fig_b = px.box(b4, x="bedRoom", y="price", color="bedRoom",
                           color_discrete_sequence=["#818cf8","#67e8f9",
                                                    "#6ee7b7","#f87171"],
                           labels={"price":"Price (Cr ₹)","bedRoom":"Bedrooms"},
                           title="Price range by BHK configuration")
            fig_b.update_layout(**{**PLOTLY_THEME,"height":360,"showlegend":False})
            st.plotly_chart(fig_b, use_container_width=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    pivot = filtered.pivot_table(
        values="price", index="sector", columns="bedRoom", aggfunc="mean")
    if pivot.shape[0] > 1:
        fig_h = px.imshow(
            pivot, aspect="auto",
            color_continuous_scale=[
                [0.0, "#1e3a8a"],
                [0.25, "#2563eb"],
                [0.5, "#06b6d4"],
                [0.75, "#f59e0b"],
                [1.0, "#ef4444"]
            ],
            labels={"color":"Avg Price (Cr ₹)"},
            title="Sector × BHK average price heatmap")
        fig_h.update_layout(**{**PLOTLY_THEME,"height":520})
        st.plotly_chart(fig_h, use_container_width=True)

# ══════════ TAB 3 ══════════
with tab3:
    st.markdown("<br>", unsafe_allow_html=True)
    pc, wc_col = st.columns(2, gap="large")

    with pc:
        st.markdown('<div class="section-label">BHK distribution</div>',
                    unsafe_allow_html=True)
        s_opts2 = ["Overall"] + sorted(sectors.keys(), key=safe_sort)
        sel_sec = st.selectbox("Select sector", s_opts2)
        pie_df  = (filtered if sel_sec == "Overall"
                   else filtered[filtered["sector"] == sel_sec])
        if len(pie_df) == 0:
            st.caption("No data for this sector.")
        else:
            fig_p = px.pie(pie_df, names="bedRoom", hole=0.45,
                           color_discrete_sequence=[
                               "#818cf8","#67e8f9","#6ee7b7","#f87171","#fde68a"],title="Sectors x BHK Pie Chart ")
            fig_p.update_layout(**{**PLOTLY_THEME,"height":260})
            fig_p.update_traces(textfont_color="#e2e8f0")
            st.plotly_chart(fig_p, use_container_width=True)

    with wc_col:
        st.markdown('<div class="section-label">Amenities word cloud</div>',
                    unsafe_allow_html=True)
        wc_opts = ["Overall"] + sorted(sectors.keys(), key=safe_sort)
        sel_wc  = st.selectbox("Select sector for features", wc_opts)
        text    = (All_feature if sel_wc == "Overall"
                   else sectors.get(sel_wc, ""))
        if not text:
            st.caption("No feature data for this sector.")
        else:
            wc = WordCloud(
                width=680, height=360,
                background_color=None, mode="RGBA",
                colormap="cool", max_words=80,
            ).generate(text)
            fig_wc, ax = plt.subplots(figsize=(6.8, 3.6))
            fig_wc.patch.set_alpha(0)
            ax.imshow(wc, interpolation="bilinear")
            ax.axis("off")
            st.pyplot(fig_wc)
            plt.close(fig_wc)