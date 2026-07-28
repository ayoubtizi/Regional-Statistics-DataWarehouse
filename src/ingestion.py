import os
import shutil
import csv
from datetime import datetime

from src.validation import validate_file, load_rules


# =============================
# Paths
# =============================

INCOMING_PATH = "data/incoming"
RAW_PATH = "data/raw"
REJECTED_PATH = "data/rejected"

LOG_PATH = "reports/ingestion_log.csv"



# =============================
# Create folders
# =============================

def create_directories():

    folders = [
        INCOMING_PATH,
        RAW_PATH,
        REJECTED_PATH,
        "reports"
    ]

    for folder in folders:

        os.makedirs(
            folder,
            exist_ok=True
        )



# =============================
# Logging
# =============================

def write_log(
        filename,
        status,
        message,
        location
):

    file_exists = os.path.isfile(LOG_PATH)


    with open(
        LOG_PATH,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:


        writer = csv.writer(file)


        # Create header only once
        if not file_exists:

            writer.writerow(
                [
                    "timestamp",
                    "file",
                    "status",
                    "message",
                    "location"
                ]
            )


        writer.writerow(
            [
                datetime.now(),
                filename,
                status,
                message,
                location
            ]
        )



# =============================
# Move files
# =============================

def move_file(
        file_path,
        destination
):

    filename = os.path.basename(file_path)

    new_path = os.path.join(
        destination,
        filename
    )


    shutil.move(
        file_path,
        new_path
    )


    return new_path



# =============================
# Main ingestion pipeline
# =============================

def run_ingestion():


    print("\n" + "="*60)
    print("STARTING INGESTION PIPELINE")
    print("="*60)



    create_directories()



    rules = load_rules()



    files = os.listdir(
        INCOMING_PATH
    )


    # Remove temporary files and folders

    files = [
        file for file in files
        if (
            os.path.isfile(
                os.path.join(INCOMING_PATH, file)
            )
            and not file.startswith("~$")
        )
    ]



    if not files:

        print(
            "No files found in incoming folder."
        )

        return



    for file in files:


        file_path = os.path.join(
            INCOMING_PATH,
            file
        )


        print(
            f"\nProcessing: {file}"
        )



        # -------------------------
        # Validation step
        # -------------------------

        is_valid, message = validate_file(
            file_path,
            rules
        )



        # -------------------------
        # Valid file
        # -------------------------

        if is_valid:


            new_location = move_file(
                file_path,
                RAW_PATH
            )


            print(
                "✅ Accepted → data/raw/"
            )


            write_log(
                file,
                "SUCCESS",
                message,
                new_location
            )



        # -------------------------
        # Invalid file
        # -------------------------

        else:


            new_location = move_file(
                file_path,
                REJECTED_PATH
            )


            print(
                "❌ Rejected → data/rejected/"
            )


            write_log(
                file,
                "FAILED",
                message,
                new_location
            )



    print("\n")
    print("="*60)
    print("INGESTION COMPLETED")
    print("="*60)



# =============================
# Run script
# =============================

if __name__ == "__main__":
    run_ingestion()