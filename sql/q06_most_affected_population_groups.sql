-- =====================================================
-- Q6 — Most affected population groups
--
-- Which groups have higher unemployment?
-- =====================================================


SELECT

    t.year,
    g.geo_name,
    r.residence_type,
    s.sex_label,
    AVG(f.unemployment_rate) AS unemployment_rate


FROM warehouse.fact_unemployment f


JOIN warehouse.dim_time t
ON f.time_id=t.time_id


JOIN warehouse.dim_geography g
ON f.geo_id=g.geo_id


JOIN warehouse.dim_residence r
ON f.residence_id=r.residence_id


JOIN warehouse.dim_sex s
ON f.sex_id=s.sex_id


GROUP BY

    t.year,
    g.geo_name,
    r.residence_type,
    s.sex_label


ORDER BY

    unemployment_rate DESC;
