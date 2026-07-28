-- =====================================================
-- Q2 — Population distribution by residence type
--
-- How is population distributed between rural and urban?
-- =====================================================


SELECT

    t.year,
    g.geo_name,
    r.residence_type,
    SUM(f.population_count) AS population_value


FROM warehouse.fact_population f


JOIN warehouse.dim_time t
ON f.time_id=t.time_id


JOIN warehouse.dim_geography g
ON f.geo_id=g.geo_id


JOIN warehouse.dim_residence r
ON f.residence_id=r.residence_id


GROUP BY

    t.year,
    g.geo_name,
    r.residence_type


ORDER BY

    t.year,
    g.geo_name;
