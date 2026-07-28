import pandas as pd

df = pd.read_excel(
    "data/processed/population_processed.xlsx"
)

print(df["population_count"].max())

print(
    df.loc[
        df["population_count"].idxmax()
    ]
)