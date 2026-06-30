
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Karyamas Plantation Rainfall Dashboard",
    page_icon="🌧️",
    layout="wide"
)

# Logo perusahaan
st.image("pt_karyamas_adinusantara_logo.jpg", width=220)

st.title("🌧️ Rainfall Monitoring Dashboard")
st.subheader("Karyamas Plantation")

st.caption(
    "Dashboard monitoring curah hujan perkebunan "
    "berdasarkan Estate, Divisi dan Document Date"
)

@st.cache_data
def load_data():
    df = pd.read_excel(
        "DATA CURAH HUJAN APRIL-JUNI 2026.XLS(1)(5).xlsx",
        header=1
    )

    df.columns = [
        "Estate","Divisi","Document Number",
        "Document Date","Statkf","Quantity",
        "UM","Created On","Created By",
        "Time","User Name"
    ]

    df["Document Date"] = pd.to_datetime(
        df["Document Date"], errors="coerce"
    )

    df["Quantity"] = pd.to_numeric(
        df["Quantity"], errors="coerce"
    )

    return df


df = load_data()

st.divider()

st.subheader("🔎 Menu Pencarian")

c1,c2,c3 = st.columns(3)

with c1:
    estate = st.selectbox(
        "🏝️ Estate",
        ["Semua"] + sorted(df["Estate"].dropna().unique())
    )

with c2:
    divisi = st.selectbox(
        "🌱 Divisi",
        ["Semua"] + sorted(df["Divisi"].dropna().unique())
    )

with c3:
    tanggal = st.date_input(
        "📅 Document Date"
    )


hasil = df.copy()

if estate != "Semua":
    hasil = hasil[hasil.Estate == estate]

if divisi != "Semua":
    hasil = hasil[hasil.Divisi == divisi]

if tanggal:
    hasil = hasil[
        hasil["Document Date"].dt.date == tanggal
    ]


st.divider()

a,b,c,d = st.columns(4)

a.metric("Total Data", len(hasil))
b.metric(
    "Curah Hujan",
    f"{hasil.Quantity.sum():,.1f} mm"
)
c.metric(
    "Rata-rata",
    f"{hasil.Quantity.mean():,.1f} mm"
)
d.metric(
    "Estate",
    hasil.Estate.nunique()
)


if len(hasil)>0:

    st.subheader("📊 Grafik Curah Hujan")

    daily = (
        hasil.groupby("Document Date")
        ["Quantity"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        daily,
        x="Document Date",
        y="Quantity",
        title="Curah Hujan Harian"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    st.subheader("📋 Informasi Lengkap")

    st.dataframe(
        hasil[
            [
                "Document Date",
                "Estate",
                "Divisi",
                "Quantity",
                "UM"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

else:
    st.warning("Data tidak ditemukan")


st.sidebar.image(
    "pt_karyamas_adinusantara_logo.jpg",
    width=180
)

st.sidebar.info(
    "Karyamas Plantation\n\n"
    "Rainfall Monitoring System"
)
