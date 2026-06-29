
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard Curah Hujan Estate",
    page_icon="🌧️",
    layout="wide"
)

# Background elegan
st.markdown("""
<style>
.stApp {
    background-image:
    linear-gradient(rgba(255,255,255,0.90), rgba(255,255,255,0.90)),
    url("https://images.unsplash.com/photo-1501691223387-dd0500403074");
    background-size: cover;
    background-attachment: fixed;
}
[data-testid="stMetric"] {
    background-color: rgba(255,255,255,0.75);
    padding: 15px;
    border-radius: 15px;
}
</style>
""", unsafe_allow_html=True)


st.title("🌧️ Dashboard Monitoring Curah Hujan Estate")
st.caption("Analisis Curah Hujan April - Juni 2026")


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

    df["quantity"] = pd.to_numeric(
        df["quantity"],
        errors="coerce"
    )

    return df


df = load_data()


# FILTER
st.subheader("🔎 Pencarian Data")

a,b = st.columns(2)

with a:
    estate = st.multiselect(
        "🏡 Estate",
        sorted(df["Estate"].dropna().astype(str).unique())
    )

with b:
    divisi = st.multiselect(
        "🏢 Divisi",
        sorted(df["Divisi"].dropna().astype(str).unique())
    )


c,d = st.columns(2)

with c:
    start = st.date_input(
        "Tanggal Mulai",
        df["Document Date"].min().date()
    )

with d:
    end = st.date_input(
        "Tanggal Akhir",
        df["Document Date"].max().date()
    )


hasil = df.copy()

if estate:
    hasil = hasil[hasil["Estate"].astype(str).isin(estate)]

if divisi:
    hasil = hasil[hasil["Divisi"].astype(str).isin(divisi)]


hasil = hasil[
    (hasil["Document Date"].dt.date >= start) &
    (hasil["Document Date"].dt.date <= end)
]


# HASIL DATA
st.subheader("📋 Informasi Lengkap Hasil Pencarian")

st.dataframe(
    hasil[
        [
            "Document Date",
            "Estate",
            "Divisi",
            "quantity",
            "UM"
        ]
    ],
    use_container_width=True
)


st.divider()


# GRAFIK

st.header("📊 Analisis Curah Hujan")


# 1 Harian
st.subheader("1. Curah Hujan Harian per Estate (Tanggal 1 - 31)")

daily = hasil.copy()
daily["Tanggal"] = daily["Document Date"].dt.day

daily = daily.groupby(
    ["Tanggal","Estate"],
    as_index=False
)["quantity"].sum()


st.plotly_chart(
    px.line(
        daily,
        x="Tanggal",
        y="quantity",
        color="Estate",
        markers=True
    ),
    use_container_width=True
)


# 2 Bulanan
st.subheader("2. Curah Hujan Bulanan per Estate (April - Juni)")


monthly = hasil.copy()
monthly["Bulan"] = monthly["Document Date"].dt.month_name()

monthly = monthly.groupby(
    ["Bulan","Estate"],
    as_index=False
)["quantity"].sum()


order = ["April","May","June"]

monthly["Bulan"] = pd.Categorical(
    monthly["Bulan"],
    categories=order,
    ordered=True
)


st.plotly_chart(
    px.bar(
        monthly,
        x="Bulan",
        y="quantity",
        color="Estate",
        barmode="group"
    ),
    use_container_width=True
)


# 3 Trend
st.subheader("3. Trend Curah Hujan per Estate")

st.plotly_chart(
    px.line(
        monthly,
        x="Bulan",
        y="quantity",
        color="Estate",
        markers=True
    ),
    use_container_width=True
)


# 4 Pie
st.subheader("4. Hari Hujan vs Tidak Hujan per Estate")


pie = hasil.copy()

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


# 5 Ranking
st.subheader("5. Ranking 3 Besar Curah Hujan Estate")


ranking = monthly.groupby(
    "Estate",
    as_index=False
)["quantity"].sum()


ranking = ranking.sort_values(
    "quantity",
    ascending=False
).head(3)


st.dataframe(ranking)


st.plotly_chart(
    px.bar(
        ranking,
        x="Estate",
        y="quantity"
    ),
    use_container_width=True
)


# 6 Status
st.subheader("6. Status Kondisi Estate per Bulan")


def status(x):
    if x < 100:
        return "Kering"
    elif x <= 300:
        return "Normal"
    else:
        return "Tinggi"


kondisi = monthly.copy()

kondisi["Status"] = kondisi["quantity"].apply(status)


st.dataframe(
    kondisi[
        [
            "Bulan",
            "Estate",
            "quantity",
            "Status"
        ]
    ],
    use_container_width=True
)


st.info(
    "Kriteria: <100 mm Kering | 100-300 mm Normal | >300 mm Tinggi"
)
