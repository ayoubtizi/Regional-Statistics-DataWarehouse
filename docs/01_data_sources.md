# Data Sources Documentation


## 1. Overview

The project uses statistical datasets provided in Excel format.

These datasets contain demographic, social, economic, and employment
indicators.

The objective is to integrate these heterogeneous sources into a unified
Data Warehouse.


---

# 2. Raw Data Sources


## Source 1: RGPH Demographic and Social Indicators


File:

rgph_demographic_social_indicators_2024.xlsx


Description:

Dataset containing demographic and socio-economic indicators collected
through population statistics.


Main domains:

- Population
- Demography
- Social characteristics


Potential usage:

- Population fact table
- Demographic indicators


---

## Source 2: Employment Survey Indicators


File:

ene_employment_indicators_2019_2024.xlsx


Description:

Dataset containing employment-related statistics over multiple years.


Main domains:

- Employment
- Unemployment
- Economic activity


Potential usage:

- Employment indicators fact table
- Historical analysis


---

## Source 3: Regional Indicators


File:

regional_indicators_2024.xlsx


Description:

Dataset containing aggregated statistical indicators by geographic areas.


Main domains:

- Regional statistics
- Socio-economic indicators


Potential usage:

- Geographic dimensions
- Statistical facts


---

## Source 4: Province Indicators


File:

province_key_indicators_2023.xlsx


Description:

Dataset containing detailed indicators at province level.


Main domains:

- Geography
- Local indicators


Potential usage:

- Geography dimension
- Detailed analysis


---

## Source 5: Employment Creation Indicators


File:

employment_creation_2023_2025.xlsx


Description:

Dataset containing information about employment creation.


Main domains:

- Employment evolution
- Economic development


Potential usage:

- Employment analysis


---

# 3. Source Integration Strategy


Each source will follow the same processing workflow:


Raw Excel File

        ↓

Data Extraction

        ↓

Data Cleaning and Validation

        ↓

Transformation

        ↓

Data Warehouse Loading


---

# 4. Data Source Management


Raw files are stored separately from processed data:


data/

├── raw/

│   ├── Excel source files

│

├── staging/

│   ├── cleaned intermediate data

│

└── warehouse/

    └── analytical database