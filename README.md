# Beer Ordering Optimization System
## Family Convenience Store
A data pipeline and forecasting system designed to optimize weekly beer ordering for my family's gas station.

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

  ### Evaluation Metrics
  - **MAE (mean absolute error)**: measures the average magnitude of forecasting errors in cases of beer.
  - **RMSE (root mean squared error)**: penalizes large, unexpected spikes or dips in the order predictions.
  - **WMAPE (weighted mean absolute percentage error)**: this was chosen because of how zero inflated the data is.

  ### Demand Estimation Strategy
  Because sales and inventory data is not available, we must infer data from the ordering invoices. We have to treat orders as a proxy for demand. Accounting for inconsistent ordering patterns, returns, and stockouts is the key to accurate demand estimation. 

  ### System Architecture
  Raw Invoices &rarr; Data Ingestion &rarr; Cleaning Data &rarr; Feature Engineering &rarr; Model Training &rarr; Demand Prediction &rarr; Order Recommendations &rarr; Dashboard

  ### Future Improvements
  - cluster SKUs by volume ordered and train models for each cluster. This will improve accuracy and lessen the impact of the zero filled data. 
  - explore tree based models or specialized count models that will handle sparse, non linear demand better than stanrd linear regression can.
  - incorporate external features like holidays, weather history + forecast, and gas prices.



 






