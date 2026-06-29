
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Curah Hujan", page_icon="🌧️", layout="wide")

st.title("🌧️ Dashboard Monitoring Curah Hujan")

@st.cache_data
def load_data():
    df = pd.read_excel("DATA CURAH HUJAN APRIL-JUNI 2026.XLS(1).xlsx", header=1)
    df.columns = [str(c).strip() for c in df.columns]
    df["Document Date"] = pd.to_datetime(df["Document Date"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    return df

df = load_data()

st.subheader("🔎 Menu Pencarian")

a,b = st.columns(2)
with a:
    estate = st.multiselect("🏡 Estate", sorted(df["Estate"].dropna().astype(str).unique()))
with b:
    divisi = st.multiselect("🏢 Divisi", sorted(df["Divisi"].dropna().astype(str).unique()))

c,d = st.columns(2)
with c:
    mulai = st.date_input("📅 Mulai", df["Document Date"].min().date())
with d:
    akhir = st.date_input("📅 Sampai", df["Document Date"].max().date())

hasil = df.copy()

if estate:
    hasil = hasil[hasil["Estate"].astype(str).isin(estate)]

if divisi:
    hasil = hasil[hasil["Divisi"].astype(str).isin(divisi)]

hasil = hasil[(hasil["Document Date"].dt.date >= mulai) &
              (hasil["Document Date"].dt.date <= akhir)]

st.subheader("📋 Informasi Lengkap Hasil Pencarian")

st.dataframe(
    hasil[["Document Date","Estate","Divisi","quantity","UM"]],
    use_container_width=True
)

st.divider()
st.subheader("📊 Grafik Analisis Curah Hujan")


# 1 Grafik harian tanggal 1-31
st.write("### 1. Curah Hujan Harian per Estate (Tanggal 1 - 31)")

harian = hasil.copy()
harian["Tanggal"] = harian["Document Date"].dt.day
harian = harian.groupby(["Tanggal","Estate"], as_index=False)["quantity"].sum()

fig1 = px.line(
    harian,
    x="Tanggal",
    y="quantity",
    color="Estate",
    markers=True
)
fig1.update_xaxes(dtick=1)

st.plotly_chart(fig1, use_container_width=True)


# 2 Grafik bulanan April Mei Juni
st.write("### 2. Curah Hujan Bulanan per Estate (April, Mei, Juni)")

bulanan = hasil.copy()
bulanan["Bulan"] = bulanan["Document Date"].dt.month_name()

bulanan = bulanan.groupby(
    ["Bulan","Estate"],
    as_index=False
)["quantity"].sum()

urutan = ["April","May","June"]
bulanan["Bulan"] = pd.Categorical(
    bulanan["Bulan"],
    categories=urutan,
    ordered=True
)

fig2 = px.bar(
    bulanan,
    x="Bulan",
    y="quantity",
    color="Estate",
    barmode="group"
)

st.plotly_chart(fig2, use_container_width=True)


# 3 Pie hari hujan
st.write("### 3. Hari Hujan vs Tidak Hujan per Estate")

pie = hasil.copy()

pie["Status"] = pie["quantity"].apply(
    lambda x: "Hari Hujan" if x > 0 else "Tidak Hujan"
)

pie = pie.groupby(
    ["Estate","Status"]
).size().reset_index(name="Jumlah Hari")

fig3 = px.pie(
    pie,
    names="Status",
    values="Jumlah Hari",
    facet_col="Estate"
)

st.plotly_chart(fig3, use_container_width=True)
