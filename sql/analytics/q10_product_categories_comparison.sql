-- =====================================================
-- Q10 — Product categories comparison
--
-- Compare categories with general CPI
-- =====================================================


SELECT

    t.year,

    p.product_category,

    AVG(f.cpi_value) AS cpi_value


FROM warehouse.fact_cpi f


JOIN warehouse.dim_product p
ON f.product_id=p.product_id


JOIN warehouse.dim_time t
ON f.time_id=t.time_id


WHERE

    p.product_category IN
    (
        'GENERAL'
    )

OR

    p.product_category <> 'GENERAL'


GROUP BY

    t.year,
    p.product_category


ORDER BY

    t.year,
    cpi_value DESC;
