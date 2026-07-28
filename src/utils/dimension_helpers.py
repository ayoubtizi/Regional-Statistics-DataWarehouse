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



def execute_dimension_insert(query, rows, get_connection):

    rows = clean_values(rows)


    conn = get_connection()
    cursor = conn.cursor()


    inserted = 0
    skipped = 0


    try:

        for row in rows:

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

            "read": len(rows),
            "inserted": inserted,
            "skipped": skipped

        }



    except Exception as e:

        conn.rollback()
        raise e



    finally:

        cursor.close()
        conn.close()