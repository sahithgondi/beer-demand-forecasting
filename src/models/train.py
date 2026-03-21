import os
import joblib
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

def wmape(y_true, y_pred):
    # calculates WMAPE
    if np.sum(y_true) == 0:
        return 0.0
    return np.sum(np.abs(y_true - y_pred)) / np.sum(y_true)


def train_model(X_train, y_train, model_type="linear_regression"):
    # trains and returns the model type. can add models later easily
    print(f"Training {model_type} model...")
    
    if model_type == "linear_regression":
        model = LinearRegression()
    else:
        raise ValueError(f"Model type {model_type} is not added yet.")
        
    model.fit(X_train, y_train)
    return model


def evaluate_model(model, X_test, y_test):
    # predicts, clips neg vals, and then returns metrics
    print("Evaluating model on test set...")
    
    y_pred = model.predict(X_test)
    
    # clip predictions to 0 since we can not have negative demand
    y_pred = np.clip(y_pred, a_min=0, a_max=None)
    
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    wmape_val = wmape(y_test, y_pred)
    
    return {"mae": mae, "rmse": rmse, "wmape": wmape_val}


def save_model(model, model_type, experiment_id):
    # saves the completely trained model file with a standardized name
    # so we know what version and model it is
    os.makedirs("models", exist_ok=True)
    file_path = f"models/{model_type}_{experiment_id}.pkl"
    
    joblib.dump(model, file_path)
    print(f"Model saved successfully to {file_path}")
    
    return file_path
