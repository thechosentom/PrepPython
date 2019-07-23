#################################
# Tableau Prep | TabPy          #
# Scenario 2: Bring in web data #
#################################

import time
import pandas_datareader as dr
#import pandas as pd
from datetime import datetime, timedelta

def getstock(df):

    dataframe = pd.DataFrame()

    for stock in df['Yahoo Ticker']:
        try:
            yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
            stockdf = dr.DataReader(stock, 'yahoo', '2016-12-01', yesterday)

            del stockdf['Close']
            # rename Adjusted Close to Close
            stockdf.rename(columns={'Adj Close': 'Close'}, inplace=True)

            start_date = stockdf.index.min()
            end_date = stockdf.index.max()
            all_weekdays = pd.date_range(start=start_date, end=end_date, freq='B')

            # Filling missing weekdays
            stockdf = stockdf.reindex(all_weekdays)
            stockdf = stockdf.fillna(method='ffill')
            stockdf['Stock'] = stock

            stockdf['% Change'] = stockdf['Close'].pct_change(1)
            stockdf['Change'] = stockdf['Close'].diff()
            stockdf['High-Low Diff'] = stockdf['High'] - stockdf['Low']
            stockdf['14ATR'] = stockdf['High-Low Diff'].abs().rolling(window=14).mean()
            stockdf['20ATR'] = stockdf['High-Low Diff'].abs().rolling(window=20).mean()

            stockdf = stockdf.reset_index()
            stockdf.rename(columns={'index': 'Date'}, inplace=True)
            stockdf['Date'] = stockdf['Date'].astype(str)

            dataframe = dataframe.append(stockdf)

        except Exception as e:
            print (e)
            pass

    df = dataframe
    return df

def get_output_schema():
    return pd.DataFrame({
        'Stock' : prep_string(),
        'Date' : prep_string(),
        'High' : prep_decimal(),
        'Low' : prep_decimal(),
        'Open': prep_decimal(),
        'Volume': prep_decimal(),
        'Close': prep_decimal(),
        '% Change': prep_decimal(),
        'Change' : prep_decimal(),
        'High-Low Diff': prep_decimal(),
        '14ATR': prep_decimal(),
        '20ATR': prep_decimal(),
        })
