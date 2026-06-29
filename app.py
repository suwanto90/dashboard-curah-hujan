
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

st.subheader("🔎 Filter Pencarian")

a,b = st.columns(2)

with a:
    estate = st.multiselect("🏡 Estate", sorted(df["Estate"].dropna().astype(str).unique()))

with b:
    divisi = st.multiselect("🏢 Divisi", sorted(df["Divisi"].dropna().astype(str).unique()))

c,d = st.columns(2)

with c:
    mulai = st.date_input("📅 Tanggal Mulai", df["Document Date"].min().date())

with d:
    akhir = st.date_input("📅 Tanggal Akhir", df["Document Date"].max().date())

data = df.copy()

if estate:
    data = data[data["Estate"].astype(str).isin(estate)]

if divisi:
    data = data[data["Divisi"].astype(str).isin(divisi)]

data = data[(data["Document Date"].dt.date >= mulai) & (data["Document Date"].dt.date <= akhir)]


st.divider()

# 1 Harian
st.subheader("1. Curah Hujan Harian per Estate")

harian = data.groupby(["Document Date","Estate"], as_index=False)["quantity"].sum()

st.plotly_chart(
    px.line(harian, x="Document Date", y="quantity", color="Estate", markers=True),
    use_container_width=True
)


# 2 Bulanan
st.subheader("2. Curah Hujan Bulanan per Estate")

bulanan = data.copy()
bulanan["Bulan"] = bulanan["Document Date"].dt.to_period("M").astype(str)

bulanan = bulanan.groupby(["Bulan","Estate"], as_index=False)["quantity"].sum()

st.plotly_chart(
    px.bar(bulanan, x="Bulan", y="quantity", color="Estate", barmode="group"),
    use_container_width=True
)


# 3 Trend
st.subheader("3. Trend Curah Hujan per Estate")

st.plotly_chart(
    px.line(bulanan, x="Bulan", y="quantity", color="Estate", markers=True),
    use_container_width=True
)


# 4 Ranking
st.subheader("4. Ranking 3 Besar Curah Hujan Estate")

ranking = bulanan.groupby("Estate", as_index=False)["quantity"].sum()
ranking = ranking.sort_values("quantity", ascending=False).head(3)

st.dataframe(ranking, use_container_width=True)

st.plotly_chart(
    px.bar(ranking, x="Estate", y="quantity"),
    use_container_width=True
)


# 5 Status
st.subheader("5. Status Kondisi Estate per Bulan")

def status(mm):
    if mm < 100:
        return "Kering"
    elif mm <= 300:
        return "Normal"
    else:
        return "Tinggi"

kondisi = bulanan.copy()
kondisi["Status"] = kondisi["quantity"].apply(status)

st.dataframe(
    kondisi[["Bulan","Estate","quantity","Status"]],
    use_container_width=True
)

st.info("Status: <100 mm Kering | 100-300 mm Normal | >300 mm Tinggi")
