import os
import pandas as pd

from src.load.database import get_connection
from src.utils.logger import start_log, update_log



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
# Helpers
# =====================================================

def clean_values(values):

    cleaned_values = []


    for row in values:

        cleaned_values.append(

            tuple(
                value.item()
                if hasattr(value, "item")
                else value

                for value in row
            )

        )


    return cleaned_values




def execute_dimension_insert(query, values):


    values = clean_values(values)


    conn = get_connection()
    cursor = conn.cursor()


    inserted = 0
    skipped = 0



    try:


        for row in values:


            cursor.execute(
                query,
                row
            )


            if cursor.rowcount == 1:

                inserted += 1

            else:

                skipped += 1



        conn.commit()



        return {

            "read": len(values),

            "inserted": inserted,

            "skipped": skipped

        }



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
            int(year),
            int((year // 10) * 10)
        )

        for year in years

    ]



    stats = execute_dimension_insert(

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
        f"""
dim_time completed

Rows read: {stats['read']}
Inserted: {stats['inserted']}
Skipped: {stats['skipped']}
"""
    )


    return stats





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



    stats = execute_dimension_insert(

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
        f"""
dim_geography completed

Rows read: {stats['read']}
Inserted: {stats['inserted']}
Skipped: {stats['skipped']}
"""
    )


    return stats





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



    stats = execute_dimension_insert(

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
        f"""
dim_residence completed

Rows read: {stats['read']}
Inserted: {stats['inserted']}
Skipped: {stats['skipped']}
"""
    )


    return stats
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



    stats = execute_dimension_insert(

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
        f"""
dim_sex completed

Rows read: {stats['read']}
Inserted: {stats['inserted']}
Skipped: {stats['skipped']}
"""
    )


    return stats







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



    stats = execute_dimension_insert(

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
        f"""
dim_product completed

Rows read: {stats['read']}
Inserted: {stats['inserted']}
Skipped: {stats['skipped']}
"""
    )


    return stats






# =====================================================
# MAIN PIPELINE WITH LOGGING
# =====================================================

if __name__ == "__main__":


    log_id = start_log(
        "DIMENSIONS_LOADING",
        "processed_files"
    )



    try:


        print(
            "Starting dimension loading..."
        )



        time_stats = load_time_dimension()

        geo_stats = load_geography_dimension()

        residence_stats = load_residence_dimension()

        sex_stats = load_sex_dimension()

        product_stats = load_product_dimension()



        total_read = (

            time_stats["read"]

            +
            geo_stats["read"]

            +
            residence_stats["read"]

            +
            sex_stats["read"]

            +
            product_stats["read"]

        )



        total_inserted = (

            time_stats["inserted"]

            +
            geo_stats["inserted"]

            +
            residence_stats["inserted"]

            +
            sex_stats["inserted"]

            +
            product_stats["inserted"]

        )



        total_skipped = (

            time_stats["skipped"]

            +
            geo_stats["skipped"]

            +
            residence_stats["skipped"]

            +
            sex_stats["skipped"]

            +
            product_stats["skipped"]

        )



        print(
            f"""
==================================================
DIMENSION LOADING SUMMARY
==================================================

Rows read:
{total_read}

Inserted:
{total_inserted}

Skipped:
{total_skipped}

==================================================
"""
        )



        update_log(

            log_id,

            total_read,

            "SUCCESS"

        )



        print(
            "All dimensions loaded successfully"
        )



    except Exception as e:


        update_log(

            log_id,

            0,

            "FAILED",

            str(e)

        )


        raise e        