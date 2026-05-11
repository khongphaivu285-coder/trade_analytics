import pandas as pd


df = pd.read_parquet(

    "data/parquet/purchase_order.parquet"
)

print(df.head())

print(df.dtypes)