import os
import joblib
from sklearn.linear_model import LinearRegression

def train_model(X_train, y_train, model_type="linear_regression"):
    # trains and returns the picked model
    print(f"Training {model_type} model...")
    
    if model_type == "linear_regression":
        model = LinearRegression()
    else:
        raise ValueError(f"Model type {model_type} is not added yet.")
        
    model.fit(X_train, y_train)
    return model

def save_model(model, model_type, experiment_id):
    # saves the trained model with a clear name
    os.makedirs("models", exist_ok=True)
    file_path = f"models/{model_type}_{experiment_id}.pkl"
    
    joblib.dump(model, file_path)
    print(f"Model saved succesfully to {file_path}")
    
    return file_path
