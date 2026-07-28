import subprocess
import sys



def run_step(command, name):

    print("\n" + "="*50)
    print(f"Running {name}")
    print("="*50)


    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )


    print(result.stdout)


    if result.returncode != 0:

        print(result.stderr)

        raise Exception(
            f"{name} failed"
        )



def main():


    print("Starting complete ETL pipeline")


    try:


        # 1. Load dimensions

        run_step(
            [
                sys.executable,
                "-m",
                "src.load.load_dimensions"
            ],
            "Dimension Loading"
        )



        # 2. Load facts

        run_step(
            [
                sys.executable,
                "-m",
                "src.load.load_facts"
            ],
            "Fact Loading"
        )



        # 3. Generate Excel report

        run_step(
            [
                sys.executable,
                "-m",
                "src.reports.export_etl_logs"
            ],
            "ETL Report Generation"
        )



        print(
            "\nETL PIPELINE COMPLETED SUCCESSFULLY"
        )



    except Exception as e:

        print(
            "\nPIPELINE FAILED"
        )

        print(e)

        raise e




if __name__ == "__main__":

    main()