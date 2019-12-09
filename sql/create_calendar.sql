

;with cte_generate_dummy as
(
select 
top 36500 -- 100 years...
	rn = ROW_NUMBER() over(order by x.number asc)
from master.dbo.spt_values x
cross join master.dbo.spt_values y
), cte_generate_calendar_dates as 
(
select 
	rn = rn,
	calendar_date = convert(Date,DATEADD(d, rn-1, '1991-01-01'))
from cte_generate_dummy
where DATEADD(d, rn-1, '1991-01-01') < '2020-01-01'
)
select 
	rn = rn,
	calendar_date = calendar_date,
	calendar_year = datepart(year,calendar_date),
	calendar_month = datepart(month,calendar_date),
	calendar_day = datepart(day,calendar_date),
	calendar_year_month = convert(varchar(4),datepart(year,calendar_date)) + '-' + IIF(datepart(month,calendar_date) < 10, '0' + convert(varchar(2),datepart(month,calendar_date)),convert(varchar(2),datepart(month,calendar_date))),
	is_weekend_day = IIF(datename(dw, calendar_date) = 'Saturday'OR datename(dw, calendar_date) = 'Sunday',1,0) 
into dbo.calendar
from cte_generate_calendar_dates