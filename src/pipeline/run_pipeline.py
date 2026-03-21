import sys
import os
import pandas as pd

# Ensure Python can find our 'src' modules regardless of execution directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.features.build_features import build_all_features
from src.models.train import train_model, save_model
from src.models.evaluate import evaluate_model
from src.utils.logger import log_experiment

def main():
    print("Starting Modular Beer Demand Forecasting Pipeline...\n")
    
    # load clean data
    data_path = "data/processed/weekly_orders_clean.csv"
    print(f"Loading dataset from {data_path}...")
    raw_df = pd.read_csv(data_path)
    
    # build features
    df = build_all_features(raw_df)
    
    # train test split (80/20) based on time
    print("Splitting data (80% train, 20% test)...")
    split_date = df["date"].quantile(0.8)
    train = df[df["date"] < split_date]
    test  = df[df["date"] >= split_date]
    
    #  context features
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
    notes = "Fully modularized pipeline run"
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
