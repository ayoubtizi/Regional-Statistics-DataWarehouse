import os
import psycopg2
import pandas as pd


# =============================
# Database connection
# =============================

def get_connection():

    return psycopg2.connect(

        host="localhost",
        database="data_engineering_lab",
        user="postgres",
        password="Ayoub1234",
        port="5432"

    )


# =============================
# Execute SQL query file
# =============================

def execute_sql_file(sql_file):

    with open(
        sql_file,
        "r",
        encoding="utf-8"
    ) as file:

        query = file.read()


    conn = get_connection()


    df = pd.read_sql_query(
        query,
        conn
    )


    conn.close()


    return df



# =============================
# Export Excel report
# =============================

def export_report(df, sql_file):

    output_folder = "reports/analytics"


    os.makedirs(
        output_folder,
        exist_ok=True
    )


    filename = os.path.basename(sql_file)


    filename = filename.replace(
        ".sql",
        ".xlsx"
    )


    output_path = os.path.join(
        output_folder,
        filename
    )


    df.to_excel(
        output_path,
        index=False
    )


    return output_path



# =============================
# Run analytics layer
# =============================

def run_analytics():


    print("\n")
    print("=" * 60)
    print("STARTING ANALYTICS GENERATION")
    print("=" * 60)


    sql_folder = "sql/analytics"


    if not os.path.exists(sql_folder):

        raise Exception(
            "Analytics SQL folder not found"
        )



    sql_files = [

        file for file in os.listdir(sql_folder)

        if file.endswith(".sql")

    ]



    if not sql_files:

        raise Exception(
            "No SQL analytics files found"
        )



    for file in sql_files:


        sql_path = os.path.join(
            sql_folder,
            file
        )


        print(
            f"\nExecuting: {file}"
        )


        df = execute_sql_file(
            sql_path
        )


        output = export_report(
            df,
            sql_path
        )


        print(
            f"Created: {output}"
        )



    print("\n")
    print("=" * 60)
    print("ANALYTICS GENERATION COMPLETED")
    print("=" * 60)



if __name__ == "__main__":

    run_analytics()