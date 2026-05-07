from etl.extract import load_excel


# =========================
# TEST PURCHASE ORDER
# =========================

df_po = load_excel(

    "purchase_order"
)

print(df_po.head())

print(df_po.columns)