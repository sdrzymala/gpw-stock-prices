# web scrapping
from bs4 import BeautifulSoup
import requests

# database related
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
import pyodbc

# other
import time
import urllib
from datetime import timedelta, date, datetime




class gpwstockpricestoolkit:




    def __init__(self):

        db_connectionstring = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=192.168.8.149;DATABASE=GPWstockprices;UID=sa;PWD=Pass@word2@"
        #url should be: "https://www.gpw.pl/archiwum-notowan-full?type=10&instrument=&date=27-11-2018"
        self.base_url = "https://www.gpw.pl/archiwum-notowan-full?type=10&instrument=&date="
        self.db_connectionstring = db_connectionstring
                
        # try to connect
        print (db_connectionstring)
        is_connected = False
        max_retries = 15
        i = 1
        while i <= max_retries and is_connected == False:
            try:
                pyodbc.connect(db_connectionstring)
                is_connected = True
            except pyodbc.Error as e:
                sqlstate = e.args[0]
                if sqlstate == '08001':
                    print ("The database is still starting, attempt {0}/{1}".format(i, max_retries))
                    i = i + 1
                    time.sleep(5)
                    continue
                else:
                    raise ValueError("There was unexpected error while trying to connect to the database. Error: {0}".format(sqlstate))

        params = urllib.parse.quote_plus(db_connectionstring)
        Base = automap_base()
        engine = create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))
        
        Base.prepare(engine, reflect=True)
        self.__stock_prices = Base.classes.stock_prices
        self.__session = Session(engine)
        


    def daterange(self, start_date, end_date):
        for n in range(int ((end_date - start_date).days)):
            yield start_date + timedelta(n)


    def get_rates(self, start_date, end_date):
        
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        for single_date in self.daterange(start_date, end_date):
            
            single_date_string = str(single_date.strftime("%d-%m-%Y"))
            day_name = single_date.strftime("%A") 
            single_date_current_data_count = self.__session.query(self.__stock_prices).filter(self.__stock_prices.prices_date == single_date_string).count()
           
            # download webpage only if:
            # a) the given date is not a weekend date
            # b) the data is not already downloaded
            if day_name not in ["Saturday","Sunday"] and single_date_current_data_count == 0:
                try:
                    self.get_single_day_rates(single_date_string)
                except:
                    print ("error while getting prices for date:  " + single_date_string)



    def get_single_day_rates(self, prices_date):

        rates = []

        # get html content from page 
        current_page_url = self.base_url + prices_date
        r = requests.get(current_page_url)
        html = r.text

        # convert to beautiful soup object
        # and extract get stock prices
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table', attrs={'class':'table footable'})
        rows = table.find_all('tr')
        del rows[0] # remove first row (header)
        
        # iterate and save stock prices
        for row in rows:
            
            cols = row.find_all('td')

            symbol_name = cols[0].text.strip()
            code_isin = cols[1].text.strip()
            currency = cols[2].text.strip()
            rate_opening = cols[3].text.strip()
            rate_max = cols[4].text.strip()
            rate_min = cols[5].text.strip()
            rate_closing = cols[6].text.strip()
            rate_diff_percentage = cols[7].text.strip()
            turnover_volume_qty = cols[8].text.strip()
            no_transcations = cols[9].text.strip()
            turnover_value_thousands = cols[10].text.strip()

            current_stock_price = self.__stock_prices(
                prices_date = prices_date,
                symbol_name = symbol_name,
                code_isin = code_isin, 
                currency = currency,
                rate_opening = rate_opening,
                rate_max = rate_max, 
                rate_min = rate_min, 
                rate_closing = rate_closing, 
                rate_diff_percentage = rate_diff_percentage, 
                turnover_volume_qty = turnover_volume_qty,
                no_transcations = no_transcations,
                turnover_value_thousands = turnover_value_thousands
            )

            self.__session.add(current_stock_price)
            self.__session.commit()

            
