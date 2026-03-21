import pandas as pd

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    # cleans datatypes, handles missing columns, and clips neg vals (returns)
    df = df.copy()
    
    # clean and normalize datatypes
    df["sku"] = df["sku"].astype(str).str.strip()
    df["item_name"] = df["item_name"].astype(str).str.strip()
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0)
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    df["total_sales"] = pd.to_numeric(df["total_sales"], errors="coerce")
    
    # any neg is clipped to 0 since demand can not be neg
    df["quantity_clean"] = df["quantity"].clip(lower=0)
    
    return df

if __name__ == "__main__":
    input_path = "../../data/processed/all_sales.csv"
    output_path = "../../data/processed/all_sales_clean.csv"
    
    print(f"Cleaning {input_path}...")
    df = pd.read_csv(input_path)
    df["date"] = pd.to_datetime(df["date"])
    
    cleaned_df = clean_data(df)
    cleaned_df.to_csv(output_path, index=False)
    print(f"Cleaned data saved to {output_path}")
