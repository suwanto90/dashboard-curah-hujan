
# GANTI BAGIAN RENTANG TANGGAL DENGAN INI

# pastikan tanggal valid
date_series = pd.to_datetime(df["Document Date"], errors="coerce").dropna()

if len(date_series) > 0:
    min_date = date_series.min().date()
    max_date = date_series.max().date()
else:
    min_date = pd.Timestamp("2026-04-01").date()
    max_date = pd.Timestamp("2026-06-30").date()


tanggal = st.date_input(
    "Rentang Tanggal",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)
