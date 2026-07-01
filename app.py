import base64
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Dashboard Curah Hujan KMP1 - KARYAMAS PLANTATION",
    page_icon="🌴",
    layout="wide",
    initial_sidebar_state="expanded",
)

APP_DIR = Path(__file__).resolve().parent
DEFAULT_EXCEL = APP_DIR / "DATA CURAH HUJAN KMP1(4).xlsx"

MONTH_ORDER = ["April", "Mei", "Juni"]
MONTH_MAP = {4: "April", 5: "Mei", 6: "Juni"}
WEEK_ORDER = ["W1", "W2", "W3", "W4"]


def palm_svg_data_uri() -> str:
    svg = """
    <svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1200 720'>
      <defs>
        <linearGradient id='g' x1='0' x2='1' y1='0' y2='1'>
          <stop offset='0' stop-color='#051512'/><stop offset='1' stop-color='#102820'/>
        </linearGradient>
        <filter id='blur'><feGaussianBlur stdDeviation='1.2'/></filter>
      </defs>
      <rect width='1200' height='720' fill='url(#g)'/>
      <g opacity='.18' fill='none' stroke='#52d273' stroke-width='10' stroke-linecap='round' filter='url(#blur)'>
        <path d='M965 705 C925 520 930 360 1018 190'/>
        <path d='M1018 190 C945 208 890 240 835 300'/>
        <path d='M1018 190 C956 148 885 130 795 145'/>
        <path d='M1018 190 C1075 128 1130 95 1190 80'/>
        <path d='M1018 190 C1110 188 1160 225 1198 280'/>
        <path d='M1018 190 C1010 105 1038 48 1090 10'/>
        <path d='M210 725 C185 565 205 430 285 295'/>
        <path d='M285 295 C215 315 150 355 90 420'/>
        <path d='M285 295 C235 245 165 222 72 232'/>
        <path d='M285 295 C340 230 402 190 482 172'/>
        <path d='M285 295 C380 292 452 330 515 398'/>
      </g>
      <g opacity='.10' fill='#a7f3d0'>
        <circle cx='160' cy='120' r='2'/><circle cx='420' cy='80' r='2'/><circle cx='740' cy='160' r='2'/>
        <circle cx='980' cy='90' r='2'/><circle cx='1100' cy='520' r='2'/><circle cx='620' cy='620' r='2'/>
      </g>
    </svg>
    """
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()



def company_logo_data_uri() -> str:
    svg = """
    <svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 620 180'>
      <defs>
        <linearGradient id='lg' x1='0' x2='1' y1='0' y2='1'>
          <stop offset='0' stop-color='#16a34a'/><stop offset='1' stop-color='#0f766e'/>
        </linearGradient>
      </defs>
      <rect width='620' height='180' rx='28' fill='rgba(3,24,20,.92)'/>
      <circle cx='86' cy='90' r='55' fill='url(#lg)'/>
      <path d='M84 134 C77 96 80 67 102 32' stroke='#052e1a' stroke-width='10' fill='none' stroke-linecap='round'/>
      <path d='M101 38 C70 42 49 56 28 82 M101 38 C76 20 49 15 18 20 M101 38 C120 17 144 8 174 6 M101 38 C138 38 164 53 184 80 M101 38 C97 14 107 0 126 -14' stroke='#dcfce7' stroke-width='8' fill='none' stroke-linecap='round'/>
      <text x='165' y='78' fill='#ecfdf5' font-size='34' font-family='Arial, sans-serif' font-weight='800'>KARYAMAS</text>
      <text x='166' y='119' fill='#a7f3d0' font-size='30' font-family='Arial, sans-serif' font-weight='700'>PLANTATION</text>
      <text x='168' y='148' fill='#86efac' font-size='16' font-family='Arial, sans-serif'>Rainfall Monitoring Dashboard</text>
    </svg>
    """
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()

