# Reports Generation Implementation


## 1. Objective

The reporting layer converts analytical SQL results into Excel reports automatically.


The objective is to provide users with ready-to-use statistical outputs.



## 2. Analytical Layer


SQL queries were created to answer the defined business questions:

- Population analysis
- Unemployment analysis
- CPI analysis



The SQL queries use the warehouse fact and dimension tables.



## 3. Report Generation Process


The generation workflow:


SQL Query Files

↓

Python Analytics Module

↓

Pandas DataFrames

↓

Excel Files



## 4. Implementation


The analytics module:

- Executes SQL scripts
- Retrieves query results
- Converts results into DataFrames
- Exports Excel files



## 5. Output Structure


Generated reports are stored in:

reports/
└── analytics/
├── q1_population_evolution.xlsx
├── q2_population_distribution.xlsx
└── ...

## 6. Technical Reports


In addition to analytical reports, the system generates ETL monitoring reports.


Example:


reports/etl_logs_report.xlsx



This report contains:

- Pipeline executions
- Status
- Processed rows
- Errors



## 7. Current Status

Implemented:

✔ Warehouse implementation  
✔ Automated loading  
✔ Pipeline orchestration  
✔ ETL monitoring  
✔ Analytical SQL layer  
✔ Excel report generation