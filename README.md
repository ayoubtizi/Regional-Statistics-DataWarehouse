# StatFlow Analytics Warehouse

## Statistical Data Integration Pipeline and Analytical Data Warehouse

---

## 1. Project Overview

**StatFlow Analytics Warehouse** is a Data Engineering project that implements a complete ETL pipeline for integrating, transforming, storing, validating, and analyzing statistical datasets.

The objective of this project is to design and implement a structured data platform capable of transforming raw statistical files into a reliable analytical warehouse.

The project covers the complete data lifecycle:

- Data ingestion
- Data validation
- Data cleaning
- Data transformation
- Dimensional data modeling
- Data warehouse loading
- Data quality validation
- Analytical SQL processing
- ETL execution reporting

The pipeline is orchestrated through a single execution command, allowing all ETL stages to run sequentially.

---

# 2. Project Context

Statistical organizations usually receive data from multiple sources in different formats.

These datasets may contain:

- Inconsistent column names
- Missing values
- Different structures
- Wide-format tables
- Manual processing requirements

This project addresses these challenges by creating a centralized analytical platform.

The final objective is to transform raw statistical files into structured information ready for analysis and reporting.

---

# 3. Project Objectives

The main objectives are:

## Data Integration

Centralize multiple statistical datasets into one warehouse.

Datasets integrated:

- Population statistics
- Unemployment statistics
- Consumer Price Index (CPI)


## Data Quality Management

Ensure that only valid datasets enter the processing workflow.

Implemented checks:

- File validation
- Schema validation
- Missing value handling
- Duplicate prevention
- Warehouse integrity checks


## Data Warehouse Implementation

Design a dimensional model optimized for analytical queries.

The warehouse follows a Star Schema architecture.

---

# 4. Pipeline Architecture

Current pipeline execution:

```
                 Incoming Files

                      |
                      v

          Data Ingestion & Validation

                      |
          -------------------------
          |                       |

          v                       v

      data/raw              data/rejected


          |
          v

     Transformation Layer


          |
          v

    data/processed


          |
          v

 PostgreSQL Data Warehouse


          |
     -----------------
     |               |

     v               v

Quality Checks    Analytics Layer


                      |
                      v

               Generated Reports

```

---

# 5. Pipeline Execution

The complete pipeline is executed manually using:

```bash
python -m src.pipeline
```

The pipeline orchestrates the following steps:

1. Data ingestion
2. File validation
3. Data transformation
4. Dimension loading
5. Fact table loading
6. Warehouse quality checks
7. Analytical SQL execution
8. ETL log report generation


The pipeline does not currently include scheduling or event-based triggering.

Future improvements may include Airflow, cron jobs, or file monitoring systems.

---

# 6. Project Structure

```
Regional-Statistics-DataWarehouse

│
├── data
│   │
│   ├── incoming
│   │   Incoming datasets
│   │
│   ├── raw
│   │   Validated raw files
│   │
│   ├── processed
│   │   Cleaned transformed datasets
│   │
│   └── rejected
│       Invalid datasets
│
│
├── docs
│   Documentation files
│
│
├── reports
│   Generated reports and logs
│
│
├── sql
│   │
│   ├── Data_Warehouse
│   │
│   ├── analytics
│   │
│   └── validation
│
│
├── src
│   │
│   ├── ingestion.py
│   ├── transformation.py
│   ├── pipeline.py
│   │
│   ├── load
│   │   ├── database.py
│   │   ├── load_dimensions.py
│   │   └── load_facts.py
│   │
│   ├── quality
│   │   └── warehouse_checks.py
│   │
│   ├── analytics
│   │   └── run_analytics.py
│   │
│   └── reports
│       └── export_etl_logs.py
│
└── README.md
```

---

# 7. Technologies Used

## Programming Language

Python

Used for:

- ETL processing
- Data cleaning
- File management
- Report generation


Main libraries:

- pandas
- psycopg2
- openpyxl


---

## Database

PostgreSQL

Used for:

- Data warehouse storage
- Dimensional modeling
- Analytical queries


---

## Development Tools

- VS Code
- DBeaver
- Git/GitHub

