
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import StringIO
import requests

# ============================================================
# KONFIGURASI
# ============================================================
st.set_page_config(
    page_title="Dashboard IDX Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

SPREADSHEET_ID = "1z2-UYSAGLHWb88LADmDKH4Y4pPFkM3aCJH5wPuw0Mp8"

# ============================================================
# CSS
# ============================================================
st.markdown("""
<style>
    #MainMenu, footer {visibility:hidden;}

    .stApp {
        background:#f4f8fc;
    }

    [data-testid="stSidebar"] {
        background:#edf3f9;
        border-right:1px solid #d9e4ef;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top:1.2rem;
    }

    .block-container {
        max-width:1500px;
        padding-top:1.5rem;
        padding-bottom:2rem;
    }

    h1,h2,h3,h4 {
        color:#063b78 !important;
    }

    .brand {
        font-size:34px;
        font-weight:900;
        color:#063b78;
        letter-spacing:-1.5px;
    }

    .brand-sub {
        font-size:11px;
        color:#6f88a1;
        margin-top:-5px;
        margin-bottom:22px;
    }

    .side-title {
        color:#063b78;
        font-size:17px;
        font-weight:800;
        margin-bottom:3px;
    }

    .side-sub {
        color:#8298ae;
        font-size:11px;
        line-height:1.5;
    }

    .hero {
        background:linear-gradient(135deg,#073d79 0%,#1d73ad 100%);
        color:white;
        padding:28px 32px;
        border-radius:18px;
        margin-bottom:22px;
        box-shadow:0 8px 24px rgba(6,59,120,.15);
    }

    .hero-kicker {
        font-size:12px;
        opacity:.78;
        letter-spacing:.5px;
        margin-bottom:6px;
    }

    .hero-title {
        font-size:31px;
        font-weight:850;
        line-height:1.15;
    }

    .hero-sub {
        font-size:14px;
        opacity:.88;
        margin-top:7px;
    }

    .section-title {
        color:#063b78;
        font-size:25px;
        font-weight:850;
        margin:22px 0 7px 0;
    }

    .section-sub {
        color:#8397aa;
        font-size:13px;
        margin-bottom:15px;
    }

    .kpi-card {
        background:white;
        border:1px solid #dce6f0;
        border-radius:16px;
        padding:19px 21px;
        min-height:126px;
        box-shadow:0 5px 18px rgba(24,65,105,.055);
    }

    .kpi-label {
        color:#7890aa;
        font-size:11px;
        font-weight:750;
        text-transform:uppercase;
        letter-spacing:.35px;
    }

    .kpi-value {
        color:#063b78;
        font-size:29px;
        font-weight:850;
        margin-top:11px;
        line-height:1;
    }

    .kpi-note {
        color:#9aabbc;
        font-size:11px;
        margin-top:8px;
    }

    .period-badge {
        display:inline-block;
        background:#e7f1fb;
        color:#063b78;
        padding:7px 14px;
        border-radius:20px;
        font-size:12px;
        font-weight:750;
        margin-bottom:10px;
    }

    .table-wrap {
        width:100%;
        background:white;
        border:1px solid #d9e3ed;
        border-radius:11px;
        overflow:hidden;
        box-shadow:0 2px 9px rgba(20,60,100,.04);
    }

    .table-scroll {
        max-height:470px;
        overflow-y:auto;
    }

    .growth-table {
        width:100%;
        border-collapse:collapse;
        font-size:12.5px;
    }

    .growth-table thead th {
        position:sticky;
        top:0;
        z-index:3;
        background:#eaf2fa;
        color:#526b84;
        font-weight:750;
        text-align:left;
        padding:10px 9px;
        border-bottom:1px solid #d5e0eb;
    }

    .growth-table tbody td {
        padding:9px;
        border-bottom:1px solid #e7edf3;
        color:#40566d;
        background:white;
    }

    .growth-table tbody tr:hover td {
        background:#f7fbff;
    }

    .growth-table tbody tr:last-child td {
        border-bottom:none;
    }

    .growth-table .num {
        width:30px;
        text-align:center;
        color:#91a1b1;
    }

    .growth-table .category {
        color:#385873;
        font-weight:550;
    }

    .positive {
        color:#159a63 !important;
        font-weight:750 !important;
        white-space:nowrap;
    }

    .negative {
        color:#e5484d !important;
        font-weight:750 !important;
        white-space:nowrap;
    }

    .neutral {
        color:#8796a5 !important;
        white-space:nowrap;
    }

    .normal {
        color:#40566d !important;
        white-space:nowrap;
    }

    .chart-card {
        background:white;
        border:1px solid #dce6f0;
        border-radius:15px;
        padding:8px;
        box-shadow:0 4px 15px rgba(24,65,105,.04);
    }

    .small-note {
        color:#8aa0b5;
        font-size:11px;
    }

    div[data-testid="stRadio"] > div {
        gap:5px;
    }

    .top5-grid { display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-top:8px; margin-bottom:8px; }
    .top5-card { background:#fff; border:1px solid #dbe6f0; border-radius:12px; padding:13px 14px 12px; box-shadow:0 3px 12px rgba(24,65,105,.05); }
    .top5-title { color:#063b78; font-size:15px; font-weight:800; margin-bottom:10px; }
    .top5-row { display:grid; grid-template-columns:24px minmax(150px,1fr) minmax(120px,1.7fr) 58px; align-items:center; gap:8px; min-height:22px; margin:3px 0; }
    .top5-rank { width:21px; height:21px; line-height:21px; text-align:center; border-radius:50%; background:#eaf2fb; color:#0a4b91; font-size:11px; font-weight:800; }
    .top5-name { color:#31516e; font-size:11px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
    .top5-bar-wrap { height:10px; background:#e9f0f7; border-radius:6px; overflow:hidden; }
    .top5-bar { height:100%; border-radius:6px; min-width:8px; }
    .topbar-blue { background:linear-gradient(90deg,#8bc5f3,#0b4d91); }
    .topbar-green { background:linear-gradient(90deg,#9fd9c4,#39b97a); }
    .top5-value { color:#0a4b91; font-size:11px; font-weight:800; text-align:right; }
    .top5-empty { color:#8799aa; font-size:12px; padding:8px 0; }
    .dashboard-footer { display:flex; justify-content:space-between; gap:20px; color:#8194a8; font-size:10px; padding:7px 3px 0; }
    @media (max-width:900px) { .top5-grid{grid-template-columns:1fr;} .top5-row{grid-template-columns:24px minmax(120px,1fr) minmax(80px,1fr) 58px;} .dashboard-footer{flex-direction:column;gap:3px;} }

</style>
""", unsafe_allow_html=True)

# ============================================================
# UTILITAS
# ============================================================
def norm(x):
    return str(x).strip().lower().replace("\n"," ").replace("_"," ")

def num(x):
    if pd.isna(x):
        return np.nan
    s = str(x).strip()
    if s in ("", "-", "—", "nan", "None"):
        return np.nan
    s = s.replace("%","").replace(" ","")
    # Data Google Sheet Indonesia dapat berupa 1.383 atau 12,34
    if "," in s:
        s = s.replace(".","").replace(",",".")
    else:
        # Jangan mengubah angka desimal yang memakai titik
        s = s.replace(",","")
    try:
        return float(s)
    except:
        return np.nan

def pct(x):
    if pd.isna(x):
        return "—"
    return f"{float(x):.2f}%"

def money(x):
    if pd.isna(x):
        return "—"
    return f"{float(x):,.2f}"

def integer(x):
    if pd.isna(x):
        return "—"
    return f"{int(round(float(x))):,}".replace(",", ".")

def gviz_url(sheet_name):
    return (
        f"https://docs.google.com/spreadsheets/d/"
        f"{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    )

@st.cache_data(ttl=300, show_spinner=False)
def read_sheet(sheet_name):
    url = gviz_url(sheet_name)
    try:
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        return pd.read_csv(StringIO(r.text))
    except Exception:
        return pd.DataFrame()

# ============================================================
# BACA SHEET
# ============================================================
s1 = read_sheet("Sheet1")
s3 = read_sheet("Sheet3")
s4 = read_sheet("Sheet4")

# ============================================================
# PARSING SHEET1
# Struktur screenshot:
# A ID, B Triwulan, C Tahun, D Periode, E Parameter,
# F IKE BEI, G PMI, H IKBM, I QtQ, J YoY, K CtoC
# ============================================================
def parse_sheet1(df):
    if df.empty:
        return pd.DataFrame()

    cols = {norm(c): c for c in df.columns}

    def find(*names):
        for n in names:
            if n in cols:
                return cols[n]
        return None

    p = find("periode")
    year = find("tahun")
    q = find("triwulan")
    ike = find("ike bei")
    pmi = find("pmi")
    ikbm = find("ikbm")
    qtoq = find("qtoq")
    yoy = find("yoy")
    ctoc = find("ctoc")

    # Jika kolom periode tidak terdeteksi, cari kolom berdasarkan posisi
    if p is None and len(df.columns) >= 4:
        p = df.columns[3]

    out = pd.DataFrame()
    out["periode"] = df[p].astype(str).str.strip().str.upper() if p else ""
    out["tahun"] = pd.to_numeric(df[year], errors="coerce") if year else np.nan
    out["triwulan"] = df[q].astype(str).str.strip().str.upper() if q else ""

    # Jika tahun/triwulan kosong, ambil dari periode
    out["tahun"] = out["tahun"].fillna(
        pd.to_numeric(out["periode"].str[:4], errors="coerce")
    )
    out["triwulan"] = out["triwulan"].replace(
        {"NAN":np.nan,"NONE":np.nan}
    )
    out["triwulan"] = out["triwulan"].fillna(
        out["periode"].str[-2:].str.upper()
    )

    out["ike_bei"] = df[ike].map(num) if ike else np.nan
    out["pmi"] = df[pmi].map(num) if pmi else np.nan
    out["ikbm"] = df[ikbm].map(num) if ikbm else np.nan
    out["qtoq"] = df[qtoq].map(num) if qtoq else np.nan
    out["yoy"] = df[yoy].map(num) if yoy else np.nan
    out["ctoc"] = df[ctoc].map(num) if ctoc else np.nan

    # Hilangkan baris tanpa periode
    out = out[out["periode"].ne("") & out["periode"].ne("NAN")].copy()

    # Hanya satu baris per periode
    out = out.drop_duplicates("periode", keep="last")

    # Urut kronologis
    out["_sort"] = (
        pd.to_numeric(out["tahun"], errors="coerce").fillna(0) * 10
        + out["triwulan"].astype(str).str.extract(r"([1-4])")[0].fillna("0").astype(int)
    )
    out = out.sort_values("_sort").drop(columns="_sort")

    return out

indicator = parse_sheet1(s1)

# ============================================================
# PARSING SHEET3
# Struktur screenshot:
# A ID, B Triwulan, C Tahun, D Periode, E Parameter, F Data
# ============================================================
def parse_sheet3(df):
    if df.empty:
        return pd.DataFrame()

    cols = {norm(c): c for c in df.columns}

    def find(*names):
        for n in names:
            if n in cols:
                return cols[n]
        return None

    p = find("periode")
    param = find("parameter")
    data = find("data")
    year = find("tahun")
    q = find("triwulan")

    if not all([p, param, data]):
        return pd.DataFrame()

    out = pd.DataFrame()
    out["periode"] = df[p].astype(str).str.strip().str.upper()
    out["parameter"] = df[param].astype(str).str.strip().str.lower()
    out["data"] = df[data].map(num)

    def target(x):
        x = norm(x)
        if "total pendapatan" in x or "total pendapata" in x:
            return "total_pendapatan"
        if "jumlah perusah" in x or x == "perusahaan":
            return "jumlah_perusahaan"
        return None

    out["target"] = out["parameter"].map(target)
    out = out[out["target"].notna()].copy()

    if out.empty:
        return pd.DataFrame()

    wide = (
        out.pivot_table(
            index="periode",
            columns="target",
            values="data",
            aggfunc="last"
        )
        .reset_index()
    )

    for c in ["total_pendapatan","jumlah_perusahaan"]:
        if c not in wide.columns:
            wide[c] = np.nan

    return wide

kpi = parse_sheet3(s3)

# ============================================================
# PARSING SHEET4
# Struktur screenshot:
# Periode, Kode, Kategori, Kontribusi, YoY, QtoQ, CtoC,
# Jumlah perusahaan
# ============================================================
def parse_sheet4(df):
    if df.empty:
        return pd.DataFrame()

    cols = {norm(c): c for c in df.columns}

    def find(*names):
        for n in names:
            if n in cols:
                return cols[n]
        return None

    p = find("periode")
    cat = find("kategori")
    kon = find("kontribusi")
    yoy = find("yoy")
    qtoq = find("qtoq", "qtoq")
    ctoc = find("ctoc")
    company = find("jumlah perusahaan", "jumlah perusaha")

    if not p or not cat:
        return pd.DataFrame()

    out = pd.DataFrame()
    out["periode"] = df[p].astype(str).str.strip().str.upper()
    out["kategori"] = df[cat].astype(str).str.strip()
    out["kontribusi"] = df[kon].map(num) if kon else np.nan
    out["yoy"] = df[yoy].map(num) if yoy else np.nan
    out["qtoq"] = df[qtoq].map(num) if qtoq else np.nan
    out["ctoc"] = df[ctoc].map(num) if ctoc else np.nan
    out["jumlah_perusahaan"] = df[company].map(num) if company else np.nan

    out = out[out["kategori"].notna()].copy()
    return out

category = parse_sheet4(s4)

# ============================================================
# GABUNGAN DATA
# ============================================================
dashboard = indicator.copy()

if not dashboard.empty:
    dashboard["periode"] = dashboard["periode"].astype(str).str.strip().str.upper()

    if not kpi.empty:
        kpi["periode"] = kpi["periode"].astype(str).str.strip().str.upper()
        dashboard = dashboard.merge(kpi, on="periode", how="left")
    else:
        dashboard["total_pendapatan"] = np.nan
        dashboard["jumlah_perusahaan"] = np.nan

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown('<div class="brand">iDEA↗</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="brand-sub">IDX Economic & Earnings Analytics</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="side-title">Dashboard IDX Analytics</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="side-sub">Kinerja Perusahaan Tercatat Bursa Efek Indonesia</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### Menu")

    menu = st.radio(
        "Menu",
        ["🏠 Home", "📊 Analisis", "ℹ️ Metadata", "📁 Data"],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("### 📅 Filter Periode")

    if not dashboard.empty:
        years = sorted(
            pd.to_numeric(dashboard["tahun"], errors="coerce")
            .dropna()
            .astype(int)
            .unique()
            .tolist()
        )
    else:
        years = []

    if not years:
        years = [2025, 2026]

    selected_year = st.selectbox(
        "Tahun",
        years,
        index=len(years)-1
    )

    quarters = ["Semua", "Q1", "Q2", "Q3", "Q4"]
    selected_quarter = st.selectbox(
        "Triwulan",
        quarters,
        index=0
    )

    st.markdown(
        "<div class='small-note'>"
        "Filter digunakan untuk KPI dan ringkasan kategori."
        "</div>",
        unsafe_allow_html=True
    )

    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# ============================================================
# FILTER DATA
# ============================================================
def filter_dashboard(df):
    if df.empty:
        return df

    x = df.copy()
    x["tahun_num"] = pd.to_numeric(x["tahun"], errors="coerce")

    x = x[x["tahun_num"].eq(selected_year)]

    if selected_quarter != "Semua":
        x = x[
            x["triwulan"].astype(str).str.upper().eq(selected_quarter)
        ]

    return x.drop(columns="tahun_num", errors="ignore")

def filter_category(df):
    if df.empty:
        return df

    x = df.copy()
    x = x[
        x["periode"].str.startswith(str(selected_year))
    ]

    if selected_quarter != "Semua":
        x = x[
            x["periode"].str.endswith(selected_quarter)
        ]

    return x

current = filter_dashboard(dashboard)
cf = filter_category(category)

# ============================================================
# NILAI KPI
# ============================================================
if not current.empty:
    r = current.iloc[-1]

    total = r.get("total_pendapatan", np.nan)
    perusahaan = r.get("jumlah_perusahaan", np.nan)
    ike = r.get("ike_bei", np.nan)
    yoy = r.get("yoy", np.nan)
    qtoq = r.get("qtoq", np.nan)
    ctoc = r.get("ctoc", np.nan)

    active_period = r.get("periode", "—")
else:
    total = perusahaan = ike = yoy = qtoq = ctoc = np.nan
    active_period = f"{selected_year}{selected_quarter if selected_quarter != 'Semua' else ''}"

# ============================================================
# HOME
# ============================================================
if menu == "🏠 Home":

    st.markdown("""
    <div class="hero">
        <div class="hero-kicker">iDEA • IDX ECONOMIC & EARNINGS ANALYTICS</div>
        <div class="hero-title">Dashboard IDX Analytics</div>
        <div class="hero-sub">
            Kinerja Perusahaan Tercatat Bursa Efek Indonesia
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ========================================================
    # PERKEMBANGAN INDIKATOR & PERTUMBUHAN PENDAPATAN
    # Dipindahkan ke HOME sesuai desain dashboard.
    # ========================================================
    st.markdown(
        '<div class="section-title">📈 Perkembangan Indikator</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="section-sub">Perbandingan IKE BEI, PMI dan IKBM per triwulan. Data kosong diabaikan.</div>',
        unsafe_allow_html=True
    )

    chart_df = dashboard.copy()
    if not chart_df.empty:
        long_ind = chart_df[["periode","ike_bei","pmi","ikbm"]].melt(
            id_vars="periode", var_name="indikator", value_name="nilai"
        ).dropna(subset=["nilai"])

        label_map = {"ike_bei":"IKE BEI", "pmi":"PMI", "ikbm":"IKBM"}
        long_ind["indikator"] = long_ind["indikator"].map(label_map)

        fig = px.line(long_ind, x="periode", y="nilai", color="indikator", markers=True)
        fig.update_traces(line=dict(width=3), marker=dict(size=8))
        fig.update_layout(
            height=430, xaxis_title="Periode", yaxis_title="Indeks",
            hovermode="x unified", paper_bgcolor="white", plot_bgcolor="white",
            margin=dict(l=35,r=30,t=25,b=45),
            legend=dict(orientation="h", y=1.08, x=0)
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

        st.markdown(
            '<div class="section-title">📈 Pertumbuhan Pendapatan</div>',
            unsafe_allow_html=True
        )
        growth_df = chart_df[chart_df["periode"].astype(str) >= "2025Q4"].copy()
        growth_cols = [("qtoq","Pertumbuhan Pendapatan (QtQ)"), ("yoy","Pertumbuhan Pendapatan (YoY)"), ("ctoc","Pertumbuhan Pendapatan (CtoC)")]
        gc = st.columns(3)

        for idx, (col, title) in enumerate(growth_cols):
            with gc[idx]:
                x = growth_df[["periode", col]].dropna()
                fig = go.Figure()
                if not x.empty:
                    fig.add_trace(go.Scatter(
                        x=x["periode"], y=x[col], mode="lines+markers+text",
                        text=[f"{v:.2f}%" for v in x[col]], textposition="top center",
                        line=dict(width=3), marker=dict(size=8),
                        hovertemplate="%{x}<br>%{y:.2f}%<extra></extra>"
                    ))
                fig.add_hline(y=0, line_dash="dot", line_width=1)
                fig.update_layout(
                    title=dict(text=title, font=dict(size=15)), height=320,
                    xaxis_title="", yaxis_title="", paper_bgcolor="white",
                    plot_bgcolor="white", margin=dict(l=20,r=20,t=55,b=35), showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

# ============================================================
# ANALISIS
# ============================================================
elif menu == "📊 Analisis":

    st.markdown("""
    <div class="hero">
        <div class="hero-kicker">ANALISIS EMITEN</div>
        <div class="hero-title">🏆 Analisis Kontributor & Pertumbuhan</div>
        <div class="hero-sub">
            Melihat kategori dengan kontribusi pendapatan dan pertumbuhan YoY tertinggi.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        f'<div class="period-badge">📅 Periode aktif: {active_period}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">📌 Ringkasan Kinerja</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-sub">'
        'Ringkasan kinerja perusahaan tercatat berdasarkan filter periode di sidebar.'
        '</div>',
        unsafe_allow_html=True
    )

    kpis = [
        ("💰", "Total Pendapatan", money(total), "Rp ribu triliun"),
        ("📈", "IKE BEI", money(ike), "indeks"),
        ("🏢", "Jumlah Perusahaan", integer(perusahaan), "perusahaan"),
        ("↗️", "Pertumbuhan YoY", pct(yoy), "year-on-year"),
        ("⚡", "Pertumbuhan QtQ", pct(qtoq), "quarter-on-quarter"),
        ("📊", "Pertumbuhan CtoC", pct(ctoc), "cumulative"),
    ]

    cols = st.columns(3)

    for i, (icon, label, value, note) in enumerate(kpis):
        with cols[i % 3]:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-label">{icon} {label}</div>
                    <div class="kpi-value">{value}</div>
                    <div class="kpi-note">{note}</div>
                </div>
                """,
                unsafe_allow_html=True
            )


    st.markdown(
        '<div class="section-title">🏆 Top 5 Kategori</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="section-sub">Kategori mengikuti filter tahun dan triwulan di sidebar.</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">🧩 Ringkasan Kategori</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-sub">'
        'Kontribusi dan pertumbuhan menurut kategori usaha.'
        '</div>',
        unsafe_allow_html=True
    )

    if not cf.empty:

        # Satu baris per kategori
        cf2 = (
            cf.sort_values("kontribusi", ascending=False)
              .drop_duplicates("kategori")
              .copy()
        )

        left, right = st.columns([1, 1.45], gap="large")

        # ----------------------------------------------------
        # TREEMAP
        # ----------------------------------------------------
        with left:
            st.markdown(
                '<div style="font-size:18px;font-weight:750;'
                'color:#173e68;margin-bottom:8px;">'
                'Kontribusi menurut Kategori'
                '</div>',
                unsafe_allow_html=True
            )

            tree = (
                cf2[["kategori", "kontribusi"]]
                .dropna()
                .sort_values("kontribusi", ascending=False)
            )

            if not tree.empty:
                # Palet warna bertingkat seperti contoh: biru tua untuk kontribusi
                # terbesar, lalu biru muda/teal/ungu untuk kategori berikutnya.
                # Warna dibuat per kategori agar setiap kotak mudah dibedakan.
                palette = [
                    "#0B4A87", "#2F80C9", "#73B7E8", "#4FC3C1",
                    "#86C9B0", "#B7DDBF", "#D8C9F2", "#C9DFF0",
                    "#E2EAF3", "#DDE7F0", "#EEF3F8"
                ]
                color_map = {
                    cat: palette[i % len(palette)]
                    for i, cat in enumerate(tree["kategori"].tolist())
                }

                fig = px.treemap(
                    tree,
                    path=["kategori"],
                    values="kontribusi",
                    color="kategori",
                    color_discrete_map=color_map
                )

                fig.update_traces(
                    texttemplate="<b>%{label}</b><br><b>%{value:.2f}%</b>",
                    textfont=dict(size=13, color="#0B315E"),
                    marker=dict(
                        line=dict(width=2, color="white")
                    ),
                    hovertemplate="<b>%{label}</b><br>Kontribusi: %{value:.2f}%<extra></extra>",
                    tiling=dict(packing="squarify", pad=2)
                )

                # Kotak terbesar berada di kiri seperti desain referensi.
                fig.update_layout(
                    height=455,
                    margin=dict(l=4, r=4, t=4, b=4),
                    showlegend=False,
                    paper_bgcolor="white",
                    plot_bgcolor="white",
                    uniformtext=dict(minsize=9, mode="hide")
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                    config={"displayModeBar": False}
                )

        # ----------------------------------------------------
        # TABEL PERTUMBUHAN BERWARNA
        # ----------------------------------------------------
        with right:

            st.markdown(
                '<div style="font-size:18px;font-weight:750;'
                'color:#173e68;margin-bottom:8px;">'
                'Tabel Pertumbuhan menurut Kategori'
                '</div>',
                unsafe_allow_html=True
            )

            def fmt_growth(x):
                if pd.isna(x):
                    return '<span class="neutral">–</span>'
                x = float(x)
                if x > 0:
                    return f'<span class="positive">▲ {x:.2f}%</span>'
                if x < 0:
                    return f'<span class="negative">▼ {abs(x):.2f}%</span>'
                return '<span class="neutral">–</span>'

            def fmt_normal(x):
                if pd.isna(x):
                    return '<span class="neutral">–</span>'
                return f'<span class="normal">{float(x):.2f}%</span>'

            rows = ""
            for i, (_, row) in enumerate(cf2.iterrows(), start=1):
                rows += f"""
                <tr>
                    <td class="num">{i}</td>
                    <td class="category">{row['kategori']}</td>
                    <td>{fmt_normal(row['kontribusi'])}</td>
                    <td>{fmt_growth(row['yoy'])}</td>
                    <td>{fmt_growth(row['qtoq'])}</td>
                    <td>{fmt_growth(row['ctoc'])}</td>
                </tr>
                """

            table_html = f"""
            <style>
                * {{ box-sizing: border-box; }}
                body {{ margin:0; font-family: Arial, sans-serif; background:transparent; }}
                .wrap {{
                    width:100%; background:#fff; border:1px solid #d9e3ed;
                    border-radius:11px; overflow:hidden;
                    box-shadow:0 2px 9px rgba(20,60,100,.04);
                }}
                .scroll {{ max-height:470px; overflow-y:auto; }}
                table {{ width:100%; border-collapse:collapse; font-size:12.5px; }}
                th {{
                    position:sticky; top:0; z-index:2; text-align:left;
                    background:#eaf2fa; color:#526b84; font-weight:700;
                    padding:10px 9px; border-bottom:1px solid #d5e0eb;
                }}
                td {{
                    padding:9px; border-bottom:1px solid #e7edf3;
                    color:#40566d; background:#fff;
                }}
                tr:hover td {{ background:#f7fbff; }}
                .num {{ width:30px; text-align:center; color:#91a1b1; }}
                .category {{ color:#385873; font-weight:550; }}
                .positive {{ color:#159a63; font-weight:750; white-space:nowrap; }}
                .negative {{ color:#e5484d; font-weight:750; white-space:nowrap; }}
                .neutral {{ color:#8796a5; white-space:nowrap; }}
                .normal {{ color:#40566d; white-space:nowrap; }}
            </style>
            <div class="wrap">
                <div class="scroll">
                    <table>
                        <thead>
                            <tr>
                                <th style="width:30px">#</th>
                                <th style="width:34%">Kategori</th>
                                <th>Kontribusi</th>
                                <th>YoY</th>
                                <th>QtQ</th>
                                <th>CtoC</th>
                            </tr>
                        </thead>
                        <tbody>{rows}</tbody>
                    </table>
                </div>
            </div>
            """

            components.html(table_html, height=min(520, 58 + (len(cf2) * 38)), scrolling=False)

        # ----------------------------------------------------
        # JUMLAH PERUSAHAAN
        # ----------------------------------------------------
        st.markdown(
            '<div class="section-title" style="font-size:21px;">'
            '🏢 Jumlah Perusahaan menurut Kategori'
            '</div>',
            unsafe_allow_html=True
        )

        comp = (
            cf2[["kategori","jumlah_perusahaan"]]
            .dropna()
            .sort_values("jumlah_perusahaan", ascending=False)
        )

        if not comp.empty:
            fig = px.bar(
                comp,
                x="kategori",
                y="jumlah_perusahaan",
                text="jumlah_perusahaan"
            )

            fig.update_traces(
                texttemplate="%{text:.0f}",
                textposition="outside"
            )

            fig.update_layout(
                height=390,
                xaxis_title="",
                yaxis_title="Jumlah Perusahaan",
                margin=dict(l=25,r=20,t=20,b=95),
                plot_bgcolor="white",
                paper_bgcolor="white",
                xaxis=dict(tickangle=-30),
                showlegend=False
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": False}
            )

    else:
        st.warning(
            "Data Sheet4 tidak tersedia untuk periode yang dipilih."
        )


    # --------------------------------------------------------
    # TOP 5 KONTRIBUTOR & TOP 5 PERTUMBUHAN YoY
    # --------------------------------------------------------
    st.markdown(
        '<div class="section-title">🏆 Kontributor & Pertumbuhan Teratas</div>',
        unsafe_allow_html=True
    )

    if not cf.empty:
        rank_df = cf.sort_values("kontribusi", ascending=False).drop_duplicates("kategori").copy()
        top_contrib = rank_df.dropna(subset=["kontribusi"]).head(5).copy()
        top_yoy = (cf.drop_duplicates("kategori").dropna(subset=["yoy"])
                     .sort_values("yoy", ascending=False).head(5).copy())

        max_contrib = float(top_contrib["kontribusi"].max()) if not top_contrib.empty else 1
        max_yoy = float(top_yoy["yoy"].max()) if not top_yoy.empty else 1
        if max_contrib <= 0: max_contrib = 1
        if max_yoy <= 0: max_yoy = 1

        def make_top5_rows(data, value_col, max_value, bar_class):
            rows = []
            for rank, (_, rr) in enumerate(data.iterrows(), 1):
                name = str(rr.get("kategori", "-"))
                value = pd.to_numeric(rr.get(value_col), errors="coerce")
                if pd.isna(value):
                    continue
                width = max(8, min(100, float(value) / max_value * 100))
                rows.append(
                    f'<div class="top5-row">'
                    f'<div class="top5-rank">{rank}</div>'
                    f'<div class="top5-name">{name}</div>'
                    f'<div class="top5-bar-wrap"><div class="top5-bar {bar_class}" style="width:{width:.1f}%"></div></div>'
                    f'<div class="top5-value">{value:.2f}%</div>'
                    f'</div>'
                )
            return ''.join(rows) or '<div class="top5-empty">Data belum tersedia.</div>'

        left = make_top5_rows(top_contrib, "kontribusi", max_contrib, "topbar-blue")
        right = make_top5_rows(top_yoy, "yoy", max_yoy, "topbar-green")

        st.markdown(
            f'<div class="top5-grid">'
            f'<div class="top5-card"><div class="top5-title">🏆 Top 5 Kontributor Pendapatan</div>{left}</div>'
            f'<div class="top5-card"><div class="top5-title">📈 Top 5 Pertumbuhan YoY</div>{right}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="dashboard-footer">'
            '<span>Sumber: Laporan Keuangan Emiten BEI (diolah)</span>'
            '<span>🟢 Data mengikuti periode/filter yang dipilih</span>'
            '</div>',
            unsafe_allow_html=True
        )


# ============================================================
# METADATA
# ============================================================
elif menu == "ℹ️ Metadata":

    st.markdown("""
    <div class="hero">
        <div class="hero-kicker">INFORMASI METADATA</div>
        <div class="hero-title">ℹ️ Definisi Indikator</div>
        <div class="hero-sub">
            Penjelasan indikator yang digunakan dalam Dashboard IDX Analytics.
        </div>
    </div>
    """, unsafe_allow_html=True)

    definitions = [
        ("Total Pendapatan",
         "Total pendapatan perusahaan tercatat pada periode yang dipilih."),
        ("Jumlah Perusahaan",
         "Jumlah perusahaan tercatat yang tercakup dalam data pada periode yang dipilih."),
        ("IKE BEI",
         "Indikator kinerja ekonomi perusahaan tercatat Bursa Efek Indonesia."),
        ("PMI",
         "Purchasing Managers' Index sebagai indikator aktivitas sektor manufaktur."),
        ("IKBM",
         "Indikator ekonomi yang digunakan dalam dashboard sesuai sumber data."),
        ("QoQ",
         "Pertumbuhan dibandingkan dengan triwulan sebelumnya."),
        ("YoY",
         "Pertumbuhan dibandingkan dengan periode yang sama pada tahun sebelumnya."),
        ("CtoC",
         "Pertumbuhan kumulatif dibandingkan periode kumulatif yang relevan.")
    ]

    for title, desc in definitions:
        st.markdown(
            f"""
            <div style="
                background:white;
                border:1px solid #dce6f0;
                border-radius:13px;
                padding:17px 20px;
                margin-bottom:10px;
                box-shadow:0 3px 12px rgba(24,65,105,.04);
            ">
                <div style="
                    color:#063b78;
                    font-weight:800;
                    font-size:15px;
                    margin-bottom:5px;
                ">
                    {title}
                </div>
                <div style="
                    color:#71869a;
                    font-size:13px;
                    line-height:1.5;
                ">
                    {desc}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# ============================================================
# DATA
# ============================================================
#else:
    
 #   st.markdown("""
 #   <div class="hero">
 #       <div class="hero-kicker">DATA SOURCE</div>
 #       <div class="hero-title">📁 Data Dashboard</div>
 #       <div class="hero-sub">
 #           Data dibaca langsung dari Google Sheets.
 #       </div>
 #   </div>
 #   """, unsafe_allow_html=True)
#
 #   st.success(
 #       "🟢 Data terhubung ke Google Sheets secara langsung."
 #   )

  #  st.markdown("### Status sumber data")

  #  c1, c2, c3 = st.columns(3)

#    with c1:
 #       st.metric("Sheet1", f"{len(s1):,} baris")
#
#    with c2:
#        st.metric("Sheet3", f"{len(s3):,} baris")

#    with c3:
#        st.metric("Sheet4", f"{len(s4):,} baris")

#    st.markdown("### Preview Sheet1")

 #   if not s1.empty:
#        st.dataframe(
#            s1,
#            use_container_width=True,
#            hide_index=True
#        )
#    else:
#        st.error("Sheet1 tidak dapat dibaca.")

#    st.markdown("### Preview Sheet3")

#    if not s3.empty:
#        st.dataframe(
#            s3,
#            use_container_width=True,
#            hide_index=True
#        )
#    else:
#        st.error("Sheet3 tidak dapat dibaca.")

#    st.markdown("### Preview Sheet4")

#    if not s4.empty:
#        st.dataframe(
#            s4,
 #           use_container_width=True,
#            hide_index=True
#        )
#    else:
#        st.error("Sheet4 tidak dapat dibaca.")

# ============================================================
# FOOTER / STATUS
# ============================================================
st.markdown(
    """
    <div style="
        margin-top:35px;
        padding-top:14px;
        border-top:1px solid #dce5ee;
        color:#8da0b2;
        font-size:11px;
        text-align:center;
    ">
        iDEA • IDX Economic & Earnings Analytics
    </div>
    """,
    unsafe_allow_html=True
)
