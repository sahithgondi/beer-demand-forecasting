import os
from pathlib import Path
import pandas as pd

# defining io directories and output file path
BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "data/raw"
OUT_DIR = BASE_DIR / "data/processed"
OUT_FILE = OUT_DIR / "all_sales.csv"

# mapping from original col names to standardized col names
COLUMN_MAP = {
    "sku": "sku",
    "itemName": "item_name",
    "unitUpc": "unit_upc",
    "caseUpc": "case_upc",
    "quantity": "quantity",
    "unitPrice": "unit_price",
    "total": "total_sales",
}

#columns that must exist in every input csv
REQUIRED_COLUMNS = [
    "sku",
    "itemName",
    "quantity",
    "unitPrice",
    "total",
]


def extract_date_from_filename(filename: str) -> str:
    # extracts date from filename
    return Path(filename).stem #removes file extension


def load_one_file(path: Path) -> pd.DataFrame:
    # loads and cleans a single csv file
    df = pd.read_csv(path, sep=";") # read csv into df sep by ; not ,

   # print("RAW COLUMNS:", df.columns.tolist())

    #need to clean col names
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.replace('\ufeff', '', regex = False)

    # col check
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"{path.name} is missing required columns: {missing}")

    # add a date column that comes from filename
    df["date"] = pd.to_datetime(extract_date_from_filename(path.name), format="%Y-%m-%d")

    # rename cols to stadnardized cols
    df = df.rename(columns=COLUMN_MAP)

    #final order ####################################
    """
    """
    keep_cols = [
        "date",
        "sku",
        "item_name",
        "unit_upc",
        "case_upc",
        "quantity",
        "unit_price",
        "total_sales",
    ]

    # make sure all cols exist and adds missing as NA
    for col in keep_cols:
        if col not in df.columns:
            df[col] = pd.NA

    # to keep only the relevant cols
    df = df[keep_cols].copy()

    # clean and normalize
    df["sku"] = df["sku"].astype(str).str.strip()
    df["item_name"] = df["item_name"].astype(str).str.strip()
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    df["total_sales"] = pd.to_numeric(df["total_sales"], errors="coerce")

    return df


def main() -> None:
    """
    Main pipeline:
    load all csvs
    clean them
    combine into one dataset
    save output
    """

    # create out dir if not exist
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # get all csv files from raw
    csv_files = sorted(RAW_DIR.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError("No CSV files found in data/raw")

    dfs = [load_one_file(path) for path in csv_files]
    all_sales = pd.concat(dfs, ignore_index=True).sort_values(["date", "sku", "item_name"])

    all_sales.to_csv(OUT_FILE, index=False)

    #print summary of info
    print(f"Saved {len(all_sales)} rows to {OUT_FILE}")
    print("Date range:", all_sales["date"].min(), "to", all_sales["date"].max())
    print("Unique SKUs:", all_sales["sku"].nunique())


if __name__ == "__main__":
    main()