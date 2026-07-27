import os
import pandas as pd
import yaml


INCOMING_PATH = "data/incoming"

RULES_PATH = "config/validation_rules.yaml"


SUPPORTED_EXTENSIONS = [
    ".xlsx",
    ".csv",
    ".json"
]


def load_rules():

    with open(RULES_PATH, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)



def check_extension(file):

    extension = os.path.splitext(file)[1].lower()

    return extension in SUPPORTED_EXTENSIONS



def read_file(file_path):

    extension = os.path.splitext(file_path)[1].lower()


    if extension == ".xlsx":

        return pd.read_excel(
            file_path,
            header=None,
            keep_default_na=False
        )


    elif extension == ".csv":

        return pd.read_csv(
            file_path,
            header=None
        )


    elif extension == ".json":

        return pd.read_json(file_path)



def detect_dataset_type(filename):

    filename = filename.lower()


    if "population" in filename:
        return "population"


    elif "unemployment" in filename:
        return "unemployment_rate"


    elif (
        "consumer" in filename
        or "price" in filename
        or "cpi" in filename
    ):
        return "consumer_price_index"


    return None



def validate_schema(df, dataset_type, rules):


    required_keywords = (
        rules["datasets"]
        [dataset_type]
        ["keywords"]
    )


    content = df.astype(str).to_string()


    for keyword in required_keywords:

        if keyword not in content:

            return False, f"Missing keyword: {keyword}"


    return True, "Schema valid"



def validate_file(file_path, rules):


    filename = os.path.basename(file_path)


    print("\nChecking:", filename)



    # Extension check

    if not check_extension(filename):

        return False, "Unsupported extension"



    # Read file

    try:

        df = read_file(file_path)

    except Exception as e:

        return False, f"Cannot read file: {e}"



    # Detect dataset

    dataset_type = detect_dataset_type(filename)


    if dataset_type is None:

        return False, "Unknown dataset"



    # Schema validation

    return validate_schema(
        df,
        dataset_type,
        rules
    )



def validate_all_files():


    rules = load_rules()


    results = []


    for file in os.listdir(INCOMING_PATH):


        file_path = os.path.join(
            INCOMING_PATH,
            file
        )


        if os.path.isfile(file_path):


            status, message = validate_file(
                file_path,
                rules
            )


            results.append(
                {
                    "file": file,
                    "status": status,
                    "message": message
                }
            )



    return results




if __name__ == "__main__":


    validation_results = validate_all_files()


    print("\n" + "="*50)
    print("VALIDATION REPORT")
    print("="*50)


    for result in validation_results:


        if result["status"]:

            print(
                f"✅ {result['file']} : {result['message']}"
            )


        else:

            print(
                f"❌ {result['file']} : {result['message']}"
            )