# Data Warehouse Design

## 1. Overview

The objective of this data warehouse is to centralize regional statistical indicators from different source datasets and provide a structured analytical environment for reporting and decision-making.

The warehouse integrates three main statistical domains:

- Population statistics
- Unemployment statistics
- Consumer Price Index (CPI)

The source files are originally designed for reporting purposes and contain metadata, presentation elements, and wide-format structures.

The warehouse transforms these sources into a standardized analytical model based on dimensional modeling principles.

---

# 2. Design Approach

## 2.1 Modeling Method

A dimensional modeling approach is adopted using a **fact constellation schema**.

This choice is justified because:

- Multiple statistical indicators must be analyzed.
- Different indicators share common analytical dimensions.
- Users need fast analytical queries and reporting capabilities.

The model contains:

- Fact tables: store numerical measurements.
- Dimension tables: store descriptive attributes used for filtering and analysis.

---

# 3. Analytical Requirements

The warehouse is designed to answer the following business questions.

---

# 3.1 Population Analysis

## Q1 — Population evolution over time

**Question:**

How has the population evolved over different years?

Required information:

- Year
- Geographic area
- Population value


---

## Q2 — Population distribution by residence type

**Question:**

How is the population distributed between rural and urban areas?

Required information:

- Year
- Geographic area
- Residence type
- Population value


---

## Q3 — Geographic population ranking

**Question:**

Which geographic areas have the highest population?

Required information:

- Geographic area
- Year
- Population value


---

## Q4 — Rural and urban population evolution

**Question:**

How has urbanization evolved over time?

Required information:

- Year
- Residence type
- Population value


---

# 3.2 Unemployment Analysis

## Q5 — Unemployment rate evolution

**Question:**

How has unemployment changed over time?

Required information:

- Year
- Geographic area
- Unemployment rate


---

## Q6 — Most affected population groups

**Question:**

Which population groups experience higher unemployment?

Required information:

- Year
- Geographic area
- Residence type
- Sex/category
- Unemployment rate


---

## Q7 — Rural versus urban unemployment comparison

**Question:**

Is unemployment different between rural and urban areas?

Required information:

- Residence type
- Year
- Unemployment rate


---

# 3.3 Consumer Price Index Analysis

## Q8 — CPI evolution over time

**Question:**

How have prices evolved over different years?

Required information:

- Year
- Geographic area
- CPI value


---

## Q9 — Product categories with highest price increase

**Question:**

Which categories experienced the largest price variations?

Required information:

- Product category
- Year
- CPI value


---

## Q10 — Comparison between product categories

**Question:**

How does each product category evolve compared to the general CPI?

Required information:

- Product category
- Year
- CPI value


---

# 4. Data Warehouse Architecture

The global architecture follows:

```
Raw Sources
    |
    |
    v
Ingestion Layer
    |
    |
    v
Raw Storage Zone
    |
    |
    v
Transformation Layer
    |
    |
    v
Staging Tables
    |
    |
    v
Analytical Data Warehouse
    |
    |
    v
Reporting / Dashboard
```

---

# 5. Dimensional Model Design

## 5.1 Shared Dimensions

Some dimensions are shared by multiple fact tables.

These are called **conformed dimensions**.

---

# Dimension: dim_time

## Purpose

Allows analysis over time.

## Attributes

| Column | Description |
|-|-|
| time_id | Primary key |
| year | Statistical year |
| decade | Year grouping |

Example:

|time_id|year|
|-|-|
|1|2024|
|2|2025|
|3|2026|

---

# Dimension: dim_geography

## Purpose

Allows analysis by geographic area.

## Attributes

| Column | Description |
|-|-|
| geo_id | Primary key |
| geo_name | Geographic name |
| geo_level | Administrative level |
| parent_geo_id | Geographic hierarchy |

Example:

|geo_id|geo_name|
|-|-|
|1|National|
|2|Agadir|
|3|Rabat|

---

# Dimension: dim_residence

## Purpose

Used for rural/urban comparisons.

## Attributes

| Column | Description |
|-|-|
| residence_id | Primary key |
| residence_type | Rural/Urbain/Total |

---

# Dimension: dim_sex

## Purpose

Used for unemployment group analysis.

## Attributes

| Column | Description |
|-|-|
| sex_id | Primary key |
| sex_label | Male/Female/Total |

---

# Dimension: dim_product

## Purpose

Used for CPI analysis.

## Attributes

| Column | Description |
|-|-|
| product_id | Primary key |
| product_category | Product classification |

---

# 6. Fact Tables Design

---

# Fact Table: fact_population

## Business Meaning

Stores population measurements.

## Grain

One row represents:

> The population of a geographic area, for a residence type, during a specific year.

## Structure

| Column | Description |
|-|-|
| population_id | Primary key |
| time_id | Foreign key |
| geo_id | Foreign key |
| residence_id | Foreign key |
| population_count | Population measurement |

---

# Fact Table: fact_unemployment

## Business Meaning

Stores unemployment indicators.

## Grain

One row represents:

> An unemployment measurement for a geographic area and population category during a specific year.

## Structure

| Column | Description |
|-|-|
| unemployment_id | Primary key |
| time_id | Foreign key |
| geo_id | Foreign key |
| residence_id | Foreign key |
| sex_id | Foreign key |
| unemployment_rate | Percentage value |

---

# Fact Table: fact_cpi

## Business Meaning

Stores Consumer Price Index measurements.

## Grain

One row represents:

> A CPI measurement for a product category, geographic area, and year.

## Structure

| Column | Description |
|-|-|
| cpi_id | Primary key |
| time_id | Foreign key |
| geo_id | Foreign key |
| product_id | Foreign key |
| cpi_value | CPI measurement |