import numpy as np
import pandas as pd
import yfinance as yf

def result_summary(ticker,startDate,endDate):
    data = get_data(ticker, startDate, endDate)
    market = get_data('^GSPC',startDate,endDate)
    returns = get_returns_series(data['Return'], data['IsYearEnd'], data['IsMonthEnd'], data['IsWeekEnd'])
    market_returns = get_returns_series(market['Return'],market['IsYearEnd'], market['IsMonthEnd'], market['IsWeekEnd'])
    
    daily = get_result(data['Return'],market['Return'],250)
    weekly = get_result(returns[0]['Return'],market_returns[0]['Return'],52)
    monthly = get_result(returns[1]['Return'],market_returns[1]['Return'],12)
    yearly = get_result(returns[2]['Return'],market_returns[2]['Return'],1)
    
    parameters = ['Number of Returns',
                  'Period Expected Return',
                  'Annualized Expected Return',
                  'Period Return Variance',
                  'Period Return Standard Deviation',
                  'Annualized Return Standard Deviation',
                  'Period Return Skewness',
                  'Period Return Kurtosis',
                  'Beta']
    final_result = pd.DataFrame({'Daily': daily, 'Weekly': weekly, 'Monthly': monthly, 'Yearly': yearly}).map(lambda x:format(x,'.2%'))
    final_result.index = parameters
    return final_result

def get_result(Return,market_return,factor):
    Number = len(Return)
    ExpReturn = Return.mean()
    AExpReturn = (1+ExpReturn)**factor-1
    Var = np.var(Return)
    Std = np.sqrt(Var)
    AVar = Std * np.sqrt(factor)
    Skew = get_skew(Return)
    Kurtosis = get_kurtosis(Return)
    Beta = get_beta(Return,market_return)
    return Number,ExpReturn,AExpReturn,Var, Std,AVar,Skew,Kurtosis,Beta

def get_data(ticker, startDate, endDate):
    data = yf.Ticker(ticker).history(start = startDate, end = endDate).reset_index()
    data['YearID'] = np.nan
    data['WeekID'] = np.nan
    data['MonthID'] = np.nan
    for i in range(len(data['Date'])):
        data['YearID'][i] = data['Date'][i].year
        data['MonthID'][i] = data['Date'][i].year *12 + data['Date'][i].month
        data['WeekID'][i] = data['Date'][i].year *53 +data['Date'][i].week

    list = ['Year','Month','Week']
    for i in range(len(list)):
        data['Is'+list[i]+'End'] = np.nan
        data['Is' + list[i] + 'End'][0] = 'Yes'
        for j in range(1, len(data['Date'])):
            if data[list[i]+'ID'][j] == data[list[i]+'ID'][j-1]:
                data['Is' + list[i] + 'End'][j] = 'No'
            else:
                data['Is' + list[i] + 'End'][j] = 'Yes'

    data['Return'] = data['Close']/data['Close'].shift(1)  - 1
    return data
# return a dataframe that includes Daily return series, W/M/Y id, and start date check result

def get_returns_series(DailyReturn, IsYearEnd, IsMonthEnd, IsWeekEnd):
    week = pd.concat([DailyReturn, IsWeekEnd], axis=1)
    WeeklyReturn = week.drop(week[week['IsWeekEnd'] == 'No'].index)
    month = pd.concat([DailyReturn,IsMonthEnd], axis=1)
    MonthlyReturn = month.drop(month[month['IsMonthEnd']=='No'].index)
    year = pd.concat([DailyReturn, IsYearEnd], axis=1)
    YearlyReturn = year.drop(year[year['IsYearEnd'] == 'No'].index)
    return WeeklyReturn, MonthlyReturn, YearlyReturn
# return a list that contains three dataframes: W/M/Y return

def get_var(Return):
    mean = Return.mean()
    var = 0
    for i in range(len(Return)):
        var = var +(Return[i]-mean)**2
    var = var / (len(Return)-1)
    return var
def get_skew(Return):
    Return = Return.drop(0)
    Return = np.array(Return)
    mean = Return.mean()
    a = 0
    for i in range(len(Return)):
        a = a +((Return[i]-mean)/get_var(Return))**3
    skew = a / (len(Return)-1)
    return skew
# return a number

def get_kurtosis(Return):
    Return = Return.drop(0) # this should not be written if I want this tool to be globalized
    Return = np.array(Return)
    mean = Return.mean()
    b = 0
    for i in range(len(Return)):
        b = b +((Return[i]-mean)/get_var(Return))**4
    kurtosis = b/(len(Return)-1)
    return kurtosis
# return a number

def get_beta(Return,market):
    Return = Return.drop(0)
    Return = np.array(Return)
    mean_stock = Return.mean()

    market = market.drop(0)
    market = np.array(market)
    mean_market = market.mean()

    c=0
    for i in range(len(Return)):
        c = c +((Return[i]-mean_stock)*(market[i]-mean_market))/get_var(market)
    beta = c/(len(Return)-1)
    return beta
# return a number
