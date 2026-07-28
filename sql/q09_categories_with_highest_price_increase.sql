-- =====================================================
-- Q9 — Categories with highest price increase
--
-- Which categories changed the most?
-- =====================================================


SELECT

    p.product_category,
    t.year,
    AVG(f.cpi_value) AS cpi_value


FROM warehouse.fact_cpi f


JOIN warehouse.dim_product p
ON f.product_id=p.product_id


JOIN warehouse.dim_time t
ON f.time_id=t.time_id


GROUP BY

    p.product_category,
    t.year


ORDER BY

    p.product_category,
    t.year;
