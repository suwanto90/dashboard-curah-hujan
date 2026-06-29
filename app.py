
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard Curah Hujan",
    page_icon="🌧️",
    layout="wide"
)

st.title("🌧️ Dashboard Pencarian Data Curah Hujan")
st.write("Pencarian berdasarkan Estate, Divisi, dan Document Date")

@st.cache_data
def load_data():
    # Header berada di baris kedua Excel (index 1)
    df = pd.read_excel(
        "DATA CURAH HUJAN APRIL-JUNI 2026.XLS(1).xlsx",
        header=1
    )

    df.columns = [str(c).strip() for c in df.columns]

    # Konversi tanggal
    if "Document Date" in df.columns:
        df["Document Date"] = pd.to_datetime(
            df["Document Date"],
            errors="coerce"
        )

    return df


df = load_data()

# Menu pencarian
st.subheader("🔎 Pencarian Data")

col1, col2, col3 = st.columns(3)

with col1:
    estate_list = ["Semua"] + sorted(
        df["Estate"].dropna().astype(str).unique()
    )
    estate = st.selectbox(
        "🏡 Estate",
        estate_list
    )

with col2:
    divisi_list = ["Semua"] + sorted(
        df["Divisi"].dropna().astype(str).unique()
    )
    divisi = st.selectbox(
        "🏢 Divisi",
        divisi_list
    )

with col3:
    tanggal = st.date_input(
        "📅 Document Date"
    )


# Filter data
hasil = df.copy()

if estate != "Semua":
    hasil = hasil[
        hasil["Estate"].astype(str) == estate
    ]

if divisi != "Semua":
    hasil = hasil[
        hasil["Divisi"].astype(str) == divisi
    ]

if tanggal:
    hasil = hasil[
        hasil["Document Date"].dt.date == tanggal
    ]


st.divider()

st.subheader("📋 Hasil Pencarian")

kolom_tampil = [
    "Document Date",
    "Estate",
    "Divisi",
    "quantity",
    "UM"
]

kolom_tersedia = [
    c for c in kolom_tampil
    if c in hasil.columns
]


if len(hasil) > 0:

    st.dataframe(
        hasil[kolom_tersedia],
        use_container_width=True
    )

    a,b,c = st.columns(3)

    a.metric(
        "Jumlah Data",
        len(hasil)
    )

    if "quantity" in hasil.columns:
        total = pd.to_numeric(
            hasil["quantity"],
            errors="coerce"
        ).sum()

        b.metric(
            "Total Curah Hujan",
            f"{total:,.0f}"
        )

    if "UM" in hasil.columns:
        c.metric(
            "Satuan",
            str(hasil["UM"].iloc[0])
        )


    st.subheader("📊 Grafik Curah Hujan")

    if "Divisi" in hasil.columns and "quantity" in hasil.columns:

        grafik = px.bar(
            hasil,
            x="Divisi",
            y="quantity",
            title="Curah Hujan Berdasarkan Divisi"
        )

        st.plotly_chart(
            grafik,
            use_container_width=True
        )


    if "Document Date" in hasil.columns and "quantity" in hasil.columns:

        trend = px.line(
            hasil.sort_values("Document Date"),
            x="Document Date",
            y="quantity",
            markers=True,
            title="Trend Curah Hujan"
        )

        st.plotly_chart(
            trend,
            use_container_width=True
        )

else:
    st.warning(
        "Data tidak ditemukan. Silakan ubah filter."
    )


st.sidebar.info(
    "Dashboard menggunakan database Excel Curah Hujan April-Juni 2026."
)
