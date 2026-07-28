CREATE TABLE IF NOT EXISTS warehouse.dim_time (

    time_id SERIAL PRIMARY KEY,
    year INT UNIQUE NOT NULL,
    decade INT

);



CREATE TABLE IF NOT EXISTS warehouse.dim_geography (

    geo_id SERIAL PRIMARY KEY,
    geo_name VARCHAR(100) UNIQUE NOT NULL,
    geo_level VARCHAR(50),
    parent_geo_id INT

);



CREATE TABLE IF NOT EXISTS warehouse.dim_residence (

    residence_id SERIAL PRIMARY KEY,
    residence_type VARCHAR(50) UNIQUE NOT NULL

);



CREATE TABLE IF NOT EXISTS warehouse.dim_sex (

    sex_id SERIAL PRIMARY KEY,
    sex_label VARCHAR(50) UNIQUE NOT NULL

);



CREATE TABLE IF NOT EXISTS warehouse.dim_product (

    product_id SERIAL PRIMARY KEY,
    product_category VARCHAR(200) UNIQUE NOT NULL

);