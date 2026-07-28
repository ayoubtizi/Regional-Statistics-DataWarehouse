import os
import pandas as pd

from src.load.database import get_connection
from src.utils.logger import start_log, update_log



# =====================================================
# Paths
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

def clean_values(rows):

    cleaned = []

    for row in rows:

        cleaned.append(
            tuple(
                value.item()
                if hasattr(value, "item")
                else value
                for value in row
            )
        )

    return cleaned



def execute_upsert(query, rows):

    rows = clean_values(rows)

    conn = get_connection()
    cursor = conn.cursor()


    inserted = 0
    updated = 0


    try:

        for row in rows:

            cursor.execute(
                query,
                row
            )


            result = cursor.fetchone()


            if result[0] == "INSERT":

                inserted += 1

            else:

                updated += 1



        conn.commit()


        return {

            "read": len(rows),

            "inserted": inserted,

            "updated": updated

        }



    except Exception as e:

        conn.rollback()

        raise e



    finally:

        cursor.close()

        conn.close()




# =====================================================
# FACT POPULATION
# =====================================================

def load_population_fact():

    print("\nLoading fact_population...")


    file_path = os.path.join(
        PROCESSED_PATH,
        "population_processed.xlsx"
    )


    df = pd.read_excel(file_path)



    df["population_count"] = pd.to_numeric(
        df["population_count"],
        errors="coerce"
    )


    df = df.dropna(
        subset=[
            "population_count",
            "year",
            "geo_name",
            "residence_type"
        ]
    )



    conn = get_connection()
    cursor = conn.cursor()


    rows = []



    for _, row in df.iterrows():


        cursor.execute(
            """
            SELECT time_id
            FROM warehouse.dim_time
            WHERE year=%s
            """,
            (
                int(row["year"]),
            )
        )

        time_id = cursor.fetchone()[0]



        cursor.execute(
            """
            SELECT geo_id
            FROM warehouse.dim_geography
            WHERE geo_name=%s
            """,
            (
                row["geo_name"],
            )
        )

        geo_id = cursor.fetchone()[0]



        cursor.execute(
            """
            SELECT residence_id
            FROM warehouse.dim_residence
            WHERE residence_type=%s
            """,
            (
                row["residence_type"],
            )
        )

        residence_id = cursor.fetchone()[0]



        rows.append(
            (
                time_id,
                geo_id,
                residence_id,
                float(row["population_count"])
            )
        )



    cursor.close()
    conn.close()



    stats = execute_upsert(

        """
        INSERT INTO warehouse.fact_population
        (
            time_id,
            geo_id,
            residence_id,
            population_count
        )

        VALUES (%s,%s,%s,%s)


        ON CONFLICT
        (
            time_id,
            geo_id,
            residence_id
        )


        DO UPDATE SET

        population_count = EXCLUDED.population_count


        RETURNING

        CASE

            WHEN xmax = 0 THEN 'INSERT'

            ELSE 'UPDATE'

        END;

        """,

        rows

    )



    print(
        f"""
fact_population completed

Rows read: {stats['read']}
Inserted: {stats['inserted']}
Updated: {stats['updated']}
"""
    )


    return stats 
# =====================================================
# FACT UNEMPLOYMENT
# =====================================================

