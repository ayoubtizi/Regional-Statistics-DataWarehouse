import psycopg2


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
# Execute query
# =============================

def execute_check(query):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(query)

    result = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return result


# =============================
# Check tables are not empty
# =============================

def check_table_not_empty(table):

    query = f"""
    SELECT COUNT(*)
    FROM warehouse.{table};
    """

    count = execute_check(query)

    if count == 0:
        return False, f"{table} is empty"

    return True, f"{table}: {count} rows"


# =============================
# Check NULL foreign keys
# =============================

def check_null_foreign_keys(table, column):

    query = f"""
    SELECT COUNT(*)
    FROM warehouse.{table}
    WHERE {column} IS NULL;
    """

    result = execute_check(query)

    if result > 0:
        return False, f"{table}.{column} contains {result} NULL values"

    return True, f"{table}.{column}: no NULL values"


# =============================
# Check orphan relationships
# =============================

def check_orphan_keys():

    errors = []

    query = """
    SELECT COUNT(*)
    FROM warehouse.fact_population f
    LEFT JOIN warehouse.dim_time t
    ON f.time_id = t.time_id
    WHERE t.time_id IS NULL;
    """

    result = execute_check(query)

    if result > 0:
        errors.append(
            f"fact_population has {result} missing time references"
        )

    return errors


# =============================
# Check invalid measures
# =============================

def check_negative_population():

    query = """
    SELECT COUNT(*)
    FROM warehouse.fact_population
    WHERE population_count < 0;
    """

    result = execute_check(query)

    if result > 0:
        return False, f"Population contains {result} negative values"

    return True, "Population values are valid"


# =============================
# Run checks
# =============================

def run_quality_checks():

    print("\n")
    print("=" * 60)
    print("STARTING WAREHOUSE QUALITY CHECKS")
    print("=" * 60)


    checks = []


    # Fact table existence/content

    checks.append(
        check_table_not_empty("fact_population")
    )

    checks.append(
        check_table_not_empty("fact_unemployment")
    )

    checks.append(
        check_table_not_empty("fact_cpi")
    )


    # Foreign keys

    checks.append(
        check_null_foreign_keys(
            "fact_population",
            "time_id"
        )
    )

    checks.append(
        check_null_foreign_keys(
            "fact_population",
            "geo_id"
        )
    )


    # Business rules

    checks.append(
        check_negative_population()
    )


    failed = False


    for status, message in checks:

        if status:
            print("[PASS]", message)

        else:
            print("[FAIL]", message)
            failed = True



    orphan_errors = check_orphan_keys()


    for error in orphan_errors:

        print("[FAIL]", error)
        failed = True



    print("=" * 60)


    if failed:

        raise Exception(
            "DATA QUALITY CHECK FAILED"
        )


    print(
        "WAREHOUSE QUALITY CHECK PASSED"
    )



if __name__ == "__main__":

    run_quality_checks()