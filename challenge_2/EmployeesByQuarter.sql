create or replace view postgres.public.employee_by_quarter as (
with

EMPLOYEE_DESCRIPTION as (
SELECT 
    d.department, j.job, EXTRACT(QUARTER FROM TO_TIMESTAMP(he.datetime, 'YYYY-MM-DD"T"HH24:MI:SS"Z"')) AS quarter, count(*) as num_employees 
FROM 
    postgres.public.hired_employees AS he
LEFT JOIN 
    postgres.public.departments AS d ON NULLIF(he.department_id, '')::INTEGER = d.id
LEFT JOIN 
    postgres.public.jobs AS j ON NULLIF(he.job_id, '')::INTEGER = j.id
where EXTRACT(YEAR FROM TO_TIMESTAMP(he.datetime, 'YYYY-MM-DD"T"HH24:MI:SS"Z"')) = 2021
group by 1,2,3
)

select
	department
	,job
	,sum(case when quarter = 1 then num_employees else 0 end) as Q1
	,sum(case when quarter = 2 then num_employees else 0 end) as Q2
	,sum(case when quarter = 3 then num_employees else 0 end) as Q3
	,sum(case when quarter = 4 then num_employees else 0 end) as Q4
from EMPLOYEE_DESCRIPTION
group by 1,2
order by 1,2
);