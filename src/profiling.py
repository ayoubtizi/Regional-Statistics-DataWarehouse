import pandas as pd
import os


RAW_PATH = "data/raw"

# Values that may represent missing information in the source files.
# They are NOT converted during profiling.
MISSING_VALUES = [
    "-",
    "...",
    "NA",
    "N/A"
]


def profile_excel(file_path):

    print("\n" + "=" * 70)
    print(f"Dataset: {os.path.basename(file_path)}")

    # Read Excel as raw as possible.
    # header=None because we first need to understand the structure.
    #
    # keep_default_na=False:
    # Prevents pandas from automatically converting values like:
    # "NA", "N/A" into NaN.
    #
    # Real empty Excel cells remain NaN because they are empty cells.
    df = pd.read_excel(
        file_path,
        header=None,
        keep_default_na=False
    )


    # -----------------------------
    # Basic information
    # -----------------------------

    print("\nShape:")
    print(df.shape)


    print("\nFirst 15 rows:")
    print(df.head(15))


    print("\nData types:")
    print(df.dtypes)



    # -----------------------------
    # Missing values analysis
    # -----------------------------

    print("\nTrue missing values (empty Excel cells only):")
    print(df.isnull().sum())


    print("\nSpecial missing representations found:")
    
    found_special_values = False

    for value in MISSING_VALUES:

        count = (df == value).sum().sum()

        if count > 0:
            found_special_values = True
            print(f"  '{value}' : {count}")


    if not found_special_values:
        print("  No special missing values detected.")



    # -----------------------------
    # Blank spaces detection
    # -----------------------------
    
    print("\nBlank spaces:")

    blank_spaces = (
        df.astype(str)
        .apply(lambda col: col.str.strip() == "")
        .sum()
    )

    print(blank_spaces)



    # -----------------------------
    # Duplicate analysis
    # -----------------------------

    print("\nDuplicate rows:")
    print(df.duplicated().sum())



    # -----------------------------
    # Empty columns
    # -----------------------------

    print("\nCompletely empty columns:")

    empty_columns = df.columns[df.isnull().all()].tolist()

    if empty_columns:
        print(empty_columns)
    else:
        print("None")



def main():

    for file in os.listdir(RAW_PATH):

        # Ignore:
        # - non Excel files
        # - Excel temporary files (~$filename.xlsx)
        if (
            file.endswith(".xlsx")
            and not file.startswith("~$")
        ):

            file_path = os.path.join(
                RAW_PATH,
                file
            )

            profile_excel(file_path)



if __name__ == "__main__":
    main()