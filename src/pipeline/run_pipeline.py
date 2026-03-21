import sys
import os
import pandas as pd

# make sure python can find the src modules no matter where the script is ran from
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.data.clean import clean_data
from src.data.aggregate import aggregate_weekly_orders
from src.features.build_features import build_all_features
from src.models.train import train_model, save_model
from src.models.evaluate import evaluate_model
from src.utils.logger import log_experiment

def main():
    print("Starting Beer Demand Forecasting Pipeline...\n")
    
    # load raw data
    data_path = "data/processed/all_sales.csv"
    print(f"Loading raw dataset from {data_path}...")
    df = pd.read_csv(data_path)
    df["date"] = pd.to_datetime(df["date"])
    
    # clean data
    print("Cleaning data and handling returns...")
    df_clean = clean_data(df)
    
    # aggregate
    print("Aggregating daily invoices into weekly demand...")
    df_weekly = aggregate_weekly_orders(df_clean)
    
    # build features
    print("Building features...")
    df_features = build_all_features(df_weekly)
    
    # train test split (80/20) based on time
    print("Splitting data (80% train, 20% test)...")
    split_date = df_features["date"].quantile(0.8)
    train = df_features[df_features["date"] < split_date]
    test  = df_features[df_features["date"] >= split_date]
    
    # context features
    features = ["lag_1", "lag_2", "lag_4", "rolling_mean_4", "rolling_std_4", "week", "month", "quarter"]
    target = "quantity_clean"
    model_type = "linear_regression"
    
    X_train, y_train = train[features], train[target]
    X_test, y_test = test[features], test[target]
    
    # train the model   
    model = train_model(X_train, y_train, model_type=model_type)
    
    # evaluate the model
    metrics = evaluate_model(model, X_test, y_test)
    print(f"Metrics -> MAE: {metrics['mae']:.4f} | RMSE: {metrics['rmse']:.4f} | WMAPE: {metrics['wmape']:.2%}")
    
    # log the experiment
    notes = "Fully end to end pipeline run"
    experiment_id = log_experiment(
        model_type=model_type,
        features=features,
        mae=metrics["mae"],
        rmse=metrics["rmse"],
        wmape=metrics["wmape"],
        notes=notes
    )
    
    # save the model
    save_model(model, model_type, experiment_id)
    
    print("\nPipeline completed successfully!")

if __name__ == "__main__":
    main()
