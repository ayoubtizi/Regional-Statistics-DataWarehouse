-- =====================================================
-- Q1 — Population evolution over time
--
-- How has population evolved over different years?
--
-- Required:
-- Year
-- Geographic area
-- Population value
-- =====================================================


SELECT

    t.year,
    g.geo_name,
    SUM(f.population_count) AS population_value


FROM warehouse.fact_population f


JOIN warehouse.dim_time t
ON f.time_id = t.time_id


JOIN warehouse.dim_geography g
ON f.geo_id = g.geo_id


GROUP BY

    t.year,
    g.geo_name


ORDER BY

    g.geo_name,
    t.year;
