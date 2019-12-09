select 
	c.calendar_date,
	count(s.stock_price_id)
from dbo.calendar c (nolock)
left join [dbo].[stock_prices] s (nolock)
	on c.calendar_date = convert(date,substring(prices_date,7,4) + '-' + substring(prices_date,4,2) + '-' + substring(prices_date,1,2))
where 
	c.is_weekend_day = 0 
	and c.calendar_date >= '2000-01-01'
	and c.calendar_date <= '2019-12-01'
group by 
	c.calendar_date
having count(s.stock_price_id) = 0
order by 1 desc

