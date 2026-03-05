# =============================================================================
# MAIZE YIELD PREDICTION DASHBOARD — REDESIGNED
# Uasin Gishu County, Kenya — KCA Tech Expo | March 2026
# Brian Okinda — Team Lead & Data Analyst
# IBM SkillsBuild Data Analytics Bootcamp
# =============================================================================
# Run with:
#   streamlit run dashboard.py
# =============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import joblib
import os

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="Maize Yield Prediction — Uasin Gishu",
    page_icon="🌽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# REDESIGNED STYLING — Dark Soil Theme
# Palette: Soil brown backgrounds · Gold accents · Green for good · Red for bad
# =============================================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

    /* ── GLOBAL ── */
    .stApp {
        background-color: #1C0A00 !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    /* Grain texture overlay */
    .stApp::before {
        content: '';
        position: fixed;
        inset: 0;
        background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.03'/%3E%3C/svg%3E");
        pointer-events: none;
        z-index: 0;
    }

    /* ── SIDEBAR ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0D0500 0%, #150800 100%) !important;
        border-right: 1px solid rgba(212,168,83,0.15) !important;
    }
    section[data-testid="stSidebar"] * {
        color: rgba(255,255,255,0.85) !important;
        font-family: 'DM Sans', sans-serif !important;
    }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #D4A853 !important;
    }
    section[data-testid="stSidebar"] .stSlider label {
        color: rgba(255,255,255,0.7) !important;
        font-size: 0.82rem !important;
        font-weight: 500 !important;
    }
    /* Slider track */
    section[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] div[role="slider"] {
        background-color: #D4A853 !important;
        border-color: #D4A853 !important;
    }

    /* ── MAIN CONTENT AREA ── */
    .main .block-container {
        background-color: transparent !important;
        padding: 1.5rem 2rem !important;
    }

    /* ── HEADINGS ── */
    h1 {
        font-family: 'Playfair Display', Georgia, serif !important;
        color: #F0E0C0 !important;
        font-weight: 900 !important;
        letter-spacing: -0.5px !important;
    }
    h2 {
        font-family: 'Playfair Display', Georgia, serif !important;
        color: #D4A853 !important;
        font-weight: 700 !important;
    }
    h3 {
        color: #D9C4A0 !important;
        font-weight: 600 !important;
    }
    p, li, div {
        color: #C8B89A;
    }

    /* ── METRIC CARDS ── */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #2D1200, #1C0A00) !important;
        border: 1px solid rgba(212,168,83,0.2) !important;
        border-radius: 10px !important;
        padding: 18px !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4) !important;
    }
    div[data-testid="metric-container"] label {
        color: #A89070 !important;
        font-size: 0.72rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1.2px !important;
        font-family: 'DM Mono', monospace !important;
    }
    div[data-testid="metric-container"] [data-testid="metric-value"] {
        color: #D4A853 !important;
        font-family: 'Playfair Display', serif !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }
    div[data-testid="metric-container"] [data-testid="metric-delta"] {
        color: #A89070 !important;
        font-size: 0.75rem !important;
    }

    /* ── TABS ── */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #0D0500 !important;
        border-radius: 8px 8px 0 0 !important;
        padding: 4px 4px 0 !important;
        gap: 2px !important;
        border-bottom: 1px solid rgba(212,168,83,0.15) !important;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        color: rgba(255,255,255,0.45) !important;
        border-radius: 6px 6px 0 0 !important;
        font-weight: 600 !important;
        font-size: 0.82rem !important;
        letter-spacing: 0.3px !important;
        padding: 10px 20px !important;
        font-family: 'DM Sans', sans-serif !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2D1200 !important;
        color: #D4A853 !important;
        border-top: 2px solid #D4A853 !important;
    }
    .stTabs [data-baseweb="tab-panel"] {
        background-color: #1C0A00 !important;
        border: 1px solid rgba(212,168,83,0.1) !important;
        border-top: none !important;
        border-radius: 0 0 10px 10px !important;
        padding: 20px !important;
    }

    /* ── BUTTONS ── */
    .stButton button {
        background: linear-gradient(135deg, #D4A853, #B8913A) !important;
        color: #0D0500 !important;
        font-weight: 700 !important;
        font-size: 0.85rem !important;
        letter-spacing: 0.5px !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        text-transform: uppercase !important;
        font-family: 'DM Sans', sans-serif !important;
        transition: all 0.2s !important;
        box-shadow: 0 4px 12px rgba(212,168,83,0.25) !important;
    }
    .stButton button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(212,168,83,0.35) !important;
    }

    /* ── SELECTBOX ── */
    .stSelectbox [data-baseweb="select"] {
        background-color: #2D1200 !important;
        border-color: rgba(212,168,83,0.25) !important;
        color: rgba(255,255,255,0.85) !important;
        border-radius: 8px !important;
    }
    .stSelectbox label {
        color: rgba(255,255,255,0.65) !important;
        font-size: 0.82rem !important;
    }

    /* ── DATAFRAME ── */
    .stDataFrame {
        border: 1px solid rgba(212,168,83,0.15) !important;
        border-radius: 8px !important;
        overflow: hidden !important;
    }
    .stDataFrame [data-testid="stDataFrameResizable"] {
        background-color: #2D1200 !important;
    }

    /* ── DIVIDER ── */
    hr {
        border-color: rgba(212,168,83,0.15) !important;
        margin: 1.5rem 0 !important;
    }

    /* ── CUSTOM COMPONENTS ── */

    /* Prediction result box */
    .prediction-box {
        background: linear-gradient(160deg, #0D2118, #0A1A10);
        border: 1px solid rgba(107,191,123,0.35);
        border-radius: 14px;
        padding: 32px;
        text-align: center;
        margin: 8px 0 16px;
        position: relative;
        overflow: hidden;
    }
    .prediction-box::before {
        content: '';
        position: absolute;
        top: -60px; left: 50%;
        transform: translateX(-50%);
        width: 220px; height: 220px;
        background: radial-gradient(circle, rgba(107,191,123,0.08) 0%, transparent 70%);
        pointer-events: none;
    }
    .prediction-box .pred-eyebrow {
        font-family: 'DM Mono', monospace;
        font-size: 0.65rem;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: rgba(107,191,123,0.7);
        margin-bottom: 10px;
    }
    .prediction-box h1 {
        color: white !important;
        font-size: 4rem !important;
        font-family: 'Playfair Display', serif !important;
        margin: 0 !important;
        line-height: 1 !important;
    }
    .prediction-box .pred-unit {
        color: #6BBF7B;
        font-size: 1.1rem;
        margin-top: 4px;
    }
    .prediction-box .pred-range {
        font-family: 'DM Mono', monospace;
        font-size: 0.75rem;
        color: rgba(255,255,255,0.35);
        margin: 8px 0 12px;
    }
    .prediction-box .pred-models {
        font-size: 0.75rem;
        color: rgba(255,255,255,0.3);
        margin-top: 8px;
    }
    .pred-verdict {
        display: inline-block;
        padding: 6px 20px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 0.3px;
        margin-top: 4px;
    }
    .pred-verdict.above {
        background: rgba(107,191,123,0.15);
        border: 1px solid rgba(107,191,123,0.35);
        color: #6BBF7B;
    }
    .pred-verdict.below {
        background: rgba(224,82,82,0.12);
        border: 1px solid rgba(224,82,82,0.3);
        color: #E05252;
    }
    .pred-verdict.average {
        background: rgba(212,168,83,0.12);
        border: 1px solid rgba(212,168,83,0.3);
        color: #D4A853;
    }

    /* Info / warning boxes */
    .info-box {
        background: rgba(74,124,89,0.12);
        border-left: 3px solid #4A7C59;
        border-radius: 0 8px 8px 0;
        padding: 12px 16px;
        margin: 8px 0;
        font-size: 0.85rem;
        color: #C8B89A;
        line-height: 1.65;
    }
    .info-box b { color: #E8D5B0; }

    .warn-box {
        background: rgba(212,168,83,0.08);
        border-left: 3px solid #D4A853;
        border-radius: 0 8px 8px 0;
        padding: 12px 16px;
        margin: 8px 0;
        font-size: 0.85rem;
        color: #C8B89A;
        line-height: 1.65;
    }
    .warn-box b { color: #D4A853; }

    /* Gap callout */
    .gap-callout {
        background: linear-gradient(135deg, #1a3a28, #0D1F14);
        border: 1px solid rgba(212,168,83,0.2);
        border-top: 3px solid #D4A853;
        border-radius: 0 0 12px 12px;
        padding: 22px 26px;
        margin: 0 0 20px;
        color: rgba(255,255,255,0.8);
    }
    .gap-callout h4 {
        font-family: 'Playfair Display', serif;
        color: #D4A853 !important;
        font-size: 1rem !important;
        margin: 0 0 10px !important;
        letter-spacing: 0.3px;
    }
    .gap-callout p {
        font-size: 0.88rem;
        line-height: 1.7;
        color: #C8B89A;
        margin: 0;
    }
    .gap-callout .gap-number {
        font-family: 'Playfair Display', serif;
        font-size: 1.6rem;
        font-weight: 700;
        color: #D4A853;
        line-height: 1;
    }
    .gap-callout .gap-number.green { color: #6BBF7B; }

    /* Onboarding banner */
    .onboard-box {
        background: rgba(212,168,83,0.06);
        border: 1px solid rgba(212,168,83,0.18);
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 20px;
        font-size: 0.88rem;
        color: #C8B89A;
        line-height: 1.7;
    }
    .onboard-box b { color: #D4A853; }

    /* Sidebar hint text */
    .slider-hint {
        font-size: 0.72rem;
        color: rgba(212,168,83,0.55);
        margin: -6px 0 10px;
        font-style: italic;
        font-family: 'DM Mono', monospace;
    }

    /* Sidebar prediction live box */
    .sidebar-pred {
        background: rgba(107,191,123,0.07);
        border: 1px solid rgba(107,191,123,0.2);
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        margin-top: 16px;
    }
    .sidebar-pred .sp-label {
        font-family: 'DM Mono', monospace;
        font-size: 0.62rem;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        color: rgba(107,191,123,0.65);
        margin-bottom: 6px;
    }
    .sidebar-pred .sp-value {
        font-family: 'Playfair Display', serif;
        font-size: 2.4rem;
        font-weight: 900;
        color: white;
        line-height: 1;
    }
    .sidebar-pred .sp-unit {
        font-size: 0.78rem;
        color: rgba(107,191,123,0.65);
        margin-top: 3px;
    }

    /* Hero header area */
    .hero-header {
        background: linear-gradient(160deg, #0D0500 0%, #1C0A00 50%, #1a3a28 100%);
        border-bottom: 1px solid rgba(212,168,83,0.15);
        padding: 8px 0 16px;
        margin-bottom: 4px;
    }

    /* Finding banner */
    .finding-banner {
        background: rgba(212,168,83,0.06);
        border: 1px solid rgba(212,168,83,0.2);
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 20px;
        font-size: 0.85rem;
        color: rgba(255,255,255,0.65);
        line-height: 1.65;
        display: flex;
        gap: 12px;
        align-items: flex-start;
    }
    .finding-banner .fb-badge {
        background: #D4A853;
        color: #0D0500;
        font-weight: 800;
        font-size: 0.65rem;
        letter-spacing: 1px;
        text-transform: uppercase;
        padding: 4px 8px;
        border-radius: 4px;
        white-space: nowrap;
        font-family: 'DM Mono', monospace;
        margin-top: 2px;
    }

    /* Reliability table */
    .rel-table { width: 100%; border-collapse: collapse; font-size: 0.82rem; }
    .rel-table th {
        background: #2D1200;
        color: #D4A853;
        padding: 8px 12px;
        text-align: left;
        font-family: 'DM Mono', monospace;
        font-size: 0.7rem;
        letter-spacing: 1px;
        text-transform: uppercase;
        border-bottom: 1px solid rgba(212,168,83,0.2);
    }
    .rel-table td {
        padding: 8px 12px;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        color: rgba(255,255,255,0.7);
        vertical-align: top;
    }
    .rel-table tr:nth-child(even) td { background: rgba(255,255,255,0.02); }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 4px; height: 4px; }
    ::-webkit-scrollbar-track { background: #0D0500; }
    ::-webkit-scrollbar-thumb { background: rgba(212,168,83,0.3); border-radius: 2px; }

</style>
""", unsafe_allow_html=True)

# =============================================================================
# LOAD DATA AND MODELS
# =============================================================================

BASE = os.path.dirname(os.path.abspath(__file__))

@st.cache_resource
def load_models():
    rf     = joblib.load(os.path.join(BASE, "rf_model_final.pkl"))
    svr    = joblib.load(os.path.join(BASE, "svr_model_final.pkl"))
    scaler = joblib.load(os.path.join(BASE, "scaler_final.pkl"))
    return rf, svr, scaler

@st.cache_data
def load_data():
    return pd.read_csv(os.path.join(BASE, "master_merged_final.csv"))

rf_model, svr_model, scaler = load_models()
master = load_data()

MODEL_FEATURES = [
    'Rain_LongRains_Fraction',
    'Humidity_ShortRains_pct',
    'Rain_DrySeason_mm',
    'Temp_ShortRains_C',
    'SoilWetness_ShortRains',
    'Rain_OffSeason_mm',
]

LOO_RMSE      = 0.3640
COUNTY_MEAN   = master['Yield_Tonnes_Ha'].mean()
COUNTY_MAX    = master['Yield_Tonnes_Ha'].max()
COUNTY_MIN    = master['Yield_Tonnes_Ha'].min()
SEED_POTENTIAL = 9.5

# Colour palette — used in all Plotly charts
P = {
    'gold':        '#D4A853',
    'gold_light':  '#F0C97A',
    'green':       '#6BBF7B',
    'green_dark':  '#4A7C59',
    'red':         '#E05252',
    'blue':        '#5B9BD5',
    'orange':      '#E8944A',
    'grey':        'rgba(255,255,255,0.25)',
    'bg':          '#1C0A00',
    'card':        '#2D1200',
    'grid':        'rgba(255,255,255,0.04)',
    'text':        'rgba(255,255,255,0.75)',
}

PLOTLY_LAYOUT = dict(
    plot_bgcolor  = P['card'],
    paper_bgcolor = '#1C0A00',
    font          = dict(family="DM Sans, sans-serif", color='#C8B89A'),
    margin        = dict(t=60, b=40, l=10, r=10),
    xaxis         = dict(gridcolor=P['grid'], linecolor='rgba(200,184,154,0.15)',
                         tickfont=dict(size=10, color='#A89070')),
    yaxis         = dict(gridcolor=P['grid'], linecolor='rgba(200,184,154,0.15)',
                         tickfont=dict(size=10, color='#A89070')),
    legend        = dict(bgcolor='rgba(0,0,0,0)', font=dict(size=10, color='#C8B89A')),
    hoverlabel    = dict(bgcolor='#0D0500', bordercolor=P['gold'],
                         font=dict(size=11, color='#E8D5B0')),
)

# High-contrast layout for Data Exploration charts
# Deep slate background makes gridlines, labels and data points clearly visible
EXPLORE_LAYOUT = dict(
    plot_bgcolor  = '#0F1923',
    paper_bgcolor = '#111D27',
    font          = dict(family="DM Sans, sans-serif", color='rgba(255,255,255,0.88)'),
    margin        = dict(t=70, b=50, l=10, r=10),
    xaxis         = dict(
        gridcolor     = 'rgba(255,255,255,0.12)',
        linecolor     = 'rgba(255,255,255,0.3)',
        zerolinecolor = 'rgba(255,255,255,0.3)',
        tickfont      = dict(size=11, color='rgba(255,255,255,0.8)'),
    ),
    yaxis         = dict(
        gridcolor     = 'rgba(255,255,255,0.12)',
        linecolor     = 'rgba(255,255,255,0.3)',
        zerolinecolor = 'rgba(255,255,255,0.3)',
        tickfont      = dict(size=11, color='rgba(255,255,255,0.8)'),
    ),
    legend        = dict(
        bgcolor     = 'rgba(255,255,255,0.05)',
        bordercolor = 'rgba(255,255,255,0.12)',
        borderwidth = 1,
        font        = dict(size=11, color='rgba(255,255,255,0.85)'),
    ),
    hoverlabel    = dict(
        bgcolor     = '#0A1520',
        bordercolor = '#D4A853',
        font        = dict(size=12, color='white'),
    ),
)

# =============================================================================
# PREDICTION HELPER
# =============================================================================

def make_prediction(rain_lr, rain_sr, rain_off, rain_dry,
                    temp_sr, humid_sr, wetness_sr):
    rain_annual = rain_lr + rain_sr + rain_off + rain_dry
    lr_fraction = rain_lr / rain_annual if rain_annual > 0 else 0.0

    row = pd.DataFrame([{
        'Rain_LongRains_Fraction': lr_fraction,
        'Humidity_ShortRains_pct': humid_sr,
        'Rain_DrySeason_mm':       rain_dry,
        'Temp_ShortRains_C':       temp_sr,
        'SoilWetness_ShortRains':  wetness_sr,
        'Rain_OffSeason_mm':       rain_off,
    }])[MODEL_FEATURES]

    scaled   = scaler.transform(row)
    rf_pred  = float(rf_model.predict(scaled)[0])
    svr_pred = float(svr_model.predict(scaled)[0])
    avg_pred = (rf_pred + svr_pred) / 2

    return {
        'rf':          round(rf_pred,  3),
        'svr':         round(svr_pred, 3),
        'avg':         round(avg_pred, 3),
        'low':         round(avg_pred - LOO_RMSE, 3),
        'high':        round(avg_pred + LOO_RMSE, 3),
        'lr_fraction': round(lr_fraction, 3),
        'annual_rain': round(rain_annual, 0),
    }

# =============================================================================
# SIDEBAR
# =============================================================================

with st.sidebar:
    st.markdown("## 🌽 Maize Yield Predictor")
    st.markdown("**Uasin Gishu County, Kenya**")
    st.markdown("---")

    st.markdown("""
    <div style="background:rgba(212,168,83,0.07);border:1px solid rgba(212,168,83,0.18);
    border-radius:8px;padding:12px 14px;font-size:0.78rem;
    color:rgba(255,255,255,0.55);line-height:1.7;margin-bottom:16px;">
    <b style="color:#D4A853;">How to use:</b><br>
    1. Adjust sliders to match your season's expected weather.<br>
    2. Your yield prediction updates live below.<br>
    3. Go to the <b>Yield Predictor</b> tab for full detail.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Rainfall by Season (mm)")

    rain_lr = st.slider("Long Rains — Mar to May", 100, 1200, 600, 10,
                        help="Main planting season — most critical window for maize growth.")
    st.markdown('<p class="slider-hint">Main planting season — most critical</p>',
                unsafe_allow_html=True)

    rain_sr = st.slider("Short Rains — Sep to Nov", 100, 900, 400, 10,
                        help="Pre-planting period. Shapes soil health going into the next Long Rains.")
    st.markdown('<p class="slider-hint">Pre-planting soil health period</p>',
                unsafe_allow_html=True)

    rain_off = st.slider("Off Season — Jun to Aug", 50, 600, 150, 10,
                         help="Normally dry. Unexpected rain causes disease and soil problems.")
    st.markdown('<p class="slider-hint">Unexpected rain causes problems</p>',
                unsafe_allow_html=True)

    rain_dry = st.slider("Dry Season — Dec to Feb", 20, 400, 80, 10,
                         help="Land preparation period. Excess rain damages soil structure.")
    st.markdown('<p class="slider-hint">Excess rain damages soil structure</p>',
                unsafe_allow_html=True)

    st.markdown("### Short Rains Conditions (Sep–Nov)")

    temp_sr = st.slider("Average Temperature (°C)", 17.0, 23.0, 20.0, 0.1,
                        help="Average temperature September–November.")
    st.markdown('<p class="slider-hint">Warmer = better soil recovery</p>',
                unsafe_allow_html=True)

    humid_sr = st.slider("Average Humidity (%)", 55.0, 85.0, 70.0, 0.5,
                         help="Above 75% signals disease and waterlogging risk.")
    st.markdown('<p class="slider-hint">Above 75% = elevated disease risk</p>',
                unsafe_allow_html=True)

    wetness_sr = st.slider("Soil Wetness (0–1)", 0.3, 0.9, 0.6, 0.01,
                           help="0 = dry · 0.5 = moist · 1 = waterlogged")
    st.markdown('<p class="slider-hint">0 = dry · 0.5 = moist · 1 = waterlogged</p>',
                unsafe_allow_html=True)

    st.markdown("---")

    # Live prediction display in sidebar
    prediction = make_prediction(rain_lr, rain_sr, rain_off, rain_dry,
                                 temp_sr, humid_sr, wetness_sr)

    pred_val  = prediction['avg']
    pred_low  = prediction['low']
    pred_high = prediction['high']

    if pred_val >= COUNTY_MEAN + 0.2:
        verdict_class = "above"
        verdict_text  = "✅ Above Average Season"
    elif pred_val <= COUNTY_MEAN - 0.2:
        verdict_class = "below"
        verdict_text  = "⚠ Below Average Season"
    else:
        verdict_class = "average"
        verdict_text  = "➡ Average Season"

    st.markdown(f"""
    <div class="sidebar-pred">
        <div class="sp-label">Live Yield Estimate</div>
        <div class="sp-value">{pred_val:.2f}</div>
        <div class="sp-unit">tonnes per hectare</div>
        <div style="font-family:'DM Mono',monospace;font-size:0.68rem;
                    color:rgba(255,255,255,0.3);margin:6px 0 10px;">
            Range: {pred_low:.2f} – {pred_high:.2f} t/ha
        </div>
        <span class="pred-verdict {verdict_class}">{verdict_text}</span>
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# HEADER
# =============================================================================

st.markdown("""
<div class="hero-header">
    <p style="font-family:'DM Mono',monospace;font-size:0.62rem;letter-spacing:3px;
              text-transform:uppercase;color:rgba(212,168,83,0.6);margin:0 0 6px;">
        IBM SkillsBuild · KCA Tech Expo · March 2026
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("# 🌽 Maize Yield Prediction Dashboard")
st.markdown("### Uasin Gishu County, Kenya &nbsp;|&nbsp; 2012–2023 &nbsp;|&nbsp; IBM SkillsBuild Data Analytics Bootcamp")

st.markdown("""
<div class="onboard-box">
<b>Welcome.</b> This dashboard uses 12 years of weather, soil, and harvest data from Uasin Gishu County
to estimate seasonal maize yield — measured in <b>tonnes per hectare (t/ha)</b>.<br>
<b>Use the sliders on the left</b> to enter your season's expected conditions.
The four tabs below cover: overall trends · data exploration · live prediction · model accuracy.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# =============================================================================
# TABS
# =============================================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "🌾  Overview",
    "📊  Data Exploration",
    "🎯  Yield Predictor",
    "📈  Model Accuracy",
])

# =============================================================================
# TAB 1 — OVERVIEW
# =============================================================================

with tab1:

    st.markdown("""
    <div class="gap-callout">
        <h4>⚠ THE MOST IMPORTANT FINDING — The Yield Gap is a Soil Problem, Not a Weather Problem</h4>
        <p>
        Farmers in Uasin Gishu harvest an average of
        <span class="gap-number">3.65 t/ha</span>
        — but the seeds they plant are capable of producing
        <span class="gap-number green">9–11 t/ha</span>.
        That is <b style="color:#D4A853;">~6.5 tonnes of lost potential every single season.</b><br><br>
        Weather improvements alone cannot close this gap. Even in 2018 — the best weather year on record —
        yield only reached 4.26 t/ha. The root cause is <b style="color:#D4A853;">soil acidity: pH 5.7</b>
        (optimal range for maize: 6.0–7.0). Agricultural lime at 1–2 t/ha is the single highest-impact
        intervention available.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # KPI cards
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("County Average Yield",   f"{COUNTY_MEAN:.2f} t/ha",  "2012–2023")
    c2.metric("Best Year on Record",    f"{COUNTY_MAX:.2f} t/ha",   "2018 — H6213 variety")
    c3.metric("Worst Year on Record",   f"{COUNTY_MIN:.2f} t/ha",   "2012 — MLN outbreak")
    c4.metric("Yield Gap vs Potential", "~6.5 t/ha",                "Seed potential: 9–11 t/ha")

    st.markdown("---")
    col_left, col_right = st.columns([2, 1])

    with col_left:
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=master['Year'], y=master['Yield_Tonnes_Ha'],
            mode='lines+markers',
            line=dict(color=P['gold'], width=2.8),
            marker=dict(
                size=9,
                color=[P['green'] if v >= COUNTY_MEAN else P['red']
                       for v in master['Yield_Tonnes_Ha']],
                line=dict(color='#1C0A00', width=2)
            ),
            fill='tozeroy',
            fillcolor='rgba(212,168,83,0.06)',
            name='Actual Yield',
            hovertemplate='<b>%{x}</b><br>Yield: %{y:.3f} t/ha<extra></extra>',
        ))

        fig.add_hline(y=COUNTY_MEAN, line_dash='dash',
                      line_color='rgba(255,255,255,0.2)', line_width=1.5,
                      annotation_text=f"County avg: {COUNTY_MEAN:.2f} t/ha",
                      annotation_font_color='rgba(255,255,255,0.4)',
                      annotation_position="bottom right")

        fig.add_hline(y=SEED_POTENTIAL, line_dash='dot',
                      line_color=P['orange'], line_width=2,
                      annotation_text="Seed potential: ~9.5 t/ha",
                      annotation_position="top right",
                      annotation_font_color=P['orange'])

        fig.add_hrect(y0=COUNTY_MEAN, y1=SEED_POTENTIAL,
                      fillcolor="rgba(232,148,74,0.05)", line_width=0,
                      annotation_text="Yield gap (~6.5 t/ha)",
                      annotation_position="top left",
                      annotation_font_color=P['orange'],
                      annotation_font_size=10)

        layout = {**PLOTLY_LAYOUT}
        layout['title'] = dict(
            text='Annual Maize Yield — Uasin Gishu County<br>'
                 '<sup style="color:rgba(255,255,255,0.4)">Gold dots = above average · Red dots = below average</sup>',
            font=dict(family="Playfair Display, serif", size=15, color='white')
        )
        layout['xaxis'] = dict(**PLOTLY_LAYOUT['xaxis'],
                                tickmode='array', tickvals=master['Year'].tolist())
        layout['yaxis'] = dict(**PLOTLY_LAYOUT['yaxis'], range=[0, 11.5],
                                title=dict(text='Yield (t/ha)', font=dict(size=10)))
        layout['height'] = 380
        fig.update_layout(**layout)
        st.plotly_chart(fig, use_container_width=True, config={"responsive": True})

    with col_right:
        st.markdown("### Key Findings")
        st.markdown("""
        <div class="info-box">
        <b>Rainfall timing beats total volume.</b><br>
        In 2020, a record 2,371mm fell — yet yield was only 3.07 t/ha.
        Only 34% arrived during planting season. Rain at the wrong time does not help.
        </div>

        <div class="info-box">
        <b>The harvest is decided before planting.</b><br>
        Humidity and soil moisture in September–November predict the following
        year's yield more strongly than planting-season conditions.
        </div>

        <div class="warn-box">
        <b>⚠ The gap is a soil problem.</b><br>
        Average 3.65 t/ha vs seed potential 9–11 t/ha. Soil acidity (pH 5.7)
        blocks nutrient uptake. Liming unlocks what better weather alone cannot.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Year-by-Year Summary")

    display_cols = ['Year', 'Yield_Tonnes_Ha', 'Rain_LongRains_mm',
                    'Rain_Annual_mm', 'Temp_LongRains_C', 'Variety', 'MLN_Risk']
    display_cols = [c for c in display_cols if c in master.columns]
    display_df   = master[display_cols].copy().rename(columns={
        'Yield_Tonnes_Ha':   'Yield (t/ha)',
        'Rain_LongRains_mm': 'Long Rains (mm)',
        'Rain_Annual_mm':    'Annual Rain (mm)',
        'Temp_LongRains_C':  'Temp Long Rains (°C)',
        'MLN_Risk':          'MLN Risk',
    })
    st.dataframe(
        display_df.style
            .format({'Yield (t/ha)': '{:.3f}', 'Long Rains (mm)': '{:.0f}',
                     'Annual Rain (mm)': '{:.0f}', 'Temp Long Rains (°C)': '{:.2f}'})
            .background_gradient(subset=['Yield (t/ha)'], cmap='YlGn'),
        use_container_width=True, hide_index=True,
    )

# =============================================================================
# TAB 2 — DATA EXPLORATION
# =============================================================================

with tab2:

    st.markdown("""
    <div class="info-box">
    <b>Data Exploration.</b> See how each weather variable relates to yield.
    Use the dropdown to build scatter plots for any variable.
    Go to the <b>Yield Predictor</b> tab if you want a prediction.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### How Each Variable Relates to Yield")
    st.markdown("""
    <div class="info-box">
    Correlation score: <b>+1</b> = when this rises yield rises ·
    <b>−1</b> = when this rises yield falls · <b>0</b> = no relationship.<br>
    Dashed lines mark the ±0.5 strong predictor threshold.
    </div>
    """, unsafe_allow_html=True)

    EXCLUDE = ['Year', 'Soil_pH', 'Nitrogen_g_kg', 'Fertilizer_Kg_Ha',
               'Yield_Tonnes_Ha', 'Yield_Potential_Min_tHa',
               'Yield_Potential_Max_tHa', 'Area_Planted_Ha',
               'Variety_Code', 'MLN_Risk']
    num_cols  = master.select_dtypes(include='number').columns.tolist()
    feat_cols = [c for c in num_cols if c not in EXCLUDE]
    corr      = master[feat_cols + ['Yield_Tonnes_Ha']].corr()['Yield_Tonnes_Ha'].drop('Yield_Tonnes_Ha')
    corr_df   = pd.DataFrame({'Feature': corr.index, 'Correlation': corr.values})
    corr_df   = corr_df.reindex(corr_df['Correlation'].abs().sort_values(ascending=True).index)

    # Brighter colours for high-contrast slate background
    colors = ['#52D68A' if v > 0 else '#FF6B6B' for v in corr_df['Correlation']]

    fig_corr = go.Figure(go.Bar(
        x=corr_df['Correlation'], y=corr_df['Feature'],
        orientation='h', marker_color=colors,
        marker_line_color='rgba(0,0,0,0)', marker_line_width=0,
        hovertemplate='<b>%{y}</b><br>r = %{x:.4f}<extra></extra>',
    ))
    fig_corr.add_vline(x=0,    line_color='rgba(255,255,255,0.5)',  line_width=1.5)
    fig_corr.add_vline(x=0.5,  line_color='#52D68A', line_width=1.5, line_dash='dash')
    fig_corr.add_vline(x=-0.5, line_color='#FF6B6B', line_width=1.5, line_dash='dash')

    layout_corr = {**EXPLORE_LAYOUT}
    layout_corr['title'] = dict(
        text='Variable Relationship with Yield<br>'
             '<sup style="color:rgba(255,255,255,0.5)">Green = higher value → better yield  ·  Red = higher value → lower yield  ·  Dashed lines = strong predictor threshold ±0.5</sup>',
        font=dict(family="Playfair Display, serif", size=15, color='white')
    )
    layout_corr['xaxis'] = dict(
        **EXPLORE_LAYOUT['xaxis'],
        range=[-1.05, 1.05],
        title=dict(text='Relationship strength (−1 to +1)', font=dict(size=11, color='rgba(255,255,255,0.75)')),
        tickvals=[-1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1],
    )
    layout_corr['yaxis'] = dict(
        **EXPLORE_LAYOUT['yaxis'],
        tickfont=dict(size=10, color='rgba(255,255,255,0.8)'),
    )
    layout_corr['height'] = 520
    layout_corr['margin'] = dict(t=80, b=50, l=240, r=20)
    fig_corr.update_layout(**layout_corr)
    st.plotly_chart(fig_corr, use_container_width=True, config={"responsive": True})

    st.markdown("---")
    st.markdown("### Explore Any Variable vs Yield")

    scatter_options = [c for c in feat_cols if c in master.columns]
    selected = st.selectbox(
        "Choose a weather variable:",
        scatter_options,
        index=scatter_options.index('Rain_LongRains_Fraction')
        if 'Rain_LongRains_Fraction' in scatter_options else 0
    )

    col_s1, col_s2 = st.columns([2, 1])
    with col_s1:
        r_val = master['Yield_Tonnes_Ha'].corr(master[selected])
        z     = np.polyfit(master[selected], master['Yield_Tonnes_Ha'], 1)
        x_min, x_max = master[selected].min(), master[selected].max()
        x_line = np.linspace(x_min, x_max, 100)

        fig_sc = go.Figure()
        # Trend line
        fig_sc.add_trace(go.Scatter(
            x=x_line, y=np.poly1d(z)(x_line),
            mode='lines',
            line=dict(color='rgba(255,255,255,0.35)', dash='dash', width=1.8),
            showlegend=False,
        ))
        # Colour each dot: gold = above avg yield, red = below avg yield
        dot_colors = ['#F0C97A' if y >= COUNTY_MEAN else '#FF6B6B'
                      for y in master['Yield_Tonnes_Ha']]
        fig_sc.add_trace(go.Scatter(
            x=master[selected], y=master['Yield_Tonnes_Ha'],
            mode='markers+text',
            marker=dict(
                size=13,
                color=dot_colors,
                line=dict(color='#0F1923', width=2),
                symbol='circle',
            ),
            text=master['Year'].astype(str),
            textposition='top right',
            textfont=dict(size=10, color='rgba(255,255,255,0.85)'),
            hovertemplate=f'<b>%{{text}}</b><br>{selected}: %{{x:.2f}}<br>Yield: %{{y:.3f}} t/ha<extra></extra>',
        ))
        layout_sc = {**EXPLORE_LAYOUT}
        layout_sc['title'] = dict(
            text=f'{selected} vs Yield  ·  r = {r_val:+.3f}<br>'
                 f'<sup style="color:rgba(255,255,255,0.5)">Gold dots = above county average · Red dots = below average</sup>',
            font=dict(family="Playfair Display, serif", size=14, color='white')
        )
        layout_sc['xaxis'] = dict(
            **EXPLORE_LAYOUT['xaxis'],
            title=dict(text=selected, font=dict(size=11, color='rgba(255,255,255,0.75)')),
        )
        layout_sc['yaxis'] = dict(
            **EXPLORE_LAYOUT['yaxis'],
            title=dict(text='Yield (t/ha)', font=dict(size=11, color='rgba(255,255,255,0.75)')),
        )
        layout_sc['height'] = 400
        fig_sc.update_layout(**layout_sc)
        st.plotly_chart(fig_sc, use_container_width=True, config={"responsive": True})

    with col_s2:
        st.markdown("#### What This Means")
        strength  = "Strong" if abs(r_val) > 0.5 else ("Moderate" if abs(r_val) > 0.3 else "Weak")
        direction = "positive" if r_val > 0 else "negative"
        plain     = ("When this variable is higher, yield tends to be higher."
                     if r_val > 0 else
                     "When this variable is higher, yield tends to be lower.")

        # High contrast info boxes for the slate-background explore tab
        st.markdown(f"""
        <div style="background:rgba(15,25,35,0.9);border:1px solid rgba(240,201,122,0.4);
                    border-left:4px solid #F0C97A;border-radius:0 8px 8px 0;
                    padding:14px 16px;margin:8px 0;font-size:0.85rem;
                    color:rgba(255,255,255,0.88);line-height:1.7;">
        <b style="color:#F0C97A;">r = {r_val:+.4f}</b><br>
        This is a <b>{strength.lower()} {direction}</b> relationship.<br><br>
        {plain}
        </div>
        """, unsafe_allow_html=True)

        if abs(r_val) < 0.3:
            st.markdown("""
            <div style="background:rgba(15,25,35,0.9);border:1px solid rgba(255,107,107,0.35);
                        border-left:4px solid #FF6B6B;border-radius:0 8px 8px 0;
                        padding:14px 16px;margin:8px 0;font-size:0.85rem;
                        color:rgba(255,255,255,0.8);line-height:1.65;">
            <b style="color:#FF6B6B;">Weak relationship</b> — not a strong standalone predictor.
            The model combines multiple weaker signals together to improve overall accuracy.
            </div>
            """, unsafe_allow_html=True)
        elif abs(r_val) >= 0.5:
            st.markdown("""
            <div style="background:rgba(15,25,35,0.9);border:1px solid rgba(82,214,138,0.35);
                        border-left:4px solid #52D68A;border-radius:0 8px 8px 0;
                        padding:14px 16px;margin:8px 0;font-size:0.85rem;
                        color:rgba(255,255,255,0.8);line-height:1.65;">
            <b style="color:#52D68A;">Strong predictor</b> — explains a meaningful share of
            year-to-year yield variation. Likely one of the 6 model inputs.
            </div>
            """, unsafe_allow_html=True)

# =============================================================================
# TAB 3 — YIELD PREDICTOR
# =============================================================================

with tab3:

    st.markdown("### Interactive Yield Predictor")
    st.markdown("""
    <div class="info-box">
    <b>How this works:</b> Adjust the sliders on the left to match your season's expected weather.
    The prediction updates live. Results are in <b>tonnes per hectare (t/ha)</b>.
    The uncertainty range of ±0.36 t/ha is derived from 12 years of honest out-of-sample testing.
    </div>
    """, unsafe_allow_html=True)

    col_p1, col_p2 = st.columns([1, 1])

    with col_p1:
        st.markdown(f"""
        <div class="prediction-box">
            <div class="pred-eyebrow">Predicted Maize Yield</div>
            <h1>{pred_val:.2f}</h1>
            <div class="pred-unit">tonnes per hectare</div>
            <div class="pred-range">Likely range: {pred_low:.2f} – {pred_high:.2f} t/ha</div>
            <span class="pred-verdict {verdict_class}">{verdict_text}</span>
            <div class="pred-models">
                Model A (Random Forest): {prediction['rf']:.2f} &nbsp;|&nbsp;
                Model B (SVR): {prediction['svr']:.2f}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Gauge
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=pred_val,
            delta={'reference': COUNTY_MEAN, 'valueformat': '.2f',
                   'suffix': ' vs avg', 'increasing': {'color': P['green']},
                   'decreasing': {'color': P['red']}},
            gauge={
                'axis': {'range': [2.0, 5.0], 'ticksuffix': ' t/ha',
                         'tickfont': {'size': 10, 'color': P['text']}},
                'bar': {'color': P['gold']},
                'bgcolor': P['card'],
                'bordercolor': 'rgba(255,255,255,0.05)',
                'steps': [
                    {'range': [2.0, 3.0], 'color': 'rgba(224,82,82,0.15)'},
                    {'range': [3.0, 3.5], 'color': 'rgba(232,148,74,0.12)'},
                    {'range': [3.5, 4.0], 'color': 'rgba(107,191,123,0.12)'},
                    {'range': [4.0, 5.0], 'color': 'rgba(107,191,123,0.2)'},
                ],
                'threshold': {'line': {'color': P['grey'], 'width': 2},
                              'thickness': 0.75, 'value': COUNTY_MEAN},
            },
            title={'text': 'Yield Gauge', 'font': {'size': 13, 'color': P['text']}},
            number={'suffix': ' t/ha', 'valueformat': '.2f',
                    'font': {'color': P['gold'], 'family': 'Playfair Display, serif', 'size': 28}},
        ))
        fig_gauge.update_layout(
            height=280, paper_bgcolor='#1C0A00',
            font=dict(color=P['text'], family='DM Sans, sans-serif'),
            margin=dict(t=40, b=10, l=10, r=10),
        )
        st.plotly_chart(fig_gauge, use_container_width=True, config={"responsive": True})

    with col_p2:
        st.markdown("#### Your Input Summary")

        rain_annual = rain_lr + rain_sr + rain_off + rain_dry
        lr_fraction = rain_lr / rain_annual if rain_annual > 0 else 0

        timing_color = P['green'] if lr_fraction > 0.35 else P['red']
        timing_label = ("✅ Good — enough rain in the planting window"
                        if lr_fraction > 0.35 else
                        "⚠ Poor — most rain fell outside planting season")

        # Donut chart
        fig_donut = go.Figure(go.Pie(
            labels=['Long Rains (Mar–May)', 'Short Rains (Sep–Nov)',
                    'Off Season (Jun–Aug)', 'Dry Season (Dec–Feb)'],
            values=[rain_lr, rain_sr, rain_off, rain_dry],
            hole=0.58,
            marker_colors=[P['gold'], P['green'], P['orange'], P['blue']],
            textinfo='label+percent',
            textfont_size=9,
            textfont_color='rgba(255,255,255,0.8)',
            hovertemplate='<b>%{label}</b><br>%{value:.0f} mm (%{percent})<extra></extra>',
        ))
        fig_donut.update_layout(
            title=dict(text=f'Rainfall Distribution — {rain_annual:.0f} mm total',
                       font=dict(size=12, color='white', family='Playfair Display, serif')),
            height=280, paper_bgcolor='#1C0A00',
            font=dict(color=P['text']),
            margin=dict(t=50, b=10, l=0, r=0),
            showlegend=False,
        )
        st.plotly_chart(fig_donut, use_container_width=True, config={"responsive": True})

        st.markdown(f"""
        <div class="info-box">
        <b>Planting-season rain share:</b> {lr_fraction:.1%}<br>
        <span style="color:{timing_color};font-weight:600;">{timing_label}</span><br>
        <span style="font-size:0.78rem;color:rgba(255,255,255,0.4);">
        Seasons with 40%+ in the planting window consistently produce above-average yields.
        </span>
        </div>
        <div class="info-box">
        <b>Total annual rainfall:</b> {rain_annual:.0f} mm<br>
        <span style="font-size:0.78rem;color:rgba(255,255,255,0.4);">
        Historical range: 1,142 – 2,371 mm
        </span>
        </div>
        <div class="warn-box">
        <b>Prediction uncertainty:</b> ±0.36 t/ha average error —
        tested against 12 years of real data using Leave-One-Out cross-validation.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Compare Scenarios Side by Side")
    st.markdown("""
    <div class="info-box">
    Set sliders to one scenario and click <b>Save Scenario</b>.
    Change sliders and save again. Compare results in the chart below.
    </div>
    """, unsafe_allow_html=True)

    if 'scenarios' not in st.session_state:
        st.session_state.scenarios = []

    col_btn1, col_btn2 = st.columns([1, 4])
    with col_btn1:
        if st.button("💾 Save Scenario"):
            st.session_state.scenarios.append({
                'Scenario':           f"Scenario {len(st.session_state.scenarios)+1}",
                'Long Rains (mm)':    rain_lr,
                'Annual Rain (mm)':   rain_annual,
                'LR Share':           f"{lr_fraction:.1%}",
                'Prediction (t/ha)':  pred_val,
                'Likely Range':       f"{pred_low:.2f} – {pred_high:.2f}",
            })
    with col_btn2:
        if st.button("🗑 Clear All"):
            st.session_state.scenarios = []

    if st.session_state.scenarios:
        sc_df = pd.DataFrame(st.session_state.scenarios)
        fig_sc_bar = go.Figure(go.Bar(
            x=sc_df['Scenario'],
            y=sc_df['Prediction (t/ha)'],
            marker_color=[P['green'] if v >= COUNTY_MEAN else P['red']
                          for v in sc_df['Prediction (t/ha)']],
            marker_line_color='rgba(0,0,0,0)',
            text=[f"{v:.2f} t/ha" for v in sc_df['Prediction (t/ha)']],
            textposition='outside',
            textfont=dict(color='white', size=11),
        ))
        fig_sc_bar.add_hline(y=COUNTY_MEAN, line_dash='dash',
                             line_color=P['grey'],
                             annotation_text=f"County avg: {COUNTY_MEAN:.2f}",
                             annotation_font_color=P['grey'])
        layout_sc_bar = {**PLOTLY_LAYOUT}
        layout_sc_bar['title'] = dict(
            text='Scenario Comparison',
            font=dict(family="Playfair Display, serif", size=14, color='white')
        )
        layout_sc_bar['yaxis'] = dict(**PLOTLY_LAYOUT['yaxis'],
                                       title=dict(text='Predicted Yield (t/ha)', font=dict(size=10)))
        layout_sc_bar['height'] = 320
        fig_sc_bar.update_layout(**layout_sc_bar)
        st.plotly_chart(fig_sc_bar, use_container_width=True, config={"responsive": True})
        st.dataframe(sc_df, use_container_width=True, hide_index=True)
    else:
        st.markdown("""
        <div class="warn-box">
        No scenarios saved yet. Adjust the sliders and click <b>💾 Save Scenario</b> to start comparing.
        </div>
        """, unsafe_allow_html=True)

# =============================================================================
# TAB 4 — MODEL ACCURACY
# =============================================================================

with tab4:

    st.markdown("### How Accurate Is the Model?")
    st.markdown("""
    <div class="info-box">
    <b>How was the model tested?</b> With only 12 years of data, standard train-test splits are
    unreliable. We used <b>Leave-One-Out Cross-Validation</b> — hold out one year, train on 11,
    predict the held-out year, repeat for all 12. Every figure below comes from this honest test.
    No metric is derived from data the model trained on.
    </div>
    """, unsafe_allow_html=True)

    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    col_m1.metric("Average Prediction Error", "0.364 t/ha", "Random Forest LOO RMSE")
    col_m2.metric("Variance Explained",        "30%",        "Weather explains ~30% of variation")
    col_m3.metric("Error vs County Average",   "10%",        "County mean = 3.65 t/ha")
    col_m4.metric("Model Bias",                "−0.007 t/ha","Essentially unbiased")

    st.markdown("---")
    col_v1, col_v2 = st.columns(2)

    LOO_PRED = np.array([3.550, 3.813, 3.756, 3.750, 3.891,
                          3.422, 3.530, 3.547, 3.451, 3.804,
                          3.495, 3.690])
    actual = master['Yield_Tonnes_Ha'].values
    years  = master['Year'].values

    with col_v1:
        lo = min(actual.min(), LOO_PRED.min()) - 0.25
        hi = max(actual.max(), LOO_PRED.max()) + 0.25

        fig_avp = go.Figure()
        fig_avp.add_trace(go.Scatter(
            x=[lo, hi], y=[lo, hi], mode='lines',
            line=dict(color=P['grey'], dash='dash', width=1.5),
            name='Perfect prediction',
        ))
        fig_avp.add_trace(go.Scatter(
            x=[lo, hi], y=[lo+LOO_RMSE, hi+LOO_RMSE],
            mode='lines', line=dict(width=0), showlegend=False, hoverinfo='skip',
        ))
        fig_avp.add_trace(go.Scatter(
            x=[lo, hi], y=[lo-LOO_RMSE, hi-LOO_RMSE],
            mode='lines', fill='tonexty',
            fillcolor='rgba(107,191,123,0.07)',
            line=dict(width=0),
            name=f'±{LOO_RMSE:.2f} t/ha error band',
        ))
        fig_avp.add_trace(go.Scatter(
            x=actual, y=LOO_PRED,
            mode='markers+text',
            marker=dict(size=12, color=P['gold'],
                        line=dict(color='#1C0A00', width=2)),
            text=[str(y) for y in years],
            textposition='top right',
            textfont=dict(size=9, color=P['text']),
            name='Predicted vs actual',
            hovertemplate='<b>%{text}</b><br>Actual: %{x:.3f}<br>Predicted: %{y:.3f}<extra></extra>',
        ))
        layout_avp = {**PLOTLY_LAYOUT}
        layout_avp['title'] = dict(
            text='Predicted vs Actual — All 12 Years<br>'
                 '<sup style="color:rgba(255,255,255,0.35)">Points on dashed line = perfect · Shaded band = acceptable error</sup>',
            font=dict(family="Playfair Display, serif", size=14, color='white')
        )
        layout_avp['xaxis'] = dict(**PLOTLY_LAYOUT['xaxis'],
                                    range=[lo,hi], title=dict(text='Actual Yield (t/ha)', font=dict(size=10)))
        layout_avp['yaxis'] = dict(**PLOTLY_LAYOUT['yaxis'],
                                    range=[lo,hi], title=dict(text='Model Prediction (t/ha)', font=dict(size=10)))
        layout_avp['height'] = 400
        fig_avp.update_layout(**layout_avp)
        st.plotly_chart(fig_avp, use_container_width=True, config={"responsive": True})

    with col_v2:
        residuals  = LOO_PRED - actual
        res_colors = [P['blue'] if r >= 0 else P['orange'] for r in residuals]

        fig_res = go.Figure(go.Bar(
            x=years, y=residuals,
            marker_color=res_colors,
            marker_line_color='rgba(0,0,0,0)',
            text=[f'{r:+.2f}' for r in residuals],
            textposition='outside',
            textfont=dict(color='rgba(255,255,255,0.6)', size=9),
            hovertemplate='<b>%{x}</b><br>Error: %{y:+.3f} t/ha<extra></extra>',
        ))
        fig_res.add_hline(y=0, line_color='rgba(255,255,255,0.3)', line_width=1.2)
        fig_res.add_hline(y=LOO_RMSE,  line_color=P['grey'], line_dash='dash', line_width=1.2,
                          annotation_text=f'+{LOO_RMSE:.2f}', annotation_font_color=P['grey'])
        fig_res.add_hline(y=-LOO_RMSE, line_color=P['grey'], line_dash='dash', line_width=1.2,
                          annotation_text=f'−{LOO_RMSE:.2f}', annotation_font_color=P['grey'])
        layout_res = {**PLOTLY_LAYOUT}
        layout_res['title'] = dict(
            text='Prediction Error by Year<br>'
                 '<sup style="color:rgba(255,255,255,0.35)">Blue = model too high · Orange = model too low · Dashed = avg error boundary</sup>',
            font=dict(family="Playfair Display, serif", size=14, color='white')
        )
        layout_res['xaxis'] = dict(**PLOTLY_LAYOUT['xaxis'],
                                    tickmode='array', tickvals=years.tolist(),
                                    title=dict(text='Year', font=dict(size=10)))
        layout_res['yaxis'] = dict(**PLOTLY_LAYOUT['yaxis'],
                                    title=dict(text='Error (t/ha)', font=dict(size=10)))
        layout_res['height'] = 400
        fig_res.update_layout(**layout_res)
        st.plotly_chart(fig_res, use_container_width=True, config={"responsive": True})

    st.markdown("---")
    col_f1, col_f2 = st.columns([1, 1])

    with col_f1:
        perm_importance = {
            'Humidity — Short Rains (Sep–Nov)': 0.0290,
            'Rainfall — Dry Season (Dec–Feb)':  0.0287,
            'Long Rains Rainfall Share':         0.0249,
            'Temperature — Short Rains':         0.0132,
            'Rainfall — Off Season (Jun–Aug)':   0.0073,
            'Soil Wetness — Short Rains':        0.0041,
        }
        imp_df = pd.DataFrame(list(perm_importance.items()),
                               columns=['Variable', 'Importance']).sort_values('Importance')

        fig_imp = go.Figure(go.Bar(
            x=imp_df['Importance'], y=imp_df['Variable'],
            orientation='h',
            marker_color=P['gold'],
            marker_line_color='rgba(0,0,0,0)',
            hovertemplate='<b>%{y}</b><br>Importance: %{x:.4f}<extra></extra>',
        ))
        layout_imp = {**PLOTLY_LAYOUT}
        layout_imp['title'] = dict(
            text='Which Variables Matter Most?<br>'
                 '<sup style="color:rgba(255,255,255,0.35)">Longer bar = removing this variable hurts accuracy more</sup>',
            font=dict(family="Playfair Display, serif", size=14, color='white')
        )
        layout_imp['xaxis'] = dict(**PLOTLY_LAYOUT['xaxis'],
                                    title=dict(text='Accuracy loss without this variable', font=dict(size=10)))
        layout_imp['height'] = 340
        layout_imp['margin'] = dict(t=70, b=40, l=210, r=10)
        fig_imp.update_layout(**layout_imp)
        st.plotly_chart(fig_imp, use_container_width=True, config={"responsive": True})

        st.markdown("""
        <div class="info-box">
        <b>Key insight:</b> 3 of the top 4 variables describe September–February —
        <i>before</i> planting begins. The harvest outcome is largely set before the farmer plants.
        </div>
        """, unsafe_allow_html=True)

    with col_f2:
        st.markdown("### Overall Model Reliability")
        reliability = [
            ("Is the seasonal design sound?",        "★★★★★", "Year split into 4 seasons — captures timing, not just totals"),
            ("Is the accuracy test honest?",          "★★★★★", "Leave-One-Out — no year tested on data it trained with"),
            ("Is the model free of data leakage?",    "★★★★★", "Yield excluded from inputs — no leakage"),
            ("Are the predictors well chosen?",       "★★★★☆", "6 from 38 — justified by data + crop science"),
            ("Is the algorithm appropriate?",         "★★★★☆", "RF + SVR well suited for small datasets"),
            ("Can results be trusted for planning?",  "★★★☆☆", "Directional patterns reliable — treat as estimates"),
            ("Is there enough historical data?",      "★★☆☆☆", "12 years only — 20+ would improve all estimates"),
        ]
        table_html = """
        <table class="rel-table">
            <tr><th>Question</th><th>Rating</th><th>What it means</th></tr>
        """
        for q, r, m in reliability:
            table_html += f"<tr><td>{q}</td><td>{r}</td><td>{m}</td></tr>"
        table_html += "</table>"
        st.markdown(table_html, unsafe_allow_html=True)

        st.markdown("""
        <div class="warn-box" style="margin-top:12px;">
        <b>Bottom line:</b> This model reliably identifies which weather conditions lead to better
        or worse harvests and is useful for seasonal planning. It is not designed for precise
        operational forecasting until more historical data becomes available.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Full Results — All 12 Years")

    pred_table = pd.DataFrame({
        'Year':                years,
        'Actual Yield (t/ha)': actual.round(3),
        'Model Prediction':    LOO_PRED.round(3),
        'Difference (t/ha)':   (LOO_PRED - actual).round(3),
        'Variety':             master['Variety'].values,
    })
    st.dataframe(
        pred_table.style
            .format({'Actual Yield (t/ha)': '{:.3f}',
                     'Model Prediction':    '{:.3f}',
                     'Difference (t/ha)':   '{:+.3f}'})
            .background_gradient(subset=['Actual Yield (t/ha)'], cmap='YlGn'),
        use_container_width=True, hide_index=True,
    )

# =============================================================================
# FOOTER
# =============================================================================

st.markdown("---")
st.markdown("""
<div style="background:#150800;border:1px solid rgba(212,168,83,0.12);
            border-radius:10px;padding:16px 24px 14px;margin-top:4px;text-align:center;">
    <div style="font-family:'DM Mono',monospace;font-size:0.68rem;letter-spacing:0.5px;
                color:#A89070;margin-bottom:10px;">
        Maize Yield Prediction — Uasin Gishu County, Kenya &nbsp;·&nbsp;
        KCA Tech Expo · March 2026 &nbsp;·&nbsp; IBM SkillsBuild Data Analytics Bootcamp
    </div>
    <div style="font-size:0.75rem;display:flex;justify-content:center;
                flex-wrap:wrap;gap:6px 20px;font-family:'DM Sans',sans-serif;">
        <span style="color:#7A6A55;">Data sources:</span>
        <a href="https://www.kilimo.go.ke" target="_blank"
           style="color:#D4A853;text-decoration:none;border-bottom:1px dotted rgba(212,168,83,0.4);">
            📋 Ministry of Agriculture, Kenya
        </a>
        <a href="https://power.larc.nasa.gov" target="_blank"
           style="color:#D4A853;text-decoration:none;border-bottom:1px dotted rgba(212,168,83,0.4);">
            🛰 NASA POWER
        </a>
        <a href="https://www.cimmyt.org" target="_blank"
           style="color:#D4A853;text-decoration:none;border-bottom:1px dotted rgba(212,168,83,0.4);">
            🌽 CIMMYT
        </a>
        <a href="https://www.purdue.edu" target="_blank"
           style="color:#D4A853;text-decoration:none;border-bottom:1px dotted rgba(212,168,83,0.4);">
            🔬 Purdue University
        </a>
        <a href="https://www.isric.org/explore/soil-geographic-databases" target="_blank"
           style="color:#D4A853;text-decoration:none;border-bottom:1px dotted rgba(212,168,83,0.4);">
            🌱 ISRIC · KENSOTER v2.0
        </a>
    </div>
</div>
""", unsafe_allow_html=True)
