from gpwstockpricestoolkit.gpwstockpricestoolkit import gpwstockpricestoolkit


start_date = "2019-12-01"
end_date = "2019-12-01"
toolkit = gpwstockpricestoolkit()
toolkit.get_rates(start_date=start_date, end_date=end_date)