---

# 8. Data Ingestion Layer

The ingestion layer manages incoming datasets.

Location:

```
data/incoming
```

Workflow:

```
New File

    |
    v

Validation Rules

    |
    |
    +----------+
    |          |
    v          v

 Valid      Invalid

    |          |
    v          v

 data/raw   data/rejected

```

Validation verifies that datasets respect predefined rules before entering the warehouse workflow.

Each ingestion execution generates logs:

```
reports/ingestion_log.csv
```

Containing:

- Timestamp
- Filename
- Status
- Validation message
- Destination location


---

# 9. Transformation Layer

The transformation layer converts raw datasets into warehouse-compatible datasets.

Implemented operations:

## Cleaning

- Remove empty rows
- Remove empty columns
- Handle missing values
- Clean text fields


## Standardization

Example:

```
Zone géographique

        |

        v

geo_name

```

```
Milieu de résidence

        |

        v

residence_type

```


## Data Reshaping

Original format:

```
        2020  2021  2022

Region   X     X     X

```

Converted:

```
Region | Year | Value

```

---

Generated datasets:

```
data/processed/

population_processed.xlsx

unemployment_processed.xlsx

cpi_processed.xlsx

```

---

# 10. Data Warehouse Design

The warehouse uses a Star Schema.

## Dimension Tables

### dim_time

Stores years and decades.

---

### dim_geography

Stores geographic information.

---

### dim_residence

Stores residence categories:

- Urban
- Rural

---

### dim_sex

Stores gender information.

---

### dim_product

Stores CPI categories.

---

# Fact Tables

## fact_population

Stores population measurements.

Attributes:

- Time
- Geography
- Residence
- Population count


---

## fact_unemployment

Stores unemployment indicators.

Attributes:

- Time
- Geography
- Residence
- Sex
- Unemployment rate


---

## fact_cpi

Stores consumer price indicators.

Attributes:

- Time
- Geography
- Product category
- CPI value


---

# 11. Loading Process

The loading phase inserts transformed datasets into PostgreSQL.

Implemented features:

- Dimension loading
- Fact loading
- Foreign key resolution
- Duplicate handling


Duplicate prevention uses:

```sql
ON CONFLICT DO NOTHING
```

for dimensions.

Facts use:

```sql
ON CONFLICT DO UPDATE
```

to update existing records when necessary.

---

# 12. Data Quality Layer

Before analytical processing, warehouse validation checks are executed.

Implemented checks:

- Duplicate detection
- Missing key detection
- Referential integrity verification
- Data consistency checks


Location:

```
src/quality/
```

---

# 13. Analytics Layer

The analytical layer contains SQL queries answering statistical questions.

Examples:

## Population Analysis

- Population evolution over time
- Population ranking by geography
- Urban versus rural evolution


## Unemployment Analysis

- Unemployment evolution
- Population groups most affected
- Gender comparison


## CPI Analysis

- Price evolution
- Categories with highest increases


SQL location:

```
sql/analytics/
```

Results:

```
reports/analytics/
```

---

# 14. ETL Execution Reports

The project generates execution reports describing pipeline activity.

Reports include:

- Execution status
- Number of processed rows
- Errors
- Execution timestamps


Generated file:

```
reports/etl_logs_report.xlsx
```

---

# 15. Current Limitations

The current version requires manual execution.

Example:

```bash
python -m src.pipeline
```

Future improvements:

- Automatic file detection
- Scheduled execution
- Apache Airflow orchestration
- Cloud deployment
- Dashboard integration
- Incremental loading strategy


---

# 16. Installation

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure database connection:

```
src/load/database.py
```

Run the pipeline:

```bash
python -m src.pipeline
```

---

# 17. Conclusion

StatFlow Analytics Warehouse demonstrates the implementation of a complete Data Engineering workflow.

The project includes:

✔ Data ingestion  
✔ Data validation  
✔ Data transformation  
✔ Data warehouse modeling  
✔ Dimension and fact loading  
✔ Data quality checks  
✔ Analytical SQL processing  
✔ Execution reporting  


It provides a foundation for a scalable statistical data platform.