-- =====================================================
-- Q7 — Rural versus urban unemployment comparison
-- =====================================================


SELECT

    t.year,
    r.residence_type,
    AVG(f.unemployment_rate) AS unemployment_rate


FROM warehouse.fact_unemployment f


JOIN warehouse.dim_time t
ON f.time_id=t.time_id


JOIN warehouse.dim_residence r
ON f.residence_id=r.residence_id


GROUP BY

    t.year,
    r.residence_type


ORDER BY

    t.year;
