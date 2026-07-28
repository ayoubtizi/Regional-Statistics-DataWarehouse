import subprocess
import sys



def run_step(command, name):

    print("\n" + "=" * 60)
    print(f"Running {name}")
    print("=" * 60)


    result = subprocess.run(
        command,
        text=True
    )


    if result.returncode != 0:

        raise Exception(
            f"{name} failed"
        )



def main():

    print("\nSTARTING COMPLETE ETL PIPELINE")


    try:


        run_step(
            [
                sys.executable,
                "-m",
                "src.ingestion"
            ],
            "Data Ingestion and Validation"
        )


        run_step(
            [
                sys.executable,
                "-m",
                "src.transformation"
            ],
            "Data Transformation"
        )


        run_step(
            [
                sys.executable,
                "-m",
                "src.load.load_dimensions"
            ],
            "Dimension Loading"
        )


        run_step(
            [
                sys.executable,
                "-m",
                "src.load.load_facts"
            ],
            "Fact Loading"
        )


        run_step(
            [
                sys.executable,
                "-m",
                "src.quality.warehouse_checks"
            ],
            "Warehouse Quality Checks"
        )


        run_step(
            [
                sys.executable,
                "-m",
                "src.analytics.run_analytics"
            ],
            "Analytics Report Generation"
        )


        run_step(
            [
                sys.executable,
                "-m",
                "src.reports.export_etl_logs"
            ],
            "ETL Logs Report Generation"
        )


        print("\n" + "=" * 60)
        print("ETL PIPELINE COMPLETED SUCCESSFULLY")
        print("=" * 60)



    except Exception as e:

        print("\nPIPELINE FAILED")
        print(e)

        raise e




if __name__ == "__main__":

    main()