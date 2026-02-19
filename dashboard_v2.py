"""
=============================================================================
HHS Unaccompanied Children Program — Analytics Dashboard
Industry-Standard · Portfolio-Ready · Healthcare / Public Sector
=============================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="HHS UAC Program | Analytics Dashboard",
    page_icon="🧒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# STYLES
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
*, html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }

.stApp { background: #0f172a; color: #f8fafc; }
#MainMenu, footer { visibility: hidden; }
.block-container { padding: 0 1.8rem 2rem !important; max-width: 100% !important; }

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #111827 !important;
    border-right: 1px solid #1e293b !important;
    min-width: 320px !important;
}
[data-testid="stSidebarContent"] { background-color: #111827 !important; }
[data-testid="stSidebarContent"] * { color: #f1f5f9; }
.sidebar-header {
    background: rgba(30, 58, 138, 0.3);
    padding: 24px 20px;
    border-radius: 12px;
    margin: 10px 0 25px 0;
    border: 1px solid rgba(59, 130, 246, 0.2);
    text-align: center;
}

/* User Capabilities Style from Image */
.uc-group { margin: 1.5rem 0 2rem; position: relative; padding-left: 28px; }
.uc-dot { 
    position: absolute; left: 0; top: 6px; width: 14px; height: 14px; 
    background: #3b82f6; border-radius: 50%; z-index: 2;
    box-shadow: 0 0 12px rgba(59, 130, 246, 0.6);
}
.uc-line { 
    position: absolute; left: 6px; top: 22px; height: 350px; width: 2px; 
    background: linear-gradient(180deg, #3b82f6 0%, rgba(59, 130, 246, 0.1) 100%); 
    z-index: 1;
}
.uc-title { font-size: 1.3rem; font-weight: 800; color: #f8fafc; margin-bottom: 25px; margin-top: -4px; }
.sb-sec-label {
    font-size: 0.9rem; font-weight: 700; color: #cbd5e1;
    display: flex; align-items: center; gap: 12px; margin-bottom: 12px;
}
.sb-sec-label i { color: #3b82f6; font-size: 1.1rem; }

/* Top header bar */
.top-header {
    background: linear-gradient(135deg, #1e3a5f 0%, #1e40af 100%);
    padding: 1.2rem 1.8rem;
    margin: 0 -1.8rem 1.4rem;
    display: flex; align-items: center; justify-content: space-between;
    flex-wrap: wrap; gap: 10px;
}
.top-header h1 {
    font-size: 1.15rem; font-weight: 800; color: #fff; margin: 0;
}
.top-header p { font-size: 0.68rem; color: rgba(255,255,255,0.6); margin: 3px 0 0; }
.top-header .badge {
    font-size: 0.65rem; background: rgba(255,255,255,0.15);
    color: #fff; border-radius: 20px; padding: 4px 12px;
    border: 1px solid rgba(255,255,255,0.2);
}

/* KPI cards */
.kpi-card {
    background: #1e293b; border: 1px solid #334155; border-radius: 12px;
    padding: 20px 22px; position: relative; overflow: hidden;
    min-height: 175px; display: flex; flex-direction: column;
}
.kpi-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 4px;
    background: var(--accent); border-radius: 12px 12px 0 0;
}
.kpi-icon  { font-size: 1.6rem; margin-bottom: 8px; }
.kpi-label { font-size: 0.65rem; font-weight: 700; letter-spacing: 0.12em;
             text-transform: uppercase; color: #94a3b8; margin-bottom: 6px; }
.kpi-value { font-size: 1.9rem; font-weight: 800; color: #f1f5f9; line-height: 1; margin-bottom: 8px; }
.kpi-delta { font-size: 0.75rem; font-weight: 600; margin-top: auto; padding-top: 8px; }
.kpi-sub   { font-size: 0.68rem; color: #64748b; margin-top: 4px; }

/* Alert */
.alert-box {
    border-radius: 8px; padding: 9px 13px;
    font-size: 0.73rem; font-weight: 600; margin: 6px 0; line-height: 1.4;
}
.alert-red    { background:#450a0a; border:1px solid #7f1d1d; color:#fca5a5; }
.alert-yellow { background:#451a03; border:1px solid #78350f; color:#fde68a; }
.alert-green  { background:#064e3b; border:1px solid #065f46; color:#a7f3d0; }

/* Insight box */
.insight-box {
    background: rgba(30, 58, 138, 0.45); 
    border: 1px solid rgba(59, 130, 246, 0.5); 
    border-radius: 14px;
    padding: 20px 24px; 
    font-size: 0.85rem; 
    color: #f1f5f9; 
    line-height: 1.7;
    margin: 30px 0 45px 0;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
    clear: both;
}
.insight-box b { color: #fff; text-decoration: underline; text-decoration-color: #3b82f6; text-underline-offset: 4px; }

/* Section divider */
.sec-div {
    background: linear-gradient(90deg, #1e3a8a 0%, #1e1b4b 100%);
    border-left: 4px solid #3b82f6;
    padding: 12px 18px;
    border-radius: 6px;
    margin: 1.8rem 0 1.2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}
.sec-div h3 { 
    font-size: 1.1rem; 
    font-weight: 700; 
    color: #f1f5f9; 
    margin: 0;
    letter-spacing: 0.02em;
}
.sec-tag {
    font-size: 0.65rem; 
    font-weight: 700; 
    letter-spacing: 0.08em;
    text-transform: uppercase; 
    padding: 4px 12px; 
    border-radius: 4px;
    background: rgba(59, 130, 246, 0.2); 
    color: #93c5fd;
    border: 1px solid rgba(59, 130, 246, 0.3);
}

/* Chart wrapper */
.chart-wrap {
    background: #1e293b; border: 1px solid #334155; border-radius: 12px;
    padding: 16px 16px 8px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s;
}
.chart-wrap:hover { transform: translateY(-2px); border-color: #3b82f6; }
.chart-title {
    font-size: 0.8rem; font-weight: 700; color: #f1f5f9;
    margin-bottom: 12px; display: flex; align-items: center; gap: 8px;
    padding-bottom: 8px; border-bottom: 1px solid #334155;
}

/* Sidebar labels */
.sb-sec {
    font-size: 0.6rem; font-weight: 700; letter-spacing: 0.12em;
    text-transform: uppercase; color: #94a3b8;
    margin: 1.2rem 0 0.4rem; padding-bottom: 4px;
    border-bottom: 1px solid #334155;
}

/* Ratio mini card */
.ratio-row {
    display: flex; align-items: center; justify-content: space-between;
    background: #0f172a; border: 1px solid #334155;
    border-radius: 7px; padding: 6px 10px; margin-bottom: 4px;
}
.ratio-lbl { font-size: 0.68rem; color: #94a3b8; }
.ratio-val { font-size: 0.82rem; font-weight: 700; }

/* Streamlit tab override */
[data-testid="stTabs"] button {
    font-size: 0.75rem !important; font-weight: 600 !important;
    color: #94a3b8 !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #3b82f6 !important; border-bottom-color: #3b82f6 !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────────────────────────────────────
import os

# ─────────────────────────────────────────────────────────────────────────────
# ROBUST PATH RESOLUTION (Local & Cloud)
# ─────────────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def resolve_path(filename, extension):
    """Checks script dir, current dir, and parent dir for the file."""
    search_paths = [
        BASE_DIR,                               # Script directory
        os.getcwd(),                             # Current directory
        os.path.dirname(BASE_DIR),              # Parent directory
    ]
    for p in search_paths:
        full_path = os.path.join(p, filename)
        if os.path.exists(full_path):
            return full_path
            
    # Fallback: Search for ANY file with the same extension in the script directory
    try:
        for f in os.listdir(BASE_DIR):
            if f.lower().endswith(extension.lower()):
                return os.path.join(BASE_DIR, f)
    except:
        pass
        
    return filename # Final fallback to string

CSV  = resolve_path("HHS_Unaccompanied_Alien_Children_Program.csv", ".csv")
LOGO = resolve_path("project 1 logo.jpg", ".jpg")

C_APP = "Children apprehended and placed in CBP custody*"
C_CBP = "Children in CBP custody"
C_TRN = "Children transferred out of CBP custody"
C_HHS = "Children in HHS Care"
C_DIS = "Children discharged from HHS Care"

BLUE  = "#1d4ed8"
TEAL  = "#0891b2"
GREEN = "#059669"
AMBER = "#d97706"
RED   = "#dc2626"
GREY  = "#64748b"

PLOTLY_THEME = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#94a3b8"),
)
MN = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
      7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}

@st.cache_data
def load():
    df = pd.read_csv(CSV)
    df.columns = df.columns.str.strip()
    df.dropna(how="all", inplace=True)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df.dropna(subset=["Date"], inplace=True)
    for c in [C_APP, C_CBP, C_TRN, C_HHS, C_DIS]:
        df[c] = pd.to_numeric(
            df[c].astype(str).str.replace(",","").str.strip(), errors="coerce"
        )
    df.sort_values("Date", inplace=True)
    df.reset_index(drop=True, inplace=True)
    df["Year"]      = df["Date"].dt.year
    df["Month"]     = df["Date"].dt.month
    df["YearMonth"] = df["Date"].dt.strftime("%Y-%m")
    df["Quarter"]   = df["Date"].dt.to_period("Q").astype(str)
    df["MonthName"] = df["Month"].map(MN)
    # Derived KPI columns
    df["Transfer_Eff"]  = (df[C_TRN] / df[C_APP].replace(0,np.nan) * 100).clip(0, 300)
    df["Discharge_Eff"] = (df[C_DIS] / df[C_HHS].replace(0,np.nan) * 100).clip(0, 100)
    df["Throughput"]    = (df[C_DIS] / df[C_APP].replace(0,np.nan) * 100).clip(0, 300)
    df["Backlog"]       = (df[C_CBP] - df[C_TRN]).clip(lower=0)
    df["Backlog_Rate"]  = (df["Backlog"] / df[C_CBP].replace(0,np.nan) * 100).clip(0, 100)
    return df

df_all = load()

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    # Adding Logo
    try:
        st.image(LOGO, use_container_width=True)
    except:
        st.markdown('<div style="font-size:3rem; text-align:center;">🧒</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-header">
        <div style="font-size:0.9rem;font-weight:800;color:#f9fafb;">HHS UAC Program</div>
        <div style="font-size:0.65rem;color:#94a3b8;margin-top:4px;">Analytics Dashboard · ORR</div>
        <div style="margin-top:10px; display:inline-block; background:#064e3b; color:#a7f3d0; 
                    padding:2px 8px; border-radius:10px; font-size:0.6rem; font-weight:700;">
            ● SYSTEM ACTIVE
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Main Function Groups
    st.markdown("""
    <div class="uc-group">
        <div class="uc-dot"></div>
        <div class="uc-line"></div>
        <div class="uc-title">User Capabilities</div>
    </div>
    """, unsafe_allow_html=True)

    # Function 1: Date Range Selection
    st.markdown('<div class="sb-sec-label">📅 Date Range Selection</div>', unsafe_allow_html=True)
    years_all = sorted(df_all["Year"].unique().tolist())
    sel_years = st.multiselect("Select Year(s)", years_all, default=years_all)
    dmin = df_all["Date"].min().date()
    dmax = df_all["Date"].max().date()
    dr   = st.date_input("Select Custom Range", value=(dmin, dmax), min_value=dmin, max_value=dmax)
    s_dt = pd.Timestamp(dr[0]) if len(dr)==2 else df_all["Date"].min()
    e_dt = pd.Timestamp(dr[1]) if len(dr)==2 else df_all["Date"].max()

    df = df_all[
        df_all["Year"].isin(sel_years) &
        (df_all["Date"] >= s_dt) & (df_all["Date"] <= e_dt)
    ].copy()
    st.caption(f"📊 {len(df):,} records active")
    st.markdown("<br>", unsafe_allow_html=True)

    # Function 2: Ratio-based Metric Toggles
    st.markdown('<div class="sb-sec-label">🔄 Ratio-based Metric Toggles</div>', unsafe_allow_html=True)
    show_ratio   = st.toggle("View as Ratio (%)",    value=True)
    show_rolling = st.toggle("Apply Rolling Averages",     value=True)
    show_target  = st.toggle("Enable Target Lines",    value=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Function 3: Threshold-based Alerts (Visual)
    st.markdown('<div class="sb-sec-label">🚨 Threshold-based Alerts</div>', unsafe_allow_html=True)

    # Compute live ratios
    if len(df) > 0:
        avg_app = df[C_APP].mean() or 1
        avg_trn = df[C_TRN].mean() or 0
        avg_hhs = df[C_HHS].mean() or 1
        avg_dis = df[C_DIS].mean() or 0
        avg_cbp = df[C_CBP].mean() or 1
        r_te  = avg_trn / avg_app * 100
        r_de  = avg_dis / avg_hhs * 100
        r_tp  = avg_dis / avg_app * 100
        r_bl  = max(0, (avg_cbp - avg_trn) / avg_cbp * 100)
    else:
        r_te = r_de = r_tp = r_bl = 0

    ratios = [
        ("🔄","Transfer Eff.",  f"{r_te:.1f}%",  BLUE),
        ("✅","Discharge Eff.", f"{r_de:.2f}%", GREEN),
        ("⚡","Throughput",     f"{r_tp:.1f}%",  TEAL),
        ("📦","Backlog Rate",   f"{r_bl:.1f}%",  AMBER),
    ]
    for icon,lbl,val,col in ratios:
        st.markdown(f"""
        <div class="ratio-row">
            <span class="ratio-lbl">{icon} {lbl}</span>
            <span class="ratio-val" style="color:{col};">{val}</span>
        </div>""", unsafe_allow_html=True)

    # Thresholds
    st.markdown('<div class="sb-sec">🚨 Alert Thresholds</div>', unsafe_allow_html=True)
    thr_cbp = st.slider("CBP Custody",    50,  600,  200, 10)
    thr_hhs = st.slider("HHS Care",       500, 15000, 5000, 100)
    thr_bl  = st.slider("Backlog Rate %", 10,  90,   50,  5)

    if len(df) > 0:
        last_cbp = float(df[C_CBP].iloc[-1])
        last_hhs = float(df[C_HHS].iloc[-1])
        def alert_html(val, thr, lbl, pct=False):
            v = f"{val:.1f}%" if pct else f"{int(val):,}"
            t = f"{thr:.0f}%" if pct else f"{int(thr):,}"
            if val > thr:
                return f'<div class="alert-box alert-red">🔴 {lbl}: <b>{v}</b> exceeds {t}</div>'
            elif val > thr * 0.8:
                return f'<div class="alert-box alert-yellow">🟡 {lbl}: <b>{v}</b> nearing {t}</div>'
            return f'<div class="alert-box alert-green">🟢 {lbl}: <b>{v}</b> — Within range</div>'
        st.markdown(alert_html(last_cbp, thr_cbp, "CBP Custody"),     unsafe_allow_html=True)
        st.markdown(alert_html(last_hhs, thr_hhs, "HHS Care"),        unsafe_allow_html=True)
        st.markdown(alert_html(r_bl,     thr_bl,  "Backlog Rate", True), unsafe_allow_html=True)

    # Added Export Section
    st.markdown('<div class="sb-sec">📤 Export Options</div>', unsafe_allow_html=True)
    if st.button("Download Current View (.csv)"):
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Confirm Download",
            data=csv_data,
            file_name=f"uac_data_export_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
        )

    st.markdown("---")
    st.markdown("<small style='color:#cbd5e1;'>HHS · ORR · Data through Dec 2025</small>",
                unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# GUARD
# ─────────────────────────────────────────────────────────────────────────────
if len(df) == 0:
    st.warning("⚠️ No data for selected filters. Adjust sidebar controls.")
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# TOP HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="top-header">
  <div style="display:flex;align-items:center;gap:14px;">
    <div style="font-size:2rem;">🧒</div>
    <div>
      <h1>HHS Unaccompanied Children Program</h1>
      <p>U.S. Dept. of Health &amp; Human Services · Office of Refugee Resettlement · Care Pipeline Analytics</p>
    </div>
  </div>
  <div class="badge">📅 {s_dt.strftime('%b %d %Y')} → {e_dt.strftime('%b %d %Y')}</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# KPI SUMMARY ROW
# ─────────────────────────────────────────────────────────────────────────────
last = df.iloc[-1]
prev = df.iloc[-2] if len(df) > 1 else df.iloc[-1]

def delta_str(cur, prv, good_down=True):
    d = cur - prv
    if d == 0: return "— No change", GREY
    up = d > 0
    good = (not up) if good_down else up
    col = GREEN if good else RED
    sym = "▲" if up else "▼"
    return f"{sym} {abs(int(d)):,} vs prev", col

d1, c1 = delta_str(last[C_APP], prev[C_APP])
d2, c2 = delta_str(last[C_CBP], prev[C_CBP])
d3, c3 = delta_str(last[C_HHS], prev[C_HHS])
d4, c4 = delta_str(last[C_DIS], prev[C_DIS], good_down=False)
d5, c5 = delta_str(last["Transfer_Eff"], prev["Transfer_Eff"], good_down=False)

kpi_data = [
    ("🚔", "Daily Apprehended",    f"{int(last[C_APP]):,}",        d1, c1, "CBP intake",           "#3b82f6"),
    ("🏛️", "CBP Custody",          f"{int(last[C_CBP]):,}",        d2, c2, "In CBP custody",       "#f59e0b"),
    ("🏠", "HHS Care",             f"{int(last[C_HHS]):,}",        d3, c3, "In HHS care",           "#10b981"),
    ("📤", "Daily Discharged",     f"{int(last[C_DIS]):,}",        d4, c4, "Placed / discharged",   "#8b5cf6"),
    ("⚡", "Transfer Efficiency",  f"{last['Transfer_Eff']:.1f}%", d5, c5, "CBP→HHS speed ratio",  "#0891b2"),
]

cols = st.columns(5)
for col, (icon, label, val, delta, dcol, sub, accent) in zip(cols, kpi_data):
    with col:
        st.markdown(f"""
        <div class="kpi-card" style="--accent:{accent};">
            <div class="kpi-icon">{icon}</div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{val}</div>
            <div class="kpi-delta" style="color:{dcol};">{delta}</div>
            <div class="kpi-sub">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='height:2.5rem'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────
def base(fig, h=290, dual=False):
    fig.update_layout(
        **PLOTLY_THEME, height=h,
        margin=dict(l=0, r=0, t=8, b=50),
        xaxis=dict(showgrid=False, zeroline=False, color=GREY,
                   tickfont=dict(size=10), automargin=True),
        yaxis=dict(gridcolor="#334155", zeroline=False, color=GREY,
                   tickfont=dict(size=10)),
        hovermode="x unified",
        legend=dict(orientation="h", y=1.1, x=0,
                    font=dict(size=10, color=GREY),
                    bgcolor="rgba(0,0,0,0)"),
    )
    if dual:
        fig.update_layout(
            yaxis2=dict(overlaying="y", side="right",
                        showgrid=False, zeroline=False,
                        color=GREY, tickfont=dict(size=10))
        )
    return fig

def ctitle(icon, text):
    st.markdown(
        f'<div class="chart-title">{icon}&nbsp;{text}</div>',
        unsafe_allow_html=True
    )

def cw(): st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
def cw_end(): st.markdown('</div>', unsafe_allow_html=True)

def insight(text):
    st.markdown(f'<div class="insight-box">💡 {text}</div>', unsafe_allow_html=True)

def sec(icon, title, tag="4 Charts"):
    st.markdown(f"""
    <div class="sec-div">
        <div style="display:flex; align-items:center; gap:12px;">
            <span style="font-size:1.4rem;">{icon}</span>
            <h3>{title}</h3>
        </div>
        <span class="sec-tag">{tag}</span>
    </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────────────
tab0, tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏛️ Overview",
    "🔄 Transfers",
    "✅ Placements",
    "⚡ Throughput",
    "📦 Backlog",
    "📊 Stability",
])

# ═════════════════════════════════════════════════════════════════════════════
# TAB 0 — EXECUTIVE OVERVIEW
# ═════════════════════════════════════════════════════════════════════════════
with tab0:
    sec("🏛️", "Executive Program Overview", "Summary of All KPIs")
    
    o_c1, o_c2 = st.columns(2)
    with o_c1:
        cw(); ctitle("🔄", "CBP → HHS Transfer Efficiency (14d MA)")
        f0_1 = go.Figure()
        f0_1.add_trace(go.Scatter(x=df["Date"], y=df["Transfer_Eff"].rolling(14).mean(),
                                 fill='tozeroy', line=dict(color=BLUE, width=3),
                                 fillcolor="rgba(30,64,175,0.1)"))
        base(f0_1, h=250)
        st.plotly_chart(f0_1, use_container_width=True)
        cw_end()
        
        cw(); ctitle("📦", "CBP Backlog Accumulation (Children)")
        f0_3 = go.Figure(go.Scatter(x=df["Date"], y=df["Backlog"],
                                   fill='tozeroy', line=dict(color=AMBER, width=2),
                                   fillcolor="rgba(217,119,6,0.1)"))
        base(f0_3, h=250)
        st.plotly_chart(f0_3, use_container_width=True)
        cw_end()

    with o_c2:
        cw(); ctitle("✅", "HHS Placement Effectiveness (%)")
        f0_2 = go.Figure(go.Scatter(x=df["Date"], y=df["Discharge_Eff"].rolling(14).mean(),
                                   fill='tozeroy', line=dict(color=GREEN, width=3),
                                   fillcolor="rgba(5,150,105,0.1)"))
        base(f0_2, h=250)
        st.plotly_chart(f0_2, use_container_width=True)
        cw_end()
        
        cw(); ctitle("🔽", "Current Pipeline Status (Funnel)")
        stages = ["Apprehended", "Custody", "HHS Care", "Discharged"]
        vals = [df[C_APP].sum(), df[C_CBP].mean()*len(df), df[C_HHS].mean()*len(df), df[C_DIS].sum()]
        f0_4 = go.Figure(go.Funnel(y=stages, x=vals, marker=dict(color=[RED, AMBER, BLUE, GREEN])))
        base(f0_4, h=250)
        st.plotly_chart(f0_4, use_container_width=True)
        cw_end()

# ═════════════════════════════════════════════════════════════════════════════
# KPI 1 — TRANSFER EFFICIENCY RATIO
# ═════════════════════════════════════════════════════════════════════════════
with tab1:
    sec("🔄", "Transfer Efficiency Ratio", "CBP → HHS Speed")

    # KPI metric row
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Avg Transfer Efficiency", f"{df['Transfer_Eff'].mean():.1f}%",
                  delta=f"{df['Transfer_Eff'].mean() - df_all['Transfer_Eff'].mean():.1f}% vs all-time")
    with m2:
        st.metric("Peak Efficiency", f"{df['Transfer_Eff'].max():.1f}%")
    with m3:
        st.metric("Days Above 80% Target",
                  f"{(df['Transfer_Eff'] >= 80).sum():,}",
                  delta=f"{(df['Transfer_Eff'] >= 80).mean()*100:.0f}% of period")

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    r1c1, r1c2 = st.columns(2)

    # Chart 1 — Trend line
    with r1c1:
        cw(); ctitle("📈", "Transfer Efficiency Trend Over Time")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df["Date"], y=df["Transfer_Eff"],
            name="Daily", mode="lines",
            line=dict(color="rgba(29,78,216,0.3)", width=1),
        ))
        if show_rolling:
            fig.add_trace(go.Scatter(
                x=df["Date"], y=df["Transfer_Eff"].rolling(14, min_periods=1).mean(),
                name="14-Day MA", line=dict(color=BLUE, width=2.2),
            ))
        if show_target:
            fig.add_hline(y=80, line_dash="dash", line_color=GREEN,
                          annotation_text="Target 80%",
                          annotation_font_color=GREEN,
                          annotation_position="top right")
        base(fig)
        fig.update_layout(yaxis=dict(title="Efficiency %", gridcolor="#f1f5f9"))
        st.plotly_chart(fig, use_container_width=True)
        cw_end()

    # Chart 2 — Monthly bar
    with r1c2:
        cw(); ctitle("📊", "Monthly Avg Transfer Efficiency")
        monthly_te = df.groupby("YearMonth")["Transfer_Eff"].mean().reset_index()
        colors = [GREEN if v >= 80 else AMBER if v >= 60 else RED
                  for v in monthly_te["Transfer_Eff"]]
        fig2 = go.Figure(go.Bar(
            x=monthly_te["YearMonth"], y=monthly_te["Transfer_Eff"],
            marker_color=colors,
            hovertemplate="%{x}<br>Efficiency: %{y:.1f}%<extra></extra>",
        ))
        if show_target:
            fig2.add_hline(y=80, line_dash="dot", line_color=GREEN,
                           annotation_text="80% target")
        base(fig2)
        fig2.update_layout(
            xaxis=dict(tickangle=-30, showgrid=False, dtick="M3"),
            yaxis=dict(title="Efficiency %", gridcolor="#f1f5f9"),
            showlegend=False,
        )
        st.plotly_chart(fig2, use_container_width=True)
        cw_end()

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    r2c1, r2c2 = st.columns(2)

    # Chart 3 — Box plot by year
    with r2c1:
        cw(); ctitle("📦", "Transfer Efficiency Distribution by Year")
        fig3 = go.Figure()
        colors_yr = [BLUE, TEAL, GREEN, AMBER, RED, "#8b5cf6"]
        for i, yr in enumerate(sorted(df["Year"].unique())):
            sub = df[df["Year"] == yr]["Transfer_Eff"].dropna()
            fig3.add_trace(go.Box(
                y=sub, name=str(yr),
                marker_color=colors_yr[i % len(colors_yr)],
                boxmean="sd", line=dict(width=1.5), showlegend=False,
            ))
        base(fig3)
        fig3.update_layout(
            yaxis=dict(title="Efficiency %", gridcolor="#f1f5f9"),
            xaxis=dict(title="Year", showgrid=False),
        )
        st.plotly_chart(fig3, use_container_width=True)
        cw_end()

    # Chart 4 — Monthly heatmap
    with r2c2:
        cw(); ctitle("🗓️", "Transfer Efficiency Heatmap (Month × Year)")
        piv = df.groupby(["Year","Month"])["Transfer_Eff"].mean().reset_index()
        pw  = piv.pivot(index="Year", columns="Month", values="Transfer_Eff")
        pw.columns = [MN.get(c,c) for c in pw.columns]
        fig4 = go.Figure(go.Heatmap(
            z=pw.values, x=pw.columns.tolist(),
            y=[str(y) for y in pw.index.tolist()],
            colorscale=[[0,"#1e3a8a"],[0.5,"#f59e0b"],[1,"#10b981"]],
            hoverongaps=False,
            hovertemplate="Year: %{y}  Month: %{x}<br>Eff: %{z:.1f}%<extra></extra>",
            colorbar=dict(title="%", thickness=10, tickfont=dict(size=9, color="#94a3b8")),
        ))
        base(fig4)
        st.plotly_chart(fig4, use_container_width=True)
        cw_end()

    
# ═════════════════════════════════════════════════════════════════════════════
# KPI 2 — DISCHARGE EFFECTIVENESS INDEX
# ═════════════════════════════════════════════════════════════════════════════
with tab2:
    sec("✅", "Discharge Effectiveness Index", "Placement Success Rate")

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Avg Discharge Rate", f"{df['Discharge_Eff'].mean():.2f}%",
                  delta=f"{df['Discharge_Eff'].mean() - df_all['Discharge_Eff'].mean():.2f}% vs all-time")
    with m2:
        st.metric("Total Discharged", f"{int(df[C_DIS].sum()):,}")
    with m3:
        st.metric("Total in HHS Care (Avg)", f"{int(df[C_HHS].mean()):,}")

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    r1c1, r1c2 = st.columns(2)

    # Chart 5 — Discharge trend
    with r1c1:
        cw(); ctitle("📈", "Discharge Effectiveness Trend")
        fig5 = go.Figure()
        fig5.add_trace(go.Scatter(
            x=df["Date"], y=df["Discharge_Eff"],
            name="Daily", fill="tozeroy",
            line=dict(color=GREEN, width=2),
            fillcolor="rgba(5,150,105,0.08)",
        ))
        if show_rolling:
            fig5.add_trace(go.Scatter(
                x=df["Date"], y=df["Discharge_Eff"].rolling(14, min_periods=1).mean(),
                name="14-Day MA", line=dict(color="#065f46", width=2.2),
            ))
        if show_target:
            fig5.add_hline(y=5, line_dash="dash", line_color=AMBER,
                           annotation_text="Target 5%",
                           annotation_font_color=AMBER,
                           annotation_position="top right")
        base(fig5)
        fig5.update_layout(yaxis=dict(title="Discharge Rate %", gridcolor="#f1f5f9"))
        st.plotly_chart(fig5, use_container_width=True)
        cw_end()

    # Chart 6 — Pie: HHS Care vs Discharged (latest month)
    with r1c2:
        cw(); ctitle("🥧", "Care Status Breakdown (Latest Month)")
        last_month = df.tail(30)
        total_hhs  = last_month[C_HHS].mean()
        total_dis  = last_month[C_DIS].sum()
        remaining  = max(0, total_hhs - total_dis)
        fig6 = go.Figure(go.Pie(
            labels=["Discharged (30d)", "Still in Care"],
            values=[total_dis, remaining],
            hole=0.5,
            marker=dict(colors=[GREEN, "#e2e8f0"]),
            textfont=dict(size=11),
            hovertemplate="%{label}: %{value:,.0f}<extra></extra>",
        ))
        fig6.update_layout(
            **PLOTLY_THEME, height=290,
            margin=dict(l=0, r=0, t=8, b=0),
            legend=dict(orientation="h", y=-0.1, x=0.1,
                        font=dict(size=10, color=GREY)),
            annotations=[dict(text=f"{total_dis/max(total_hhs,1)*100:.0f}%",
                              x=0.5, y=0.5, font=dict(size=18, color=GREEN), showarrow=False)],
        )
        st.plotly_chart(fig6, use_container_width=True)
        cw_end()

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    r2c1, r2c2 = st.columns(2)

    # Chart 7 — Monthly discharge vs intake stacked bar
    with r2c1:
        cw(); ctitle("📊", "Monthly Intake vs Discharge (last 24 months)")
        mio = df.groupby("YearMonth").agg(
            Intake=(C_APP,"sum"), Discharge=(C_DIS,"sum")
        ).reset_index().tail(24)
        fig7 = go.Figure()
        fig7.add_trace(go.Bar(x=mio["YearMonth"], y=mio["Intake"],
            name="Intake", marker_color="#fca5a5", opacity=0.9))
        fig7.add_trace(go.Bar(x=mio["YearMonth"], y=mio["Discharge"],
            name="Discharged", marker_color=GREEN, opacity=0.9))
        base(fig7)
        fig7.update_layout(
            barmode="group",
            xaxis=dict(tickangle=-30, showgrid=False, dtick="M6"),
            yaxis=dict(title="Children", gridcolor="#f1f5f9"),
        )
        st.plotly_chart(fig7, use_container_width=True)
        cw_end()

    # Chart 8 — HHS Care box by year
    with r2c2:
        cw(); ctitle("📦", "HHS Care Distribution by Year")
        fig8 = go.Figure()
        colors_yr = [BLUE, TEAL, GREEN, AMBER, RED, "#8b5cf6"]
        for i, yr in enumerate(sorted(df["Year"].unique())):
            sub = df[df["Year"]==yr][C_HHS].dropna()
            fig8.add_trace(go.Box(
                y=sub, name=str(yr),
                marker_color=colors_yr[i % len(colors_yr)],
                boxmean="sd", line=dict(width=1.5), showlegend=False,
            ))
        base(fig8)
        fig8.update_layout(
            yaxis=dict(title="Children in HHS Care", gridcolor="#f1f5f9"),
            xaxis=dict(title="Year", showgrid=False),
        )
        st.plotly_chart(fig8, use_container_width=True)
        cw_end()

    with st.expander("💡 Insight — Discharge Effectiveness"):
        avg_de = df["Discharge_Eff"].mean()
        insight(f"""
        <b>Average Discharge Rate: {avg_de:.2f}% per day</b> of children in HHS care are discharged.
        A higher rate indicates faster successful placements. The pie chart shows the proportion
        discharged in the last 30 days vs still in care. Stacked bars reveal months where intake
        significantly outpaces discharges — a leading indicator of care capacity pressure.
        """)

# ═════════════════════════════════════════════════════════════════════════════
# KPI 3 — PIPELINE THROUGHPUT
# ═════════════════════════════════════════════════════════════════════════════
with tab3:
    sec("⚡", "Pipeline Throughput", "Total System Movement")

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Avg Throughput Ratio", f"{df['Throughput'].mean():.1f}%",
                  delta=f"{df['Throughput'].mean() - df_all['Throughput'].mean():.1f}% vs all-time")
    with m2:
        st.metric("Total Apprehended", f"{int(df[C_APP].sum()):,}")
    with m3:
        st.metric("Total Transferred", f"{int(df[C_TRN].sum()):,}")

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    r1c1, r1c2 = st.columns(2)

    # Chart 9 — Area chart throughput
    with r1c1:
        cw(); ctitle("📈", "Pipeline Throughput Over Time")
        fig9 = go.Figure()
        for col, color, fill_rgba, lbl in [
            (C_APP, "#fca5a5", "rgba(252,165,165,0.3)", "Apprehended"),
            (C_TRN, "#93c5fd", "rgba(147,197,253,0.3)", "Transferred"),
            (C_DIS, "#86efac", "rgba(134,239,172,0.3)", "Discharged"),
        ]:
            fig9.add_trace(go.Scatter(
                x=df["Date"], y=df[col],
                name=lbl, fill="tozeroy",
                line=dict(width=1.5),
                fillcolor=fill_rgba,
                line_color=color,
            ))
        base(fig9)
        fig9.update_layout(yaxis=dict(title="Children", gridcolor="#f1f5f9"))
        st.plotly_chart(fig9, use_container_width=True)
        cw_end()

    # Chart 10 — Funnel chart (pipeline stages)
    with r1c2:
        cw(); ctitle("🔽", "Care Pipeline Funnel (Period Totals)")
        stages = ["Apprehended", "In CBP Custody", "Transferred to HHS", "In HHS Care", "Discharged"]
        values = [
            df[C_APP].sum(), df[C_CBP].mean() * len(df),
            df[C_TRN].sum(), df[C_HHS].mean() * len(df),
            df[C_DIS].sum(),
        ]
        fig10 = go.Figure(go.Funnel(
            y=stages, x=values,
            textposition="inside",
            textinfo="value+percent initial",
            marker=dict(color=[RED, AMBER, BLUE, GREEN, "#8b5cf6"]),
            connector=dict(line=dict(color="#e2e8f0", width=1)),
        ))
        fig10.update_layout(
            height=290,
            margin=dict(l=0, r=0, t=8, b=0),
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#94a3b8"),
        )
        st.plotly_chart(fig10, use_container_width=True)
        cw_end()

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    r2c1, r2c2 = st.columns(2)

    # Chart 11 — Quarterly throughput horizontal bar
    with r2c1:
        cw(); ctitle("📊", "Quarterly Throughput (Apprehended vs Discharged)")
        qtr = df.groupby("Quarter").agg(
            App=(C_APP,"sum"), Dis=(C_DIS,"sum")
        ).reset_index()
        fig11 = go.Figure()
        fig11.add_trace(go.Bar(
            y=qtr["Quarter"], x=qtr["App"],
            name="Apprehended", orientation="h",
            marker_color="#fca5a5", opacity=0.9,
        ))
        fig11.add_trace(go.Bar(
            y=qtr["Quarter"], x=qtr["Dis"],
            name="Discharged", orientation="h",
            marker_color=GREEN, opacity=0.9,
        ))
        base(fig11)
        fig11.update_layout(
            barmode="group",
            xaxis=dict(title="Children", gridcolor="#f1f5f9"),
            yaxis=dict(showgrid=False),
        )
        st.plotly_chart(fig11, use_container_width=True)
        cw_end()

    # Chart 12 — Rolling avg throughput
    with r2c2:
        cw(); ctitle("📉", "Throughput Ratio — Rolling Averages")
        fig12 = go.Figure()
        fig12.add_trace(go.Scatter(
            x=df["Date"], y=df["Throughput"],
            name="Daily", mode="lines",
            line=dict(color="rgba(8,145,178,0.25)", width=1),
        ))
        if show_rolling:
            for w, col, dash in [(7,TEAL,"solid"),(30,BLUE,"dot"),(90,AMBER,"dashdot")]:
                fig12.add_trace(go.Scatter(
                    x=df["Date"],
                    y=df["Throughput"].rolling(w, min_periods=1).mean(),
                    name=f"{w}-Day MA",
                    line=dict(color=col, width=2, dash=dash),
                ))
        base(fig12)
        fig12.update_layout(yaxis=dict(title="Throughput %", gridcolor="#f1f5f9"))
        st.plotly_chart(fig12, use_container_width=True)
        cw_end()

    with st.expander("💡 Insight — Pipeline Throughput"):
        tp = df["Throughput"].mean()
        insight(f"""
        <b>Average Pipeline Throughput: {tp:.1f}%</b> — this measures how many children
        discharged relative to those apprehended. The funnel chart reveals drop-off at each
        pipeline stage. Quarters where apprehensions significantly exceed discharges signal
        growing system pressure and potential capacity constraints.
        """)

# ═════════════════════════════════════════════════════════════════════════════
# KPI 4 — BACKLOG ACCUMULATION RATE
# ═════════════════════════════════════════════════════════════════════════════
with tab4:
    sec("📦", "Backlog Accumulation Rate", "Delay Severity Indicator")

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Avg Backlog", f"{int(df['Backlog'].mean()):,}",
                  delta=f"{int(df['Backlog'].mean() - df_all['Backlog'].mean()):,} vs all-time")
    with m2:
        st.metric("Peak Backlog", f"{int(df['Backlog'].max()):,}")
    with m3:
        bl_status = "🔴 High" if r_bl > thr_bl else ("🟡 Moderate" if r_bl > thr_bl*0.7 else "🟢 Low")
        st.metric("Backlog Rate", f"{r_bl:.1f}%", delta=bl_status)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    r1c1, r1c2 = st.columns(2)

    # Chart 13 — Backlog trend
    with r1c1:
        cw(); ctitle("📈", "CBP Backlog Trend Over Time")
        fig13 = go.Figure()
        fig13.add_trace(go.Scatter(
            x=df["Date"], y=df["Backlog"],
            name="Backlog", fill="tozeroy",
            line=dict(color=AMBER, width=2),
            fillcolor="rgba(217,119,6,0.1)",
        ))
        if show_rolling:
            fig13.add_trace(go.Scatter(
                x=df["Date"], y=df["Backlog"].rolling(14, min_periods=1).mean(),
                name="14-Day MA", line=dict(color=RED, width=2.2),
            ))
        if show_target:
            fig13.add_hline(y=df["Backlog"].mean(), line_dash="dash", line_color=GREY,
                            annotation_text="Period Avg",
                            annotation_font_color=GREY,
                            annotation_position="top right")
        base(fig13)
        fig13.update_layout(yaxis=dict(title="Backlog (Children)", gridcolor="#f1f5f9"))
        st.plotly_chart(fig13, use_container_width=True)
        cw_end()

    # Chart 14 — Histogram of backlog
    with r1c2:
        cw(); ctitle("📊", "Backlog Distribution (Histogram)")
        fig14 = go.Figure(go.Histogram(
            x=df["Backlog"].dropna(),
            nbinsx=30,
            marker=dict(
                color=df["Backlog"].dropna(),
                colorscale=[[0,"#dcfce7"],[0.5,"#fef9c3"],[1,"#fef2f2"]],
                showscale=False,
            ),
            hovertemplate="Backlog: %{x}<br>Count: %{y}<extra></extra>",
        ))
        base(fig14)
        fig14.update_layout(
            xaxis=dict(title="Backlog (Children)", showgrid=False),
            yaxis=dict(title="Frequency", gridcolor="#f1f5f9"),
            showlegend=False,
        )
        st.plotly_chart(fig14, use_container_width=True)
        cw_end()

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    r2c1, r2c2 = st.columns(2)

    # Chart 15 — Monthly backlog heatmap
    with r2c1:
        cw(); ctitle("🗓️", "Backlog Heatmap (Month × Year)")
        piv_bl = df.groupby(["Year","Month"])["Backlog"].mean().reset_index()
        pw_bl  = piv_bl.pivot(index="Year", columns="Month", values="Backlog")
        pw_bl.columns = [MN.get(c,c) for c in pw_bl.columns]
        fig15 = go.Figure(go.Heatmap(
            z=pw_bl.values, x=pw_bl.columns.tolist(),
            y=[str(y) for y in pw_bl.index.tolist()],
            colorscale=[[0,"#064e3b"],[0.5,"#f59e0b"],[1,"#ef4444"]],
            hoverongaps=False,
            hovertemplate="Year: %{y}  Month: %{x}<br>Backlog: %{z:,.0f}<extra></extra>",
            colorbar=dict(title="Count", thickness=10, tickfont=dict(size=9, color="#94a3b8")),
        ))
        base(fig15)
        st.plotly_chart(fig15, use_container_width=True)
        cw_end()

    # Chart 16 — Alert indicator gauge
    with r2c2:
        cw(); ctitle("🚨", "Backlog Rate Alert Indicator")
        fig16 = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=r_bl,
            delta=dict(reference=thr_bl, increasing=dict(color=RED),
                       decreasing=dict(color=GREEN)),
            gauge=dict(
                axis=dict(range=[0, 100], tickfont=dict(size=10, color=GREY)),
                bar=dict(color=AMBER if r_bl < thr_bl else RED, thickness=0.3),
                bgcolor="#f8fafc",
                bordercolor="#e2e8f0",
                steps=[
                    dict(range=[0, thr_bl*0.7],   color="#dcfce7"),
                    dict(range=[thr_bl*0.7, thr_bl], color="#fef9c3"),
                    dict(range=[thr_bl, 100],       color="#fef2f2"),
                ],
                threshold=dict(line=dict(color=RED, width=3),
                               thickness=0.8, value=thr_bl),
            ),
            title=dict(text="Backlog Rate %", font=dict(size=13, color=GREY)),
            number=dict(suffix="%", font=dict(size=32, color="#1e293b")),
        ))
        fig16.update_layout(
            **PLOTLY_THEME, height=290,
            margin=dict(l=30, r=30, t=30, b=20),
        )
        st.plotly_chart(fig16, use_container_width=True)
        cw_end()

    with st.expander("💡 Insight — Backlog Accumulation"):
        avg_bl = df["Backlog"].mean()
        insight(f"""
        <b>Average Backlog: {avg_bl:,.0f} children</b> remain in CBP custody beyond transfer.
        The gauge shows current backlog rate vs your threshold of {thr_bl}%.
        Red months in the heatmap indicate peak pressure periods requiring surge capacity.
        The histogram reveals whether backlogs are consistently low or have extreme outlier spikes.
        """)

# ═════════════════════════════════════════════════════════════════════════════
# KPI 5 — OUTCOME STABILITY SCORE
# ═════════════════════════════════════════════════════════════════════════════
with tab5:
    sec("📊", "Outcome Stability Score", "Consistency of Placements")

    # Compute stability metrics
    monthly_hhs = df.groupby("YearMonth")[C_HHS].agg(["mean","std"]).reset_index()
    monthly_hhs.columns = ["YearMonth","Mean","Std"]
    monthly_hhs["CV"] = (monthly_hhs["Std"] / monthly_hhs["Mean"].replace(0,np.nan) * 100).fillna(0)
    monthly_hhs["Stability"] = 100 - monthly_hhs["CV"].clip(0, 100)

    overall_stability = monthly_hhs["Stability"].mean()
    overall_cv        = monthly_hhs["CV"].mean()

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Stability Score", f"{overall_stability:.1f} / 100",
                  delta="Higher = more consistent")
    with m2:
        st.metric("Coefficient of Variation", f"{overall_cv:.1f}%",
                  delta="Lower = more stable")
    with m3:
        rolling_std = df[C_HHS].rolling(30, min_periods=1).std().iloc[-1]
        st.metric("30-Day Rolling Std Dev", f"{rolling_std:,.0f}")

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    r1c1, r1c2 = st.columns(2)

    # Chart 17 — Std deviation trend
    with r1c1:
        cw(); ctitle("📉", "Rolling Std Deviation — HHS Care (Stability Trend)")
        fig17 = go.Figure()
        fig17.add_trace(go.Scatter(
            x=df["Date"], y=df[C_HHS].rolling(30, min_periods=1).std(),
            name="30-Day Std Dev", fill="tozeroy",
            line=dict(color=BLUE, width=2),
            fillcolor="rgba(29,78,216,0.07)",
        ))
        fig17.add_trace(go.Scatter(
            x=df["Date"], y=df[C_HHS].rolling(90, min_periods=1).std(),
            name="90-Day Std Dev",
            line=dict(color=AMBER, width=2, dash="dot"),
        ))
        base(fig17)
        fig17.update_layout(yaxis=dict(title="Std Deviation", gridcolor="#f1f5f9"))
        st.plotly_chart(fig17, use_container_width=True)
        cw_end()

    # Chart 18 — Control chart (mean ± 2σ)
    with r1c2:
        cw(); ctitle("📊", "Control Chart — HHS Care (Mean ± 2σ)")
        roll_mean = df[C_HHS].rolling(30, min_periods=1).mean()
        roll_std  = df[C_HHS].rolling(30, min_periods=1).std().fillna(0)
        ucl = roll_mean + 2 * roll_std
        lcl = (roll_mean - 2 * roll_std).clip(lower=0)

        fig18 = go.Figure()
        fig18.add_trace(go.Scatter(
            x=df["Date"], y=ucl, name="UCL (+2σ)",
            line=dict(color=RED, width=1, dash="dash"), showlegend=True,
        ))
        fig18.add_trace(go.Scatter(
            x=df["Date"], y=lcl, name="LCL (−2σ)",
            line=dict(color=RED, width=1, dash="dash"),
            fill="tonexty", fillcolor="rgba(220,252,231,0.3)",
            showlegend=True,
        ))
        fig18.add_trace(go.Scatter(
            x=df["Date"], y=df[C_HHS],
            name="HHS Care", mode="lines",
            line=dict(color=BLUE, width=1.8),
        ))
        fig18.add_trace(go.Scatter(
            x=df["Date"], y=roll_mean,
            name="30-Day Mean", line=dict(color=GREEN, width=2, dash="dot"),
        ))
        base(fig18)
        fig18.update_layout(yaxis=dict(title="Children in HHS Care", gridcolor="#f1f5f9"))
        st.plotly_chart(fig18, use_container_width=True)
        cw_end()

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    r2c1, r2c2 = st.columns(2)


    # Chart 20 — Monthly stability score bar
    with r2c2:
        cw(); ctitle("📊", "Monthly Stability Score (100 = Perfectly Stable)")
        stab_colors = [GREEN if v >= 70 else AMBER if v >= 50 else RED
                       for v in monthly_hhs["Stability"]]
        fig20 = go.Figure(go.Bar(
            x=monthly_hhs["YearMonth"], y=monthly_hhs["Stability"],
            marker_color=stab_colors,
            hovertemplate="%{x}<br>Stability: %{y:.1f}<extra></extra>",
        ))
        if show_target:
            fig20.add_hline(y=70, line_dash="dash", line_color=GREEN,
                            annotation_text="Good (70+)",
                            annotation_font_color=GREEN)
        base(fig20)
        fig20.update_layout(
            xaxis=dict(tickangle=-30, showgrid=False, dtick="M3"),
            yaxis=dict(title="Stability Score", gridcolor="#f1f5f9", range=[0,105]),
            showlegend=False,
        )
        st.plotly_chart(fig20, use_container_width=True)
        cw_end()

    with st.expander("💡 Insight — Outcome Stability"):
        insight(f"""
        <b>Overall Stability Score: {overall_stability:.1f}/100</b> — 
        measured as 100 minus the Coefficient of Variation (CV%) of monthly HHS care counts.
        The control chart highlights periods where care population breached ±2σ control limits,
        indicating operational instability. Lower std deviation = more predictable, stable outcomes.
        Months scoring below 50 (red bars) warrant operational review.
        """)

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="border-top:1px solid #334155;margin-top:1.5rem;padding-top:0.8rem;
            text-align:center;color:#64748b;font-size:0.62rem;">
    HHS Unaccompanied Children Program · Analytics Dashboard &nbsp;·&nbsp;
    6 Sections · 20 Interactive Charts &nbsp;·&nbsp;
    Built with Streamlit &amp; Plotly &nbsp;·&nbsp;
    Data: HHS / ORR · Updated Dec 2025
</div>
""", unsafe_allow_html=True)
