# Beer Ordering Optimization System
## Family Convenience Store
A forecasting system designed to optimize weekly beer ordering for my family's gas station.

Beer ordering is currently based on:
 - intuition
 - last week's orders
 - current stock
 - supplier recommendations

This has been leading to:
 - over ordering &rarr; wasted storage space and unsold beer
 - under ordering &rarr; decrease in beer sales
 - returns to supplier &rarr; wasting time and resources

### Goal is to build a system that will give recommendations on how much beer to order each week.
We will look at past invoices to:
 - learn ordering patterns
 - predict the optimal weekly order quantities
 - provide recommendations with explanations via a dashboard

### Store Details
 - 1 location family gas station
 - Beer is a key product category
 - Orders are places once a week
   
### Current Ordering Process

Each weeks order is determined by:
 - last week's order
 - estimate of demand
 - current stock levels (manually tracked)
 - supplier input

This process is inconsistent and requires constant knowledge of the store.
Some of the problems caused by this current process are:
 - Over ordering
     - limited storage space
     - inventory can sit for a long time
     - returns to supplier
  - Under ordering
    - popular items run out
    - lost sales

Goal is to predict optimal weekly beer order quantities to reduce waste and improve inventory efficiency. 

### Constraints
 - Orders placed every 7 days
 - no access to sales data
 - no access to inventory data
 - only data available is supplier invoices (orders + returns)

Because of these constraints the system must:
 - infer the demand per SKU from the ordering behavior
 - handle the noise of returns and inconsistent ordering
 - operate under the data limitations

### Data Pipeline and Ingestion
Data comes from weekly CSV invoice files.
Each file represents supplier transactions for the given week.
This includes:
  - SKU
  - itemName
  - unitUpc
  - caseUpc
  - quantity
  - unitPrice
  - total

### Data Challenges
 - Pandas `read_csv` is default delimited by `,` and the data was delimited by `;`
 - Encoding issues due to BOM in headers
 - Dates embedded in filenames
 - Inconsistent column presence
 - Returns represented as negative values

### Pipeline Design
Raw Invoices &rarr; Validation &rarr; Cleaning &rarr; Standardization &rarr; Combined Dataset
1. Steps: Load each file
2. Normalize schema and column names
3. Extract date from filename
4. Convert numeric fields
5. Combine into a single dataset

### Data Processing
After ingestion, the data is transformed into a time based format.

Steps:
  - aggregate invoices into weekly demand by SKU
  - fill missing SKU week combinations with 0 (for no order placed)
  - negative quantities are treated as returns and subtracted from the week's order
  - cleaned demand is output 

  ### Data Version Control (DVC)
  The raw and engineered datasets are not included in Git to keep the data secure. The data layer is versioned entirely with DVC.
  - `data/**/*.dvc`: These small files track exact versions, md5 hashes, and sizes of datasets like `all_sales.csv`. 
  - Reproducibility: If a newly engineered feature breaks the regression model, you can instantly rollback the DVC pointers to safely restore the exact dataset state that generated the previous best wmape baseline.

### Engineered Features:
  - lag features
    - `lag_1`,`lag_2`,`lag_4` are previous week's demand
  - rolling stats
    - rolling mean (window = 4)
    - rolling standard deviation
  - time features
    - week 
    - month
    - quarter
  - planned features
    - holidays
    - weather forecast
    - gas prices
  
  ### Modeling Approach
  - global standard linear regression: predicts weekly demand across all 98 SKU's to build an inital pipeline before comparing to more complex models.
  - baseline comparison: predicts exactly the previous week's sales `lag_1` to test how well the linear regression model learns ordering patterns.

  ### Demand Estimation Strategy
  Because sales and inventory data is not available, we must infer data from the ordering invoices. We have to treat orders as a direct indicator for demand. Accounting for inconsistent ordering patterns and returns is the way to accurately estimating demand. 

  ### System Architecture
  Raw Invoices &rarr; Data Ingestion &rarr; Cleaning Data &rarr; Feature Engineering &rarr; Model Training &rarr; Demand Prediction &rarr; Order Recommendations &rarr; Dashboard

  ### Experiment Tracking & Model Versioning
  To make sure we can reproduce experiments and continuously improve the pipeline, every run of [run_pipeline.py] is automatically tracked:
  - Experiments Logger [reports/experiments.csv]: Logs a unique `experiment_id`, the timestamp, the exact features used, and the holdout mae/rmse/wmape scores for every single run.
  - Model Artifacts (`models/`): Every trained model is exported as a `.pkl` file tagged identically with the `experiment_id` from the logger. If a new experimental feature improves the wmape, the exact regression weights are saved and ready for deployment without ever losing track of past baselines.

   ### Evaluation Metrics & Current Performance
  After executing the modular pipeline, predicting weekly demand against our holdout test set generated the following results via the Global Linear Regression model:
  - WMAPE: `45.89%` (Weighted Mean Absolute Percentage Error) — Chosen due to the zero inflated demand as we cleaned.
  - MAE: `1.0867` (Mean Absolute Error) — Off by an average of ~1 case per week per SKU.
  - RMSE: `2.0075` (Root Mean Squared Error) — Penalizes predicting a spike when actual demand was 0.

  ### Future Improvements
  - cluster SKUs by volume ordered and train models for each cluster. This will improve accuracy and lessen the impact of the zero filled data. 
  - explore tree based models or specialized count models that will handle sparse, non linear demand better than stanrd linear regression can.
  - incorporate external features like holidays, weather history + forecast, and gas prices.

  ### Project Structure
  ```
     ├── README.md
     ├── app
     |  └── app.py
     ├── data
     |  ├── features
     |  ├── processed
     |  └── raw
     ├── models
     ├── notebooks
     |  ├── 01_eda.ipynb
     |  ├── 02_feature_engineering.ipynb
     |  └── 03_modeling.ipynb
     ├── reports
     |  ├── figures
     |  └── results
     ├── requirements.txt
     ├── src
     |  ├── data
     |  ├── features
     |  ├── models
     |  ├── pipeline
     |  └── utils
     └── structure.txt
  ```

### Usage and Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/sahithgondi/beer-demand-forecasting.git
   cd beer-demand-forecasting
   ```

2. Set up the environment:
  Create and activate your venv

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the End-to-End Pipeline:
   ```bash
   python src/pipeline/run_pipeline.py
   ```

