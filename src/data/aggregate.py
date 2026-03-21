import pandas as pd

def aggregate_weekly_orders(df: pd.DataFrame) -> pd.DataFrame:
    # aggregates weekly invoice data into a single dataset
    df = df.copy()
    
    # group by sku and week
    weekly = (
        df.groupby(["item_name", pd.Grouper(key="date", freq="W-MON")])
        .agg({"quantity_clean": "sum"})
        .reset_index()
    )
    
    weekly["quantity_clean"] = weekly["quantity_clean"].fillna(0)
    weekly = weekly.sort_values(["item_name", "date"])
    
    return weekly

if __name__ == "__main__":
    input_path = "../../data/processed/all_sales_clean.csv"
    output_path = "../../data/processed/weekly_orders_clean.csv"
    
    print(f"Aggregating weekly demand from {input_path}...")
    df = pd.read_csv(input_path)
    df["date"] = pd.to_datetime(df["date"])
    
    weekly_df = aggregate_weekly_orders(df)
    weekly_df.to_csv(output_path, index=False)
    print(f"Aggregated weekly orders saved to {output_path}")
