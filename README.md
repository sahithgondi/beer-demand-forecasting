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

### Project Goal
 Build a system that will look at past invoices and:
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




 






