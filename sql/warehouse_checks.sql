-- =====================================
-- Row counts
-- =====================================

SELECT 'dim_time' AS table_name, COUNT(*) FROM warehouse.dim_time
UNION ALL
SELECT 'dim_geography', COUNT(*) FROM warehouse.dim_geography
UNION ALL
SELECT 'dim_residence', COUNT(*) FROM warehouse.dim_residence
UNION ALL
SELECT 'dim_sex', COUNT(*) FROM warehouse.dim_sex
UNION ALL
SELECT 'dim_product', COUNT(*) FROM warehouse.dim_product
UNION ALL
SELECT 'fact_population', COUNT(*) FROM warehouse.fact_population
UNION ALL
SELECT 'fact_unemployment', COUNT(*) FROM warehouse.fact_unemployment
UNION ALL
SELECT 'fact_cpi', COUNT(*) FROM warehouse.fact_cpi;



-- =====================================
-- Check orphan keys
-- =====================================

SELECT *
FROM warehouse.fact_population f
LEFT JOIN warehouse.dim_time t
ON f.time_id=t.time_id
WHERE t.time_id IS NULL;



SELECT *
FROM warehouse.fact_population f
LEFT JOIN warehouse.dim_geography g
ON f.geo_id=g.geo_id
WHERE g.geo_id IS NULL;



-- =====================================
-- Check duplicates
-- =====================================

SELECT 
time_id,
geo_id,
residence_id,
COUNT(*)

FROM warehouse.fact_population

GROUP BY 
time_id,
geo_id,
residence_id

HAVING COUNT(*) > 1;