-- =====================================================
-- Q8 — CPI evolution over time
--
-- How have prices evolved?
-- =====================================================


SELECT

    t.year,
    g.geo_name,
    AVG(f.cpi_value) AS cpi_value


FROM warehouse.fact_cpi f


JOIN warehouse.dim_time t
ON f.time_id=t.time_id


JOIN warehouse.dim_geography g
ON f.geo_id=g.geo_id


GROUP BY

    t.year,
    g.geo_name


ORDER BY

    t.year;
