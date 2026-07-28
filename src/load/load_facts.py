import os
import pandas as pd

from database import get_connection


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



def execute_insert(query, rows):

    rows = clean_values(rows)

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.executemany(
            query,
            rows
        )

        conn.commit()


    except Exception as e:

        conn.rollback()
        print("Insert failed:")
        print(e)

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

        time = cursor.fetchone()

        if time is None:
            raise Exception(
                f"Missing year dimension: {row['year']}"
            )

        time_id = time[0]



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

        geo = cursor.fetchone()

        if geo is None:
            raise Exception(
                f"Missing geography: {row['geo_name']}"
            )

        geo_id = geo[0]



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

        residence = cursor.fetchone()

        if residence is None:
            raise Exception(
                f"Missing residence: {row['residence_type']}"
            )

        residence_id = residence[0]



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



    # Debug before insertion

    print("\nFirst 10 rows:")

    for r in rows[:10]:
        print(r)


    print(
        "\nMaximum population value:",
        max(
            r[3]
            for r in rows
        )
    )


    execute_insert(

        """
        INSERT INTO warehouse.fact_population
        (
            time_id,
            geo_id,
            residence_id,
            population_count
        )

        VALUES (%s,%s,%s,%s);
        """,

        rows

    )


    print(
        f"fact_population loaded: {len(rows)} rows"
    )



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


    conn=get_connection()
    cursor=conn.cursor()

    rows=[]


    for _,row in df.iterrows():


        cursor.execute(
            """
            SELECT time_id FROM warehouse.dim_time
            WHERE year=%s
            """,
            (
                int(row["year"]),
            )
        )

        time_id=cursor.fetchone()[0]



        cursor.execute(
            """
            SELECT geo_id FROM warehouse.dim_geography
            WHERE geo_name=%s
            """,
            (
                row["geo_name"],
            )
        )

        geo_id=cursor.fetchone()[0]



        cursor.execute(
            """
            SELECT residence_id FROM warehouse.dim_residence
            WHERE residence_type=%s
            """,
            (
                row["residence_type"],
            )
        )

        residence_id=cursor.fetchone()[0]



        cursor.execute(
            """
            SELECT sex_id FROM warehouse.dim_sex
            WHERE sex_label=%s
            """,
            (
                row["sex"],
            )
        )

        sex_id=cursor.fetchone()[0]



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



    execute_insert(

        """
        INSERT INTO warehouse.fact_unemployment
        (
            time_id,
            geo_id,
            residence_id,
            sex_id,
            unemployment_rate
        )

        VALUES (%s,%s,%s,%s,%s);
        """,

        rows
    )


    print(
        f"fact_unemployment loaded: {len(rows)} rows"
    )



# =====================================================
# FACT CPI
# =====================================================

def load_cpi_fact():

    print("\nLoading fact_cpi...")


    df=pd.read_excel(
        os.path.join(
            PROCESSED_PATH,
            "cpi_processed.xlsx"
        )
    )


    conn=get_connection()
    cursor=conn.cursor()

    rows=[]


    for _,row in df.iterrows():


        cursor.execute(
            """
            SELECT time_id FROM warehouse.dim_time
            WHERE year=%s
            """,
            (
                int(row["year"]),
            )
        )

        time_id=cursor.fetchone()[0]



        cursor.execute(
            """
            SELECT geo_id FROM warehouse.dim_geography
            WHERE geo_name=%s
            """,
            (
                row["geo_name"],
            )
        )

        geo_id=cursor.fetchone()[0]



        cursor.execute(
            """
            SELECT product_id FROM warehouse.dim_product
            WHERE product_category=%s
            """,
            (
                row["product_category"],
            )
        )

        product_id=cursor.fetchone()[0]



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



    execute_insert(

        """
        INSERT INTO warehouse.fact_cpi
        (
            time_id,
            geo_id,
            product_id,
            cpi_value
        )

        VALUES (%s,%s,%s,%s);
        """,

        rows
    )


    print(
        f"fact_cpi loaded: {len(rows)} rows"
    )



# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    print(
        "Starting fact loading..."
    )


    load_population_fact()

    load_unemployment_fact()

    load_cpi_fact()


    print(
        "\nAll facts loaded successfully"
    )