def load_unemployment_fact():

    print("\nLoading fact_unemployment...")


    df = pd.read_excel(
        os.path.join(
            PROCESSED_PATH,
            "unemployment_processed.xlsx"
        )
    )


    conn = get_connection()
    cursor = conn.cursor()


    rows = []



    for _, row in df.iterrows():


        cursor.execute(
            """
            SELECT time_id
            FROM warehouse.dim_time
            WHERE year=%s
            """,
            (
                int(row["year"]),
            )
        )

        time_id = cursor.fetchone()[0]



        cursor.execute(
            """
            SELECT geo_id
            FROM warehouse.dim_geography
            WHERE geo_name=%s
            """,
            (
                row["geo_name"],
            )
        )

        geo_id = cursor.fetchone()[0]



        cursor.execute(
            """
            SELECT residence_id
            FROM warehouse.dim_residence
            WHERE residence_type=%s
            """,
            (
                row["residence_type"],
            )
        )

        residence_id = cursor.fetchone()[0]



        cursor.execute(
            """
            SELECT sex_id
            FROM warehouse.dim_sex
            WHERE sex_label=%s
            """,
            (
                row["sex"],
            )
        )

        sex_id = cursor.fetchone()[0]



        rows.append(
            (
                time_id,
                geo_id,
                residence_id,
                sex_id,
                float(row["unemployment_rate"])
            )
        )



    cursor.close()
    conn.close()



    stats = execute_upsert(

        """
        INSERT INTO warehouse.fact_unemployment
        (
            time_id,
            geo_id,
            residence_id,
            sex_id,
            unemployment_rate
        )


        VALUES (%s,%s,%s,%s,%s)



        ON CONFLICT
        (
            time_id,
            geo_id,
            residence_id,
            sex_id
        )



        DO UPDATE SET

        unemployment_rate = EXCLUDED.unemployment_rate



        RETURNING

        CASE

            WHEN xmax = 0 THEN 'INSERT'

            ELSE 'UPDATE'

        END;

        """,

        rows

    )



    print(
        f"""
fact_unemployment completed

Rows read: {stats['read']}
Inserted: {stats['inserted']}
Updated: {stats['updated']}
"""
    )


    return stats







# =====================================================
# FACT CPI
# =====================================================

def load_cpi_fact():

    print("\nLoading fact_cpi...")



    df = pd.read_excel(
        os.path.join(
            PROCESSED_PATH,
            "cpi_processed.xlsx"
        )
    )



    conn = get_connection()
    cursor = conn.cursor()



    rows = []



    for _, row in df.iterrows():



        cursor.execute(
            """
            SELECT time_id
            FROM warehouse.dim_time
            WHERE year=%s
            """,
            (
                int(row["year"]),
            )
        )

        time_id = cursor.fetchone()[0]



        cursor.execute(
            """
            SELECT geo_id
            FROM warehouse.dim_geography
            WHERE geo_name=%s
            """,
            (
                row["geo_name"],
            )
        )

        geo_id = cursor.fetchone()[0]



        cursor.execute(
            """
            SELECT product_id
            FROM warehouse.dim_product
            WHERE product_category=%s
            """,
            (
                row["product_category"],
            )
        )

        product_id = cursor.fetchone()[0]



        rows.append(
            (
                time_id,
                geo_id,
                product_id,
                float(row["cpi_value"])
            )
        )



    cursor.close()
    conn.close()



    stats = execute_upsert(

        """
        INSERT INTO warehouse.fact_cpi
        (
            time_id,
            geo_id,
            product_id,
            cpi_value
        )


        VALUES (%s,%s,%s,%s)



        ON CONFLICT
        (
            time_id,
            geo_id,
            product_id
        )



        DO UPDATE SET

        cpi_value = EXCLUDED.cpi_value



        RETURNING

        CASE

            WHEN xmax = 0 THEN 'INSERT'

            ELSE 'UPDATE'

        END;

        """,

        rows

    )



    print(
        f"""
fact_cpi completed

Rows read: {stats['read']}
Inserted: {stats['inserted']}
Updated: {stats['updated']}
"""
    )


    return stats
# =====================================================
# MAIN WITH ETL LOGGING
# =====================================================

if __name__ == "__main__":


    log_id = start_log(
        "FACTS_LOADING",
        "processed_files"
    )


    try:

        print(
            "Starting fact loading..."
        )


        population_stats = load_population_fact()

        unemployment_stats = load_unemployment_fact()

        cpi_stats = load_cpi_fact()



        total_read = (
            population_stats["read"]
            +
            unemployment_stats["read"]
            +
            cpi_stats["read"]
        )


        total_inserted = (
            population_stats["inserted"]
            +
            unemployment_stats["inserted"]
            +
            cpi_stats["inserted"]
        )


        total_updated = (
            population_stats["updated"]
            +
            unemployment_stats["updated"]
            +
            cpi_stats["updated"]
        )



        print(
            f"""
==================================================
FACT LOADING SUMMARY
==================================================

Rows read:
{total_read}

Inserted:
{total_inserted}

Updated:
{total_updated}

==================================================
"""
        )



        update_log(

            log_id,

            total_read,

            "SUCCESS"

        )



        print(
            "All facts loaded successfully"
        )



    except Exception as e:


        update_log(

            log_id,

            0,

            "FAILED",

            str(e)

        )


        raise e