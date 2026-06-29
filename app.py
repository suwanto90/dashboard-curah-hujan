
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard Curah Hujan Estate",
    page_icon="🌧️",
    layout="wide"
)

# Background dashboard
st.markdown("""
<style>
.stApp {
    background-image:
    linear-gradient(rgba(255,255,255,0.88), rgba(255,255,255,0.88)),
    url("https://images.unsplash.com/photo-1437622368342-7a3d73a34c8f");
    background-size: cover;
    background-attachment: fixed;
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


# =====================
# FILTER PENCARIAN
# =====================

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
    start = st.date_input(
        "📅 Mulai",
        df["Document Date"].min().date()
    )

with c4:
    end = st.date_input(
        "📅 Sampai",
        df["Document Date"].max().date()
    )


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
    (hasil["Document Date"].dt.date >= start) &
    (hasil["Document Date"].dt.date <= end)
]


# =====================
# HASIL PENCARIAN
# =====================

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

st.header("📊 Analisis Curah Hujan")


# =====================
# 1. WEEKLY W1-W4
# =====================

st.subheader("1. Curah Hujan Mingguan per Estate (W1-W4)")

weekly = hasil.copy()

weekly["Bulan"] = weekly["Document Date"].dt.month_name()

weekly["Minggu"] = (
    ((weekly["Document Date"].dt.day - 1) // 7) + 1
)

weekly["Minggu"] = "W" + weekly["Minggu"].astype(str)

weekly = weekly.groupby(
    ["Bulan","Minggu","Estate"],
    as_index=False
)["quantity"].sum()


bulan_order = ["April","May","June"]
minggu_order = ["W1","W2","W3","W4"]

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
        category_orders={
            "Bulan": bulan_order,
            "Minggu": minggu_order
        }
    ),
    use_container_width=True
)


# =====================
# 2. BULANAN
# =====================

st.subheader("2. Curah Hujan Bulanan per Estate")

monthly = hasil.copy()

monthly["Bulan"] = monthly["Document Date"].dt.month_name()

monthly = monthly.groupby(
    ["Bulan","Estate"],
    as_index=False
)["quantity"].sum()

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
        category_orders={
            "Bulan": bulan_order
        }
    ),
    use_container_width=True
)


# =====================
# 3 TREND BAR
# =====================

st.subheader("3. Trend Curah Hujan Estate per Bulan")

st.plotly_chart(
    px.bar(
        monthly,
        x="Bulan",
        y="quantity",
        color="Estate",
        category_orders={
            "Bulan": bulan_order
        }
    ),
    use_container_width=True
)


# =====================
# 4 PIE
# =====================

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


# =====================
# 5 RANKING
# =====================

st.subheader("5. Ranking 3 Besar Curah Hujan Estate")

ranking = (
    monthly.groupby("Estate", as_index=False)
    ["quantity"].sum()
    .sort_values(
        "quantity",
        ascending=False
    )
    .head(3)
)

st.dataframe(
    ranking,
    use_container_width=True
)


st.plotly_chart(
    px.bar(
        ranking,
        x="Estate",
        y="quantity"
    ),
    use_container_width=True
)


# =====================
# 6 STATUS
# =====================

st.subheader("6. Status Kondisi Estate per Bulan")


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
    status[
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
