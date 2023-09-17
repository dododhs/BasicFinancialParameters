import numpy as np
import pandas as pd
import yfinance as yf

def result_summary(ticker,startDate, endDate):
    data = get_data(ticker, startDate, endDate)
    returns = get_returns_series(data['Return'], data['IsYearEnd'], data['IsMonthEnd'], data['IsWeekEnd'])
    daily = get_result(data['Return'],250)
    weekly = get_result(returns[0]['Return'],52)
    monthly = get_result(returns[1]['Return'],12)
    yearly = get_result(returns[2]['Return'],1)
    parameters = ['Period Expected Return',
                  'Annualized Expected Return',
                  'Period Return Variance',
                  'Period Return Standard Deviation',
                  'Annualized Return Standard Deviation',
                  'Period Return Skewness',
                  'Period Return Kurtosis']
    final_result = pd.DataFrame({'Daily': daily, 'Weekly': weekly, 'Monthly': monthly, 'Yearly': yearly}).map(lambda x:format(x,'.2%'))
    final_result.index = parameters
    return final_result

def get_result(Return,factor):
    ExpReturn = Return.mean()
    AExpReturn = (1+ExpReturn)**factor-1
    Var = np.var(Return)
    Std = np.sqrt(Var)
    AVar = Std * np.sqrt(factor)
    Skew = get_skew(Return)
    Kurtosis = get_kurtosis(Return)
    return ExpReturn,AExpReturn,Var, Std,AVar,Skew,Kurtosis

def get_data(ticker, startDate, endDate,):
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
    c = 0
    for i in range(len(Return)):
        c = c +(Return[i]-mean)**2
    var = c / (len(Return)-1)
    return var
def get_skew(Returns):
    Returns = Returns.drop(0)
    Returns = np.array(Returns)
    mean = Returns.mean()
    a = 0
    for i in range(len(Returns)):
        a = a +((Returns[i]-mean)/get_var(Returns))**3
    skew = a / (len(Returns)-1)
    return skew
# return a number

def get_kurtosis(Returns):
    Returns = Returns.drop(0) # this should not be written if I want this tool to be globalized
    Returns = np.array(Returns)
    mean = Returns.mean()
    b = 0
    for i in range(len(Returns)):
        b = b +((Returns[i]-mean)/get_var(Returns))**4
    kurtosis = b/(len(Returns)-1)
    return kurtosis
# return a number
