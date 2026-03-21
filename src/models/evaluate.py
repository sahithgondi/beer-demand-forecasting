import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error

def wmape(y_true, y_pred):
    # calculates wmape
    if np.sum(y_true) == 0:
        return 0.0
    return np.sum(np.abs(y_true - y_pred)) / np.sum(y_true)

def evaluate_model(model, X_test, y_test):
    # predicts, then clips neg vals, adn then return metrics
    print("Evaluating model on test set...")
    
    y_pred = model.predict(X_test)
    
    # clip predictions to 0 cant have neg demand
    y_pred = np.clip(y_pred, a_min=0, a_max=None)
    
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    wmape_val = wmape(y_test, y_pred)
    
    return {"mae": mae, "rmse": rmse, "wmape": wmape_val}
