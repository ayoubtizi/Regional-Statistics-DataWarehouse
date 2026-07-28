-- =====================================================
-- Q4 — Rural and urban population evolution
--
-- How has urbanization evolved over time?
-- =====================================================


SELECT

    t.year,
    r.residence_type,
    SUM(f.population_count) AS population_value


FROM warehouse.fact_population f


JOIN warehouse.dim_time t
ON f.time_id=t.time_id


JOIN warehouse.dim_residence r
ON f.residence_id=r.residence_id


GROUP BY

    t.year,
    r.residence_type


ORDER BY

    t.year;
