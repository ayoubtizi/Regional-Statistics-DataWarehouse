from datetime import datetime
from src.load.database import get_connection



def start_log(process_name, source_file):

    conn = get_connection()
    cursor = conn.cursor()


    query = """
    INSERT INTO warehouse.etl_logs
    (
        process_name,
        source_file,
        status,
        start_time
    )

    VALUES (%s,%s,%s,%s)

    RETURNING log_id;
    """


    cursor.execute(
        query,
        (
            process_name,
            source_file,
            "RUNNING",
            datetime.now()
        )
    )


    log_id = cursor.fetchone()[0]


    conn.commit()

    cursor.close()
    conn.close()


    return log_id





def update_log(
        log_id,
        rows_processed,
        status,
        error_message=None
):

    conn = get_connection()
    cursor = conn.cursor()


    query = """
    UPDATE warehouse.etl_logs

    SET

        rows_processed=%s,

        status=%s,

        error_message=%s,

        end_time=%s


    WHERE log_id=%s;
    """


    cursor.execute(
        query,
        (
            rows_processed,
            status,
            error_message,
            datetime.now(),
            log_id
        )
    )


    conn.commit()

    cursor.close()
    conn.close()