from src.utils.logger import start_log, update_log



log_id = start_log(
    "TEST_PROCESS",
    "test.xlsx"
)


print(
    "Created log:",
    log_id
)



update_log(
    log_id,
    100,
    "SUCCESS"
)


print(
    "Updated log"
)