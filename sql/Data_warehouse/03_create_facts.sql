CREATE TABLE IF NOT EXISTS warehouse.fact_population (

    population_id SERIAL PRIMARY KEY,

    time_id INT REFERENCES warehouse.dim_time(time_id),

    geo_id INT REFERENCES warehouse.dim_geography(geo_id),

    residence_id INT REFERENCES warehouse.dim_residence(residence_id),

    population_count INT

);



CREATE TABLE IF NOT EXISTS warehouse.fact_unemployment (

    unemployment_id SERIAL PRIMARY KEY,

    time_id INT REFERENCES warehouse.dim_time(time_id),

    geo_id INT REFERENCES warehouse.dim_geography(geo_id),

    residence_id INT REFERENCES warehouse.dim_residence(residence_id),

    sex_id INT REFERENCES warehouse.dim_sex(sex_id),

    unemployment_rate DECIMAL

);



CREATE TABLE IF NOT EXISTS warehouse.fact_cpi (

    cpi_id SERIAL PRIMARY KEY,

    time_id INT REFERENCES warehouse.dim_time(time_id),

    geo_id INT REFERENCES warehouse.dim_geography(geo_id),

    product_id INT REFERENCES warehouse.dim_product(product_id),

    cpi_value DECIMAL

);