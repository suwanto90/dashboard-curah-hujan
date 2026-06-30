
# PERBAIKAN RENTANG TANGGAL STREAMLIT
# Ganti bagian date_input lama dengan kode ini

min_date = df["Document Date"].dropna().min()
max_date = df["Document Date"].dropna().max()

if pd.isna(min_date) or pd.isna(max_date):
    min_date = pd.Timestamp("2026-04-01")
    max_date = pd.Timestamp("2026-06-30")

c1, c2, c3 = st.columns(3)

with c3:
    tanggal = st.date_input(
        "Rentang Tanggal",
        value=[
            min_date.date(),
            max_date.date()
        ],
        min_value=min_date.date(),
        max_value=max_date.date()
    )


# filter tanggal
if len(tanggal) == 2:
    data = data[
        (data["Document Date"] >= pd.to_datetime(tanggal[0])) &
        (data["Document Date"] <= pd.to_datetime(tanggal[1]))
    ]
