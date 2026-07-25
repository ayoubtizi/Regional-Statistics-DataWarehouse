import pandas as pd
import os


RAW_PATH = "data/raw"

# Values considered as missing
MISSING_VALUES = [
    "-",
    "...",
    "NA",
    "N/A",
    "",
    " "
]


def profile_excel(file_path):

    print("\n" + "=" * 70)
    print(f"Dataset: {file_path}")

    # Read Excel without assuming headers
    # because we need to discover the structure first
    df = pd.read_excel(
        file_path,
        header=None,
        na_values=MISSING_VALUES
    )

    print("\nShape:")
    print(df.shape)

    print("\nFirst 15 rows:")
    print(df.head(15))

    print("\nData types:")
    print(df.dtypes)

    print("\nMissing values (including '-', '...', 'N/A', blanks):")
    print(df.isnull().sum())

    print("\nSpecial missing values before conversion:")

    for value in MISSING_VALUES:
        count = (df == value).sum().sum()
        if count > 0:
            print(f"{value}: {count}")

    print("\nDuplicate rows:")
    print(df.duplicated().sum())

    print("\nCompletely empty columns:")
    print(df.columns[df.isnull().all()].tolist())


def main():

    for file in os.listdir(RAW_PATH):

        if file.endswith(".xlsx"):

            file_path = os.path.join(
                RAW_PATH,
                file
            )

            profile_excel(file_path)


if __name__ == "__main__":
    main()