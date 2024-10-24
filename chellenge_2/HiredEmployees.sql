create or replace view postgres.public.top_hires_by_department as (
WITH 
department_hires AS (
    SELECT
        d.id,
        d.department,
        COUNT(*) AS hired
    FROM 
        postgres.public.hired_employees AS he
    LEFT JOIN 
        postgres.public.departments AS d ON NULLIF(he.department_id, '')::INTEGER = d.id
    WHERE 
        EXTRACT(YEAR FROM TO_TIMESTAMP(he.datetime, 'YYYY-MM-DD"T"HH24:MI:SS"Z"')) = 2021
    GROUP BY 
        d.id, d.department
),

mean_hires AS (
    SELECT
        AVG(hired) AS mean_hired
    FROM 
        department_hires
)

SELECT 
    dh.id,
    dh.department,
    dh.hired
FROM 
    department_hires AS dh,
    mean_hires AS mh
WHERE 
    dh.hired > mh.mean_hired
ORDER BY 
    dh.hired desc
);