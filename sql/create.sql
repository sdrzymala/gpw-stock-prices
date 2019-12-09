create database GPWstockprices;

go

use GPWstockprices;

go

create table [dbo].[stock_prices]
(
    [stock_price_id] int identity(1,1),
    [prices_date] nvarchar(255),
    [symbol_name] nvarchar(255),
    [code_isin] nvarchar(255),
    [currency] nvarchar(255),
    [rate_opening] nvarchar(255),
    [rate_max] nvarchar(255),
    [rate_min] nvarchar(255),
    [rate_closing] nvarchar(255),
    [rate_diff_percentage] nvarchar(255),
    [turnover_volume_qty] nvarchar(255),
    [no_transcations] nvarchar(255),
    [turnover_value_thousands] nvarchar(255),
    [inserted_at] datetime,
    PRIMARY KEY CLUSTERED 
	(
		[stock_price_id] ASC
	)
);

go

ALTER TABLE [dbo].[stock_prices] 
	ADD CONSTRAINT [DF_stock_prices_inserted_at]  
	DEFAULT (getdate()) 
	FOR [inserted_at]