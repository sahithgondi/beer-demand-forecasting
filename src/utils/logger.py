import os
import csv
import uuid
from datetime import datetime

def log_experiment(model_type, features, mae, rmse, wmape, notes=""):
    # logs experiment results to a central csv tracker
    # define tracking file
    report_file = "reports/experiments.csv"

    # make sure reports directory exists if not creaet it 
    os.makedirs(os.path.dirname(report_file), exist_ok=True)
    
    
    # generate unique ids and timestamps
    experiment_id = str(uuid.uuid4())[:8]  # e.g., 'a3b9c24d'
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # format features as a simple string
    features_str = "|".join(features)
    
    # check if file exists if file is new then we add headers
    file_exists = os.path.isfile(report_file)
    
    # append the new run
    with open(report_file, mode='a', newline='') as f:
        writer = csv.writer(f)
        
        # write header if new
        if not file_exists:
            writer.writerow([
                "experiment_id", "timestamp", "model_type", 
                "features_used", "mae", "rmse", "wmape", "notes"
            ])
            
        # write the experiment data
        writer.writerow([
            experiment_id, timestamp, model_type, 
            features_str, round(mae, 4), round(rmse, 4), round(wmape, 4), notes
        ])
        
    print(f"Experiment {experiment_id} logged to {report_file}")
    
    return experiment_id
