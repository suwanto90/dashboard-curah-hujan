
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard Curah Hujan",
    page_icon="🌧️",
    layout="wide"
)

st.title("🌧️ Dashboard Pencarian Data Curah Hujan")
st.write("Pencarian berdasarkan multi Estate, multi Divisi, dan rentang Document Date")


@st.cache_data
def load_data():
    df = pd.read_excel(
        "DATA CURAH HUJAN APRIL-JUNI 2026.XLS(1).xlsx",
        header=1
    )

    df.columns = [str(c).strip() for c in df.columns]

    df["Document Date"] = pd.to_datetime(
        df["Document Date"],
        errors="coerce"
    )

    return df


df = load_data()


st.subheader("🔎 Menu Pencarian")

col1, col2 = st.columns(2)

with col1:
    estate_list = sorted(
        df["Estate"].dropna().astype(str).unique()
    )

    estate = st.multiselect(
        "🏡 Pilih Estate (bisa lebih dari satu)",
        estate_list
    )


with col2:
    divisi_list = sorted(
        df["Divisi"].dropna().astype(str).unique()
    )

    divisi = st.multiselect(
        "🏢 Pilih Divisi (bisa lebih dari satu)",
        divisi_list
    )


col3, col4 = st.columns(2)

with col3:
    tanggal_awal = st.date_input(
        "📅 Document Date Mulai",
        value=df["Document Date"].min().date()
    )

with col4:
    tanggal_akhir = st.date_input(
        "📅 Document Date Sampai",
        value=df["Document Date"].max().date()
    )


# FILTER DATA
hasil = df.copy()


if estate:
    hasil = hasil[
        hasil["Estate"].astype(str).isin(estate)
    ]


if divisi:
    hasil = hasil[
        hasil["Divisi"].astype(str).isin(divisi)
    ]


hasil = hasil[
    (hasil["Document Date"].dt.date >= tanggal_awal) &
    (hasil["Document Date"].dt.date <= tanggal_akhir)
]


st.divider()

st.subheader("📋 Hasil Pencarian")


kolom = [
    "Document Date",
    "Estate",
    "Divisi",
    "quantity",
    "UM"
]


kolom_tersedia = [
    x for x in kolom if x in hasil.columns
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


    total = pd.to_numeric(
        hasil["quantity"],
        errors="coerce"
    ).sum()

    b.metric(
        "Total Curah Hujan",
        f"{total:,.0f}"
    )


    c.metric(
        "Periode",
        f"{tanggal_awal} s/d {tanggal_akhir}"
    )


    st.subheader("📊 Grafik Curah Hujan")


    grafik1 = px.bar(
        hasil,
        x="Estate",
        y="quantity",
        color="Divisi",
        title="Curah Hujan per Estate dan Divisi"
    )

    st.plotly_chart(
        grafik1,
        use_container_width=True
    )


    grafik2 = px.line(
        hasil.sort_values("Document Date"),
        x="Document Date",
        y="quantity",
        color="Estate",
        markers=True,
        title="Trend Curah Hujan"
    )

    st.plotly_chart(
        grafik2,
        use_container_width=True
    )


else:

    st.warning(
        "Data tidak ditemukan. Silakan ubah filter pencarian."
    )


st.sidebar.info(
    "Dashboard Curah Hujan - Database Excel April-Juni 2026"
)
