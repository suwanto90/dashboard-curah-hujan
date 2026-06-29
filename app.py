
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard Curah Hujan Estate",
    page_icon="🌴",
    layout="wide"
)

# Background kebun sawit
st.markdown("""
<style>
.stApp {
    background-image:
    linear-gradient(rgba(255,255,255,0.86), rgba(255,255,255,0.86)),
    url("https://images.unsplash.com/photo-1595841696677-6489ff3f8cd1");
    background-size: cover;
    background-attachment: fixed;
}
</style>
""", unsafe_allow_html=True)

st.title("🌴 Dashboard Monitoring Curah Hujan Perkebunan Kelapa Sawit")
st.caption("Analisis rata-rata curah hujan berdasarkan Estate - April, Mei, Juni 2026")


@st.cache_data
def load_data():
    df = pd.read_excel(
        "DATA CURAH HUJAN APRIL-JUNI 2026.XLS(1).xlsx",
        header=1
    )

    df.columns = [str(c).strip() for c in df.columns]
    df["Document Date"] = pd.to_datetime(df["Document Date"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

    return df


df = load_data()

st.subheader("🔎 Menu Pencarian")

c1, c2 = st.columns(2)

with c1:
    estate = st.multiselect(
        "🏡 Estate",
        sorted(df["Estate"].dropna().astype(str).unique())
    )

with c2:
    divisi = st.multiselect(
        "🏢 Divisi",
        sorted(df["Divisi"].dropna().astype(str).unique())
    )

c3, c4 = st.columns(2)

with c3:
    start = st.date_input("Tanggal Mulai", df["Document Date"].min().date())

with c4:
    end = st.date_input("Tanggal Akhir", df["Document Date"].max().date())


hasil = df.copy()

if estate:
    hasil = hasil[hasil["Estate"].astype(str).isin(estate)]

if divisi:
    hasil = hasil[hasil["Divisi"].astype(str).isin(divisi)]

hasil = hasil[
    (hasil["Document Date"].dt.date >= start) &
    (hasil["Document Date"].dt.date <= end)
]


st.subheader("📋 Informasi Lengkap Hasil Pencarian")

st.dataframe(
    hasil[["Document Date","Estate","Divisi","quantity","UM"]],
    use_container_width=True
)

st.divider()

# DATA ANALISIS RATA-RATA
analisis = hasil.copy()

analisis["Bulan"] = analisis["Document Date"].dt.month_name()
analisis["Minggu"] = "W" + (((analisis["Document Date"].dt.day-1)//7)+1).astype(str)


bulan_order = ["April","May","June"]
minggu_order = ["W1","W2","W3","W4"]


# 1 rata-rata mingguan
st.subheader("1️⃣ Rata-rata Curah Hujan Harian per Estate per Minggu")

weekly = analisis.groupby(
    ["Bulan","Minggu","Estate"],
    as_index=False
)["quantity"].mean()

weekly["Bulan"] = pd.Categorical(
    weekly["Bulan"],
    categories=bulan_order,
    ordered=True
)

weekly["Minggu"] = pd.Categorical(
    weekly["Minggu"],
    categories=minggu_order,
    ordered=True
)

st.plotly_chart(
    px.bar(
        weekly,
        x="Minggu",
        y="quantity",
        color="Estate",
        facet_col="Bulan",
        category_orders={"Bulan":bulan_order,"Minggu":minggu_order},
        title="Rata-rata Curah Hujan Harian Mingguan"
    ),
    use_container_width=True
)


# 2 bulanan rata-rata
st.subheader("2️⃣ Rata-rata Curah Hujan Bulanan per Estate")

monthly = analisis.groupby(
    ["Bulan","Estate"],
    as_index=False
)["quantity"].mean()

monthly["Bulan"] = pd.Categorical(
    monthly["Bulan"],
    categories=bulan_order,
    ordered=True
)

st.plotly_chart(
    px.bar(
        monthly,
        x="Bulan",
        y="quantity",
        color="Estate",
        barmode="group",
        title="Rata-rata Curah Hujan Bulanan"
    ),
    use_container_width=True
)


# 3 trend bar
st.subheader("3️⃣ Trend Rata-rata Curah Hujan Estate per Bulan")

st.plotly_chart(
    px.bar(
        monthly,
        x="Bulan",
        y="quantity",
        color="Estate",
        title="Trend Curah Hujan"
    ),
    use_container_width=True
)


# 4 pie
st.subheader("4️⃣ Hari Hujan vs Tidak Hujan per Estate")

pie = analisis.copy()

pie["Status Hari"] = pie["quantity"].apply(
    lambda x: "Hari Hujan" if x > 0 else "Tidak Hujan"
)

pie = pie.groupby(
    ["Estate","Status Hari"]
).size().reset_index(name="Jumlah Hari")


st.plotly_chart(
    px.pie(
        pie,
        names="Status Hari",
        values="Jumlah Hari",
        facet_col="Estate"
    ),
    use_container_width=True
)


# 5 ranking
st.subheader("5️⃣ Ranking 3 Besar Curah Hujan Estate")

ranking = monthly.groupby(
    "Estate",
    as_index=False
)["quantity"].mean()

ranking = ranking.sort_values(
    "quantity",
    ascending=False
).head(3)

st.dataframe(ranking)


# 6 status
st.subheader("6️⃣ Status Kondisi Estate per Bulan")

def kondisi(x):
    if x < 100:
        return "Kering"
    elif x <= 300:
        return "Normal"
    else:
        return "Tinggi"

status = monthly.copy()
status["Status"] = status["quantity"].apply(kondisi)

st.dataframe(
    status[["Bulan","Estate","quantity","Status"]],
    use_container_width=True
)

st.info("Kriteria: <100 mm Kering | 100-300 mm Normal | >300 mm Tinggi")
