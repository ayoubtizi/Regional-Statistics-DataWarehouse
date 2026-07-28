import os
import pandas as pd

from database import get_connection


# =====================================================
# Project paths
# =====================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

PROCESSED_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed"
)


# =====================================================
# Load dimension helper
# =====================================================

def execute_insert(query, values):

    # Convert numpy data types to Python native types
    cleaned_values = []

    for row in values:

        cleaned_row = tuple(
            value.item()
            if hasattr(value, "item")
            else value
            for value in row
        )

        cleaned_values.append(cleaned_row)


    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.executemany(
            query,
            cleaned_values
        )

        conn.commit()


    except Exception as e:

        conn.rollback()
        raise e


    finally:

        cursor.close()
        conn.close()

# =====================================================
# dim_time
# =====================================================

def load_time_dimension():

    files = [
        "population_processed.xlsx",
        "unemployment_processed.xlsx",
        "cpi_processed.xlsx"
    ]


    years = set()


    for file in files:

        path = os.path.join(
            PROCESSED_PATH,
            file
        )

        df = pd.read_excel(path)

        years.update(
            df["year"]
            .dropna()
            .astype(int)
            .unique()
        )


    values = [

        (
            year,
            (year // 10) * 10
        )

        for year in years

    ]


    execute_insert(

        """
        INSERT INTO warehouse.dim_time
        (
            year,
            decade
        )

        VALUES (%s,%s)

        ON CONFLICT(year)
        DO NOTHING;
        """,

        values
    )


    print(
        f"dim_time loaded: {len(values)} rows"
    )



# =====================================================
# dim_geography
# =====================================================

def load_geography_dimension():

    files = [
        "population_processed.xlsx",
        "unemployment_processed.xlsx",
        "cpi_processed.xlsx"
    ]


    geography = set()


    for file in files:

        path = os.path.join(
            PROCESSED_PATH,
            file
        )

        df = pd.read_excel(path)


        geography.update(
            df["geo_name"]
            .dropna()
            .unique()
        )


    values = [

        (geo,)

        for geo in geography

    ]


    execute_insert(

        """
        INSERT INTO warehouse.dim_geography
        (
            geo_name
        )

        VALUES (%s)

        ON CONFLICT(geo_name)
        DO NOTHING;
        """,

        values
    )


    print(
        f"dim_geography loaded: {len(values)} rows"
    )



# =====================================================
# dim_residence
# =====================================================

def load_residence_dimension():

    path = os.path.join(
        PROCESSED_PATH,
        "population_processed.xlsx"
    )


    df = pd.read_excel(path)


    values = [

        (value,)

        for value in
        df["residence_type"]
        .dropna()
        .unique()

    ]


    execute_insert(

        """
        INSERT INTO warehouse.dim_residence
        (
            residence_type
        )

        VALUES (%s)

        ON CONFLICT(residence_type)
        DO NOTHING;
        """,

        values
    )


    print(
        f"dim_residence loaded: {len(values)} rows"
    )



# =====================================================
# dim_sex
# =====================================================

def load_sex_dimension():

    path = os.path.join(
        PROCESSED_PATH,
        "unemployment_processed.xlsx"
    )


    df = pd.read_excel(path)


    values = [

        (value,)

        for value in
        df["sex"]
        .dropna()
        .unique()

    ]


    execute_insert(

        """
        INSERT INTO warehouse.dim_sex
        (
            sex_label
        )

        VALUES (%s)

        ON CONFLICT(sex_label)
        DO NOTHING;
        """,

        values
    )


    print(
        f"dim_sex loaded: {len(values)} rows"
    )



# =====================================================
# dim_product
# =====================================================

def load_product_dimension():

    path = os.path.join(
        PROCESSED_PATH,
        "cpi_processed.xlsx"
    )


    df = pd.read_excel(path)


    values = [

        (value,)

        for value in
        df["product_category"]
        .dropna()
        .unique()

    ]


    execute_insert(

        """
        INSERT INTO warehouse.dim_product
        (
            product_category
        )

        VALUES (%s)

        ON CONFLICT(product_category)
        DO NOTHING;
        """,

        values
    )


    print(
        f"dim_product loaded: {len(values)} rows"
    )



# =====================================================
# Main pipeline
# =====================================================

if __name__ == "__main__":


    print("Starting dimension loading...")


    load_time_dimension()

    load_geography_dimension()

    load_residence_dimension()

    load_sex_dimension()

    load_product_dimension()


    print(
        "All dimensions loaded successfully"
    )