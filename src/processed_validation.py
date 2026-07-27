import pandas as pd
import os


PROCESSED_PATH = "data/processed"


def validate_file(file, required_columns):

    path = os.path.join(
        PROCESSED_PATH,
        file
    )

    print("\n" + "="*60)
    print(file)


    df = pd.read_excel(path)


    # Columns check
    missing_columns = set(required_columns) - set(df.columns)

    if missing_columns:
        print("Missing columns:", missing_columns)
    else:
        print("Columns: OK")


    # Empty rows
    print(
        "Empty rows:",
        df.isnull().all(axis=1).sum()
    )


    # Duplicate rows
    print(
        "Duplicates:",
        df.duplicated().sum()
    )


    # Datatypes
    print("\nTypes:")
    print(df.dtypes)



def main():

    validate_file(
        "population_processed.xlsx",
        [
            "geo_name",
            "residence_type",
            "year",
            "population_count"
        ]
    )


    validate_file(
        "unemployment_processed.xlsx",
        [
            "geo_name",
            "residence_type",
            "sex",
            "year",
            "unemployment_rate"
        ]
    )


    validate_file(
        "cpi_processed.xlsx",
        [
            "geo_name",
            "product_category",
            "year",
            "cpi_value"
        ]
    )


if __name__ == "__main__":
    main()