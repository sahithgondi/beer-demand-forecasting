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

# columns that must exist in every input csv
REQUIRED_COLUMNS = [
    "sku",
    "itemName",
    "quantity",
    "unitPrice",
    "total",
]


def extract_date_from_filename(filename: str) -> str:
    # extracts date from filename
    return Path(filename).stem


def load_one_file(path: Path) -> pd.DataFrame:
    # simply loads a single csv file and standardizes columns
    df = pd.read_csv(path, sep=";") 

    # strip headers to prevent key errors
    df.columns = df.columns.str.strip().str.replace('\ufeff', '', regex=False)

    # col check
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"{path.name} is missing required columns: {missing}")

    # add a date column that comes from filename
    df["date"] = pd.to_datetime(extract_date_from_filename(path.name), format="%Y-%m-%d")

    # rename cols to standardized cols
    df = df.rename(columns=COLUMN_MAP)

    keep_cols = [
        "date", "sku", "item_name", "unit_upc",
        "case_upc", "quantity", "unit_price", "total_sales",
    ]

    for col in keep_cols:
        if col not in df.columns:
            df[col] = pd.NA

    # pass the raw combined columns without doing data type cleaning (handled by clean.py now)
    df = df[keep_cols].copy()

    return df


def main() -> None:
    # main pipeline load all raaw csvs and dump into all_sales.csv
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    csv_files = sorted(RAW_DIR.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError("No CSV files found in data/raw")

    dfs = [load_one_file(path) for path in csv_files]
    all_sales = pd.concat(dfs, ignore_index=True).sort_values(["date", "sku", "item_name"])

    all_sales.to_csv(OUT_FILE, index=False)

    print(f"Saved {len(all_sales)} raw rows to {OUT_FILE}")


if __name__ == "__main__":
    main()