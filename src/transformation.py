import pandas as pd
import os
from datetime import datetime


# ==========================
# Paths
# ==========================

RAW_PATH = "data/raw"
PROCESSED_PATH = "data/processed"


# Missing representations
MISSING_VALUES = [
    "-",
    "...",
    "NA",
    "N/A",
    "",
    " "
]


# ==========================
# General functions
# ==========================

def create_processed_folder():

    os.makedirs(
        PROCESSED_PATH,
        exist_ok=True
    )



def clean_dataframe(df):
    """
    Apply general cleaning rules
    """

    # Remove completely empty rows
    df = df.dropna(
        axis=0,
        how="all"
    )


    # Remove completely empty columns
    df = df.dropna(
        axis=1,
        how="all"
    )


    # Convert missing representations
    df = df.replace(
        MISSING_VALUES,
        pd.NA
    )


    # Clean text columns
    for col in df.select_dtypes(
        include=["object", "string"]
    ).columns:

        df[col] = (
            df[col]
            .astype("string")
            .str.strip()
        )


        df[col] = df[col].replace(
            "nan",
            pd.NA
        )


    return df



def standardize_columns(df):
    """
    Rename columns according to warehouse model
    """


    mapping = {

        "Zone géographique":
            "geo_name",

        "Milieu de résidence":
            "residence_type",

        "Sexe":
            "sex",

        "Produit(IPC)":
            "product_category"
    }


    df = df.rename(
        columns=mapping
    )


    # Remove Excel unnamed columns safely
    columns_to_keep = []

    for col in df.columns:

        if isinstance(col, str):

            if not col.startswith("Unnamed"):
                columns_to_keep.append(col)

        else:
            # keep years
            columns_to_keep.append(col)


    df = df[
        columns_to_keep
    ]


    return df



def convert_wide_to_long(df, value_name):
    """
    Convert year columns into rows
    """


    id_columns = []
    year_columns = []


    for col in df.columns:

        if isinstance(col, int):

            year_columns.append(col)

        else:

            id_columns.append(col)



    df = df.melt(
        id_vars=id_columns,
        value_vars=year_columns,
        var_name="year",
        value_name=value_name
    )


    return df



def add_metadata(df, source_file):

    df["source_file"] = source_file

    df["processed_date"] = (
        datetime.now()
        .strftime("%Y-%m-%d %H:%M:%S")
    )


    return df



def save_excel(df, filename):

    output_path = os.path.join(
        PROCESSED_PATH,
        filename
    )


    df.to_excel(
        output_path,
        index=False
    )


    print(f"Saved: {output_path}")



# ==========================
# Population transformation
# ==========================

def transform_population():

    print("\nTransforming population...")


    source_file = "population.xlsx"


    df = pd.read_excel(
        os.path.join(
            RAW_PATH,
            source_file
        ),
        header=11
    )


    df = clean_dataframe(df)

    df = standardize_columns(df)


    df = convert_wide_to_long(
        df,
        "population_count"
    )


    df["year"] = df["year"].astype(int)


    df["population_count"] = pd.to_numeric(
        df["population_count"],
        errors="coerce"
    )


    df = add_metadata(
        df,
        source_file
    )


    save_excel(
        df,
        "population_processed.xlsx"
    )



# ==========================
# Unemployment transformation
# ==========================

def transform_unemployment():

    print("\nTransforming unemployment...")


    source_file = "unemployment_rate.xlsx"


    df = pd.read_excel(
        os.path.join(
            RAW_PATH,
            source_file
        ),
        header=11
    )


    df = clean_dataframe(df)

    df = standardize_columns(df)


    df = convert_wide_to_long(
        df,
        "unemployment_rate"
    )


    df["year"] = df["year"].astype(int)


    df["unemployment_rate"] = pd.to_numeric(
        df["unemployment_rate"],
        errors="coerce"
    )


    df = add_metadata(
        df,
        source_file
    )


    save_excel(
        df,
        "unemployment_processed.xlsx"
    )



# ==========================
# CPI transformation
# ==========================

def transform_cpi():

    print("\nTransforming CPI...")


    source_file = "consumer_price_index.xlsx"


    df = pd.read_excel(
        os.path.join(
            RAW_PATH,
            source_file
        ),
        header=11
    )


    df = clean_dataframe(df)

    df = standardize_columns(df)


    df = convert_wide_to_long(
        df,
        "cpi_value"
    )


    df["year"] = df["year"].astype(int)


    df["cpi_value"] = pd.to_numeric(
        df["cpi_value"],
        errors="coerce"
    )


    df = add_metadata(
        df,
        source_file
    )


    save_excel(
        df,
        "cpi_processed.xlsx"
    )



# ==========================
# Main
# ==========================

def main():

    create_processed_folder()


    transform_population()

    transform_unemployment()

    transform_cpi()


    print(
        "\nTransformation completed successfully."
    )



if __name__ == "__main__":

    main()