import joblib
import numpy as np

def load_model(file_path):
    # loads saved model from disk
    print(f"Loading model from {file_path}")
    return joblib.load(file_path)

def predict(model, X_input):
    # makes predictions on new inference data
    preds = model.predict(X_input)
    
    # demand cannot be neg
    preds = np.clip(preds, a_min=0, a_max=None)
    
    return preds
