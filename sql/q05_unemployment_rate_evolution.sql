-- =====================================================
-- Q5 — Unemployment rate evolution
--
-- How has unemployment changed over time?
-- =====================================================


SELECT

    t.year,
    g.geo_name,
    AVG(f.unemployment_rate) AS unemployment_rate


FROM warehouse.fact_unemployment f


JOIN warehouse.dim_time t
ON f.time_id=t.time_id


JOIN warehouse.dim_geography g
ON f.geo_id=g.geo_id


GROUP BY

    t.year,
    g.geo_name


ORDER BY

    g.geo_name,
    t.year;
