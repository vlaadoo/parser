from pandas_datareader import data as pdr
import yfinance as yf
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import time
import math

from Downloader.filings import Filing, FilingType

yf.pdr_override()

def get_nasdaq_tickers():
    table = pd.read_html('https://en.wikipedia.org/wiki/NASDAQ-100')[3]
    sliced_table = table[1:]
    header = table.iloc[0]
    corrected_table = sliced_table.rename(columns=header)
    tickers = corrected_table['ATVI'].tolist()
    tickers.append('ATVI')
    
    return tickers

def get_sp500_tickers():
    table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
    sliced_table = table[1:]
    header = table.iloc[0]
    corrected_table = sliced_table.rename(columns=header)
    tickers = corrected_table['MMM'].tolist()
    tickers.append('MMM')
    return tickers

tickers = get_nasdaq_tickers() + get_sp500_tickers()

for tick in range(len(tickers)):

	print(tickers[tick])
	filings_10k = Filing(cik_lookup=tickers[tick],
    	                filing_type=FilingType.FILING_10K,
        	            count=1,
            	        user_agent='vladoo')
	filings_10k.save("EDGAR", file_pattern="10-K.txt")

	filings_10q = Filing(cik_lookup=tickers[tick],
    	                filing_type=FilingType.FILING_10Q,
        	            count=1,
            	        user_agent='vladoo')
	filings_10q.save("EDGAR", file_pattern="10-Q.txt")