def inject_css() -> None:
    bg = palm_svg_data_uri()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(2, 6, 6, .78), rgba(2, 6, 6, .90)), url('{bg}');
            background-size: cover;
            background-attachment: fixed;
        }}
        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, rgba(8, 28, 24, .96), rgba(4, 17, 15, .96));
            border-right: 1px solid rgba(129, 230, 217, .18);
        }}
        .hero {{
            padding: 22px 26px;
            border-radius: 22px;
            background: linear-gradient(135deg, rgba(15, 118, 110, .32), rgba(34, 197, 94, .12));
            border: 1px solid rgba(167, 243, 208, .22);
            box-shadow: 0 18px 45px rgba(0,0,0,.26);
            margin-bottom: 14px;
        }}
        .hero-inner {{ display: flex; align-items: center; gap: 22px; }}
        .company-logo {{ width: 215px; min-width: 190px; filter: drop-shadow(0 10px 18px rgba(0,0,0,.28)); }}
        .hero h1 {{ margin: 0; font-size: 34px; color: #ecfdf5; font-weight: 900; }}
        .hero p {{ margin: 8px 0 0; color: #b7f7d0; font-size: 15px; }}
        .metric-card {{
            padding: 15px 16px;
            border-radius: 18px;
            background: rgba(3, 24, 20, .78);
            border: 1px solid rgba(45, 212, 191, .18);
        }}
        .metric-card {{ display: flex; align-items: center; gap: 12px; min-height: 88px; }}
        .metric-icon {{ font-size: 30px; width: 46px; height: 46px; display:flex; align-items:center; justify-content:center; border-radius: 15px; background: rgba(20, 184, 166, .16); }}
        .metric-label {{ color: #9de8c5; font-size: 13px; }}
        .metric-value {{ color: #ffffff; font-size: 27px; font-weight: 800; }}
        .chart-title {{ font-size: 18px; font-weight: 900; color: #ecfdf5; margin: 18px 0 18px 0; padding-top: 8px; }}
        div[data-testid="stDataFrame"] {{ border: 1px solid rgba(167, 243, 208, .12); border-radius: 16px; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data(show_spinner=False)
def load_data(uploaded_file=None) -> pd.DataFrame:
    source = uploaded_file if uploaded_file is not None else DEFAULT_EXCEL
    raw = pd.read_excel(source, header=None)
    header_idx = raw.index[raw.apply(lambda r: r.astype(str).str.contains("Estate", case=False, na=False).any(), axis=1)][0]
    df = pd.read_excel(source, header=header_idx)
    df = df.rename(columns=lambda c: str(c).strip())
    rename = {
        "Document No": "Document No",
        "Document number": "Document No",
        "Document Date": "Document Date",
        "User Name": "User Name",
        "quantity": "quantity",
        "UM": "UM",
        "Divisi": "Divisi",
        "Estate": "Estate",
    }
    df = df.rename(columns=rename)
    keep = [c for c in ["Document Date", "Estate", "Divisi", "Document No", "StatKF", "Object number", "quantity", "UM", "Created on", "Time", "User Name"] if c in df.columns]
    df = df[keep].copy()
    df["Document Date"] = pd.to_datetime(df["Document Date"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0)
    df["Estate"] = df["Estate"].astype(str).str.strip()
    df["Divisi"] = df["Divisi"].astype(str).str.strip()
    df["UM"] = df["UM"].fillna("MM").astype(str).str.strip()
    df = df.dropna(subset=["Document Date", "Estate", "Divisi"])
    df = df[df["Estate"].ne("") & df["Divisi"].ne("")]
    df["Bulan"] = df["Document Date"].dt.month.map(MONTH_MAP)
    df["Bulan"] = pd.Categorical(df["Bulan"], categories=MONTH_ORDER, ordered=True)
    day = df["Document Date"].dt.day
    df["Minggu"] = pd.cut(day, bins=[0, 7, 14, 21, 31], labels=WEEK_ORDER, include_lowest=True)
    return df.sort_values(["Document Date", "Estate", "Divisi"])


def status_hujan(mm: float) -> str:
    if mm < 100:
        return "Kering"
    if mm <= 300:
        return "Normal"
    return "Tinggi"


def status_icon(status: str) -> str:
    return {"Kering": "🟠", "Normal": "🟢", "Tinggi": "🔵"}.get(status, "⚪")


def plotly_layout(fig, height=280):
    fig.update_layout(
        height=height,
        template="plotly_dark",
        margin=dict(l=10, r=10, t=20, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        title_font=dict(size=18),
    )
    return fig


inject_css()

df = load_data()

logo_uri = company_logo_data_uri()
st.markdown(
    f"""
    <div class="hero">
      <div class="hero-inner">
        <img class="company-logo" src="{logo_uri}" />
        <div>
          <h1>🌴 Dashboard Curah Hujan KMP1 - KARYAMAS PLANTATION</h1>
          <p>Pencarian Estate, Divisi, dan rentang Document Date dengan grafik mingguan, bulanan, tren, hari hujan, ranking, dan status kondisi.</p>
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("## 📋 Menu Informasi")
    menu = st.radio(
        "Pilih tampilan",
        ["Ringkasan Dashboard", "Informasi Lengkap", "Ranking & Status", "Tentang Data"],
        label_visibility="collapsed",
    )

estates = sorted(df["Estate"].dropna().unique().tolist())
divisions = sorted(df["Divisi"].dropna().unique().tolist())
min_date = df["Document Date"].min().date()
max_date = df["Document Date"].max().date()

st.markdown("### 🔎 Menu Pencarian")
col1, col2, col3, col4 = st.columns([1.2, 1.2, 1.1, 1.1])
with col1:
    selected_estates = st.multiselect("Estate", estates, default=estates)
with col2:
    selected_divisions = st.multiselect("Divisi", divisions, default=divisions)
with col3:
    start_date = st.date_input("Document Date mulai", min_date, min_value=min_date, max_value=max_date)
with col4:
    end_date = st.date_input("Document Date akhir", max_date, min_value=min_date, max_value=max_date)

if start_date > end_date:
    st.error("Tanggal mulai tidak boleh lebih besar dari tanggal akhir.")
    st.stop()

mask = (
    df["Estate"].isin(selected_estates)
    & df["Divisi"].isin(selected_divisions)
    & (df["Document Date"].dt.date >= start_date)
    & (df["Document Date"].dt.date <= end_date)
)
f = df.loc[mask].copy()

m1, m2, m3, m4, m5 = st.columns(5)
total_mm = int(round(f["quantity"].sum())) if len(f) else 0
avg_mm = int(round(f["quantity"].mean())) if len(f) else 0
rain_days = int(f.loc[f["quantity"] > 0, "Document Date"].dt.date.nunique()) if len(f) else 0
no_rain_days = max(0, int(f["Document Date"].dt.date.nunique()) - rain_days) if len(f) else 0
for col, icon, label, value in [
    (m1, "🌧️", "Total Curah Hujan", f"{total_mm:,} MM"),
    (m2, "📊", "Rata-rata", f"{avg_mm:,} MM"),
    (m3, "🏞️", "Jumlah Estate", f"{f['Estate'].nunique():,}"),
    (m4, "🌴", "Jumlah Divisi", f"{f['Divisi'].nunique():,}"),
    (m5, "☔", "Hari Hujan", f"{rain_days:,} hari"),
]:
    col.markdown(
        f"<div class='metric-card'><div class='metric-icon'>{icon}</div><div><div class='metric-label'>{label}</div><div class='metric-value'>{value}</div></div></div>",
        unsafe_allow_html=True,
    )

st.divider()

# Aggregations use the filtered result for interactive dashboard output.
daily = f.groupby(["Estate", "Document Date"], as_index=False)["quantity"].mean()
daily["Bulan"] = daily["Document Date"].dt.month.map(MONTH_MAP)
daily["Bulan"] = pd.Categorical(daily["Bulan"], categories=MONTH_ORDER, ordered=True)
daily["Minggu"] = pd.cut(daily["Document Date"].dt.day, bins=[0, 7, 14, 21, 31], labels=WEEK_ORDER, include_lowest=True)
weekly = daily.groupby(["Estate", "Bulan", "Minggu"], observed=False, as_index=False)["quantity"].mean()
weekly["Periode"] = weekly["Bulan"].astype(str) + "-" + weekly["Minggu"].astype(str)
weekly_order = [f"{m}-{w}" for m in MONTH_ORDER for w in WEEK_ORDER]
weekly["Periode"] = pd.Categorical(weekly["Periode"], categories=weekly_order, ordered=True)

monthly_div = f.groupby(["Estate", "Divisi", "Bulan"], observed=False, as_index=False)["quantity"].sum()
monthly = monthly_div.groupby(["Estate", "Bulan"], observed=False, as_index=False)["quantity"].mean()
monthly["quantity_bulat"] = monthly["quantity"].round(0).astype(int)
monthly["Status"] = monthly["quantity"].apply(status_hujan)
monthly["Status Kondisi"] = monthly["Status"].map(lambda s: f"{status_icon(s)} {s}")

ranking = monthly.groupby("Estate", as_index=False)["quantity"].sum().sort_values("quantity", ascending=False).head(3)
ranking["Curah Hujan"] = ranking["quantity"].round(0).astype(int)

rain_by_day = f.groupby(["Estate", "Document Date"], as_index=False)["quantity"].mean()
rain_by_day["Kategori"] = rain_by_day["quantity"].apply(lambda x: "Hari Hujan" if x > 0 else "Tidak Hujan")
pie_data = rain_by_day.groupby(["Estate", "Kategori"], as_index=False)["Document Date"].nunique().rename(columns={"Document Date": "Jumlah Hari"})

if menu == "Ringkasan Dashboard":
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='chart-title'>Rata-rata Harian Curah Hujan per Estate per Minggu</div>", unsafe_allow_html=True)
        fig = px.line(weekly.sort_values("Periode"), x="Periode", y="quantity", color="Estate", markers=True,
                      labels={"quantity": "Rata-rata MM", "Periode": "Bulan-Minggu"})
        st.plotly_chart(plotly_layout(fig), use_container_width=True)
    with c2:
        st.markdown("<div class='chart-title'>Curah Hujan Rata-rata Bulanan per Estate</div>", unsafe_allow_html=True)
        fig = px.bar(monthly.sort_values("Bulan"), x="Bulan", y="quantity", color="Estate", barmode="group",
                     labels={"quantity": "Rata-rata MM"})
        st.plotly_chart(plotly_layout(fig), use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown("<div class='chart-title'>Trend Curah Hujan Rata-rata per Estate per Bulan</div>", unsafe_allow_html=True)
        fig = px.bar(monthly.sort_values("Bulan"), x="Bulan", y="quantity", color="Estate", barmode="group",
                     labels={"quantity": "Rata-rata MM", "Bulan": "Bulan"})
        st.plotly_chart(plotly_layout(fig), use_container_width=True)
    with c4:
        st.markdown("<div class='chart-title'>Ranking 3 Besar Curah Hujan per Estate</div>", unsafe_allow_html=True)
        fig = px.bar(ranking, x="Estate", y="Curah Hujan", text="Curah Hujan", labels={"Curah Hujan": "MM"})
        st.plotly_chart(plotly_layout(fig), use_container_width=True)

    st.markdown("<div class='chart-title'>Hari Hujan versus Tidak Hujan per Estate</div>", unsafe_allow_html=True)
    pie_estates = sorted(pie_data["Estate"].dropna().unique().tolist())
    for i in range(0, len(pie_estates), 5):
        cols = st.columns(5)
        for col, estate in zip(cols, pie_estates[i:i + 5]):
            with col:
                estate_pie = pie_data[pie_data["Estate"] == estate]
                fig = px.pie(estate_pie, names="Kategori", values="Jumlah Hari", title=f"<b>{estate}</b>")
                st.plotly_chart(plotly_layout(fig, height=260), use_container_width=True)

elif menu == "Informasi Lengkap":
    st.markdown("### 📄 Informasi Lengkap Hasil Pencarian")
    detail_cols = [c for c in ["Document Date", "Estate", "Divisi", "quantity", "UM", "Document No", "StatKF", "Created on", "Time", "User Name"] if c in f.columns]
    show = f[detail_cols].rename(columns={"Estate": "Kebun", "quantity": "Quantity"})
    show["Document Date"] = show["Document Date"].dt.strftime("%Y-%m-%d")
    st.dataframe(show, use_container_width=True, hide_index=True)
    st.download_button("⬇️ Download hasil pencarian CSV", show.to_csv(index=False).encode("utf-8"), "hasil_pencarian_curah_hujan.csv", "text/csv")

elif menu == "Ranking & Status":
    c1, c2 = st.columns([.9, 1.2])
    with c1:
        st.markdown("### 🏆 Ranking 3 Besar Curah Hujan per Estate")
        st.dataframe(ranking[["Estate", "Curah Hujan"]], use_container_width=True, hide_index=True)
        fig = px.bar(ranking, x="Estate", y="Curah Hujan", text="Curah Hujan", title="<b>Top 3 Estate</b>")
        st.plotly_chart(plotly_layout(fig, height=340), use_container_width=True)
    with c2:
        st.markdown("### 🌧️ Status Kondisi per Estate per Bulan")
        status_df = monthly[["Estate", "Bulan", "quantity_bulat", "Status Kondisi"]].rename(columns={"quantity_bulat": "Curah Hujan Bulanan (MM)"})
        st.dataframe(status_df.sort_values(["Estate", "Bulan"]), use_container_width=True, hide_index=True)
        st.caption("Status: <100 MM = Kering, 100–300 MM = Normal, >300 MM = Tinggi.")

else:
    st.markdown("### ℹ️ Tentang Data")
    st.write("Aplikasi ini memakai database Excel curah hujan yang disertakan pada folder aplikasi. Filter utama berada di bagian atas dashboard.")
    st.dataframe(pd.DataFrame({
        "Item": ["Baris data", "Periode awal", "Periode akhir", "Estate", "Divisi"],
        "Nilai": [len(df), str(min_date), str(max_date), df["Estate"].nunique(), df["Divisi"].nunique()],
    }), hide_index=True, use_container_width=True)
