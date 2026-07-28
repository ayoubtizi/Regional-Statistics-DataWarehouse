-- =====================================================
-- Q3 — Geographic population ranking
--
-- Which geographic areas have the highest population?
-- =====================================================


SELECT

    g.geo_name,
    t.year,
    SUM(f.population_count) AS population_value


FROM warehouse.fact_population f


JOIN warehouse.dim_geography g
ON f.geo_id=g.geo_id


JOIN warehouse.dim_time t
ON f.time_id=t.time_id


GROUP BY

    g.geo_name,
    t.year


ORDER BY

    population_value DESC;
