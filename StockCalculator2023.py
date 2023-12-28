#!/usr/bin/env python
# coding: utf-8

# In[10]:


import time
import datetime
import pandas as pd
import numpy as np
import holidays

from collections import OrderedDict
HOLIDAYS_US = holidays.US()

ONE_DAY = datetime.timedelta(days=1)

def next_business_day(aDay):

    while aDay.weekday() in holidays.WEEKEND or aDay in HOLIDAYS_US:
        aDay = aDay + pd.Timedelta(1, unit='D')
    return aDay

def calc(df):
    target_dates = pd.date_range(start_date, end_date, freq='MS')  # .strftime('%Y-%m-%d').tolist()

    period1 = int(time.mktime(datetime.datetime(2000, 1, 1, 23, 59).timetuple()))
    period2 = int(time.mktime(datetime.datetime.now().timetuple()))
    interval = '1d'  # 1d, 1m

    total_shares = 0

    holdings_df = pd.DataFrame(
        columns=["Date", "Share Price", "Shares Purchased", "Dividend", "Dividend Shares", "Dividend Payout"])

    dividends_df = pd.DataFrame(
        columns=["Date", "Share Price", "Shares Purchased", "Dividend", "Dividend Shares", "Dividend Payout"])
    dividends = list()


    def record_dividend(date, dividend):
        return entry


    # Get date from feed(s)
    stock_query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
    stock_df = pd.read_csv(stock_query_string)

    div_query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={period1}&period2={period2}&interval={interval}&events=div&includeAdjustedClose=true'
    div_df = pd.read_csv(div_query_string, parse_dates=['Date'])
    div_df.set_index('Date', inplace=True)
    div_df.sort_index(inplace=True)

    # identify business days in the range
    bus_days = map(lambda x: next_business_day(x), target_dates)
    bus_day_list = list(bus_days)

    # Preform initial purchase if any
    if initial_investment != 0:
        try:
            initial_investment_close_price = \
            stock_df.loc[stock_df.Date == bus_day_list[0].date().strftime('%Y-%m-%d')].Close.values[0]
            entry = pd.DataFrame({'Date': bus_day_list[0].date().strftime('%Y-%m-%d'),
                'Share Price': initial_investment_close_price,
                'Shares Purchased': initial_investment / initial_investment_close_price},
                index=[bus_day_list[0].date().strftime('%Y-%m-%d')])
            holdings_df = pd.concat([holdings_df, entry]).sort_index()
            total_shares = initial_investment / initial_investment_close_price
        except:
            pass
    # Calculate Holdings for begining of month

    close_prices = []
    for day in bus_day_list:
        try:
            carr = stock_df.loc[stock_df.Date == day.date().strftime('%Y-%m-%d')].Close.values
            if carr.size == 0:
                next_day = day - pd.offsets.BDay() - pd.offsets.BDay()
                carr = stock_df.loc[stock_df.Date == day.date().strftime('%Y-%m-%d')].Close.values

            if carr.size != 0:
                close = carr[0]

            close_prices.append((day.date().strftime('%Y-%m-%d'), close))
            entry = pd.DataFrame({'Date': day.date(), 'Share Price': close, 'Shares Purchased': monthly_investment / close},
                                 index=[0])
            holdings_df = pd.concat([holdings_df, entry], ignore_index=True)
        except:
            pass
            

    holdings_df['Date'] = pd.to_datetime(holdings_df['Date'])
    holdings_df.set_index('Date', inplace=True)

    # Calculate Dividends - if any - as they occurred
    divs_to_consider_df = div_df.loc[start_date:end_date]
    for div_date, dividend in divs_to_consider_df.itertuples():
        if reinvest:
            close_price_on_date = stock_df.loc[stock_df.Date == div_date.strftime('%Y-%m-%d')].Close.values[0]
            entry = pd.DataFrame({
                "Share Price": close_price_on_date,
                "Shares Purchased": (holdings_df[:div_date]['Shares Purchased'].sum()) * dividend / close_price_on_date,
                "Dividend": dividend,
                "Dividend Shares": holdings_df[:div_date]['Shares Purchased'].sum(),
                "Dividend Payout": 0
            }, index=[div_date]).sort_index()
        else:
            entry = pd.DataFrame({
                "Dividend": dividend,
                "Dividend Shares": holdings_df[:div_date]['Shares Purchased'].sum(),
                "Dividend Payout": (holdings_df[:div_date]['Shares Purchased'].sum()) * dividend
            }, index=[div_date]).sort_index()

        holdings_df = pd.concat([holdings_df, entry]).sort_index()

    for price in close_prices:
        monthly_shares = monthly_investment / price[1]
        total_shares = total_shares + monthly_shares

    total_shares = holdings_df['Shares Purchased'].sum()
    value = total_shares * close_prices[-1][1]
    df = holdings_df.replace(np.nan, '').sort_index()
    print("would spend ", (len(close_prices) * monthly_investment) + initial_investment, " over ", len(close_prices),
          "months")
    print("and would have: ", total_shares, " shares, worth ", value, " at ", close_prices[-1][1])
    print("Dividends erned: ", holdings_df['Dividend Payout'].sum())
    return df


# In[15]:


# Analysis Data
# ETF: QYLD, NUSI, RYLD
# Divident ETFs: SCHD, JEPI, DIVO, VTI
# Stocks:AAPL, MS, MSFT
ticker = 'aapl'
start_date = '2023-01-01'
end_date = '2023-12-27'
initial_investment = 10000
monthly_investment = 0
reinvest = False
interval = "d"
df = pd.DataFrame(
    columns=["Date", "Share Price", "Shares Purchased", "Dividend", "Dividend Shares", "Dividend Payout"])
a=calc(df)
a

