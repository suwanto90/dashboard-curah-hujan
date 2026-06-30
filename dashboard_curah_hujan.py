
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Karyamas Plantation Rainfall Dashboard",
    page_icon="🌧️",
    layout="wide"
)

# =========================
# STYLE DASHBOARD
# =========================
st.markdown("""
<style>
.stApp{
    background:#071821;
    color:white;
}
[data-testid="metric-container"]{
    background:#102b36;
    padding:15px;
    border-radius:12px;
}
</style>
""", unsafe_allow_html=True)


# =========================
# LOAD EXCEL DATABASE
# =========================
@st.cache_data
def load_data():

    df = pd.read_excel(
        "DATA CURAH HUJAN APRIL-JUNI 2026.XLS(1)(5).xlsx",
        header=1
    )

    df.columns=[
        "Estate",
        "Divisi",
        "Document Number",
        "Document Date",
        "Statkf",
        "Quantity",
        "UM",
        "Created On",
        "Created By",
        "Time",
        "User Name"
    ]

    df["Document Date"] = pd.to_datetime(
        df["Document Date"],
        errors="coerce"
    )

    df["Quantity"] = pd.to_numeric(
        df["Quantity"],
        errors="coerce"
    )

    df=df.dropna(subset=["Document Date"])

    df["Bulan"] = df["Document Date"].dt.month.map({
        4:"April",
        5:"Mei",
        6:"Juni"
    })

    df["Minggu"] = (
        "W" +
        (((df["Document Date"].dt.day-1)//7)+1)
        .astype(int)
        .astype(str)
    )

    return df


df=load_data()


# =========================
# HEADER
# =========================
st.title("🌧️ DASHBOARD SISTEM MONITORING TERPADU CURAH HUJAN")
st.caption("KARYAMAS PLANTATION - MULTI ESTATE MONITORING SYSTEM")


# =========================
# FILTER
# =========================
st.subheader("🔎 Pencarian Data Curah Hujan")

c1,c2,c3=st.columns(3)

with c1:
    estate=st.multiselect(
        "Pilih Estate",
        sorted(df.Estate.unique()),
        default=list(df.Estate.unique())
    )

with c2:
    divisi=st.multiselect(
        "Pilih Divisi",
        sorted(df.Divisi.unique()),
        default=list(df.Divisi.unique())
    )

with c3:

    min_date=df["Document Date"].min().date()
    max_date=df["Document Date"].max().date()

    tanggal=st.date_input(
        "Rentang Document Date",
        value=(min_date,max_date),
        min_value=min_date,
        max_value=max_date
    )


data=df.copy()

if estate:
    data=data[data.Estate.isin(estate)]

if divisi:
    data=data[data.Divisi.isin(divisi)]

if len(tanggal)==2:
    data=data[
        (data["Document Date"]>=pd.to_datetime(tanggal[0])) &
        (data["Document Date"]<=pd.to_datetime(tanggal[1]))
    ]


# =========================
# KPI
# =========================
a,b,c,d=st.columns(4)

a.metric(
    "Rata-rata Harian",
    f"{data.Quantity.mean():.0f} mm"
)

b.metric(
    "Total Curah Hujan",
    f"{data.Quantity.sum():.0f} mm"
)

c.metric(
    "Hari Hujan",
    int((data.Quantity>0).sum())
)

d.metric(
    "Jumlah Estate",
    data.Estate.nunique()
)


# =========================
# 1 WEEKLY ESTATE
# =========================
st.subheader(
"1. Rata-rata Curah Hujan Harian per Estate per Minggu"
)

bulan_order=["April","Mei","Juni"]
minggu_order=["W1","W2","W3","W4"]

weekly=data.groupby(
["Bulan","Minggu","Estate"]
)["Quantity"].mean().reset_index()

weekly["Bulan"]=pd.Categorical(
    weekly.Bulan,
    bulan_order,
    ordered=True
)

weekly["Minggu"]=pd.Categorical(
    weekly.Minggu,
    minggu_order,
    ordered=True
)

weekly=weekly.sort_values(
["Bulan","Minggu"]
)


st.plotly_chart(
px.line(
weekly,
x="Minggu",
y="Quantity",
color="Estate",
facet_col="Bulan",
markers=True
),
use_container_width=True
)



# =========================
# 2 MONTHLY LINE
# =========================
st.subheader(
"2. Rata-rata Curah Hujan Bulanan per Estate"
)

monthly=data.groupby(
["Bulan","Estate"]
)["Quantity"].mean().reset_index()

monthly["Bulan"]=pd.Categorical(
monthly.Bulan,
bulan_order,
ordered=True
)

monthly=monthly.sort_values("Bulan")


st.plotly_chart(
px.line(
monthly,
x="Bulan",
y="Quantity",
color="Estate",
markers=True
),
use_container_width=True
)



# =========================
# 3 BAR TREND
# =========================
st.subheader(
"3. Trend Curah Hujan Rata-rata Estate per Bulan"
)

st.plotly_chart(
px.bar(
monthly,
x="Bulan",
y="Quantity",
color="Estate",
barmode="group"
),
use_container_width=True
)



# =========================
# 4 PIE HUJAN PER ESTATE
# =========================
st.subheader(
"4. Hari Hujan vs Tidak Hujan per Estate"
)

pie=data.copy()

pie["Status Hujan"]=pie.Quantity.apply(
lambda x:"Hari Hujan" if x>0 else "Tidak Hujan"
)

pie=pie.groupby(
["Estate","Status Hujan"]
).size().reset_index(name="Jumlah")


st.plotly_chart(
px.pie(
pie,
names="Status Hujan",
values="Jumlah",
facet_col="Estate"
),
use_container_width=True
)



# =========================
# 5 RANKING
# =========================
st.subheader(
"5. Ranking 3 Besar Curah Hujan Estate"
)

rank=data.groupby(
"Estate"
)["Quantity"].mean().reset_index()

rank=rank.sort_values(
"Quantity",
ascending=False
).head(3)

rank["Quantity"]=rank.Quantity.round().astype(int)

st.dataframe(rank)



# =========================
# 6 STATUS KONDISI
# =========================
st.subheader(
"6. Status Kondisi Curah Hujan per Estate per Bulan"
)


status=data.groupby(
["Estate","Bulan"]
)["Quantity"].mean().reset_index()


status["Total Bulanan"]=(
status.Quantity*30
).round().astype(int)


def kondisi(x):

    if x < 100:
        return "KERING"

    elif x <=300:
        return "NORMAL"

    else:
        return "TINGGI"


status["Status"]=status["Total Bulanan"].apply(kondisi)


st.dataframe(
status[
[
"Estate",
"Bulan",
"Total Bulanan",
"Status"
]
],
use_container_width=True
)
