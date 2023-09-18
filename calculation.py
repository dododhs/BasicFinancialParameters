import numpy as np
import pandas as pd
import yfinance as yf


def result_summary(ticker, startDate, endDate):
    data = get_data(ticker, startDate, endDate)
    market = get_data('^GSPC', startDate, endDate)

    returns = get_return_series(data['Close'], data['IsYearEnd'], data['IsMonthEnd'], data['IsWeekEnd'])
    returns = list(returns)
    returns[0]=returns[0].drop(0)
    returns[1]=returns[1].drop([0])
    returns[2]=returns[2].drop(0)
    market_returns = get_return_series(market['Close'], market['IsYearEnd'], market['IsMonthEnd'], market['IsWeekEnd'])
    market_returns = list(market_returns)
    market_returns[0]=market_returns[0].drop(0)
    market_returns[1]=market_returns[1].drop(0)
    market_returns[2]=market_returns[2].drop(0)

    daily = get_result(data['Return'], market['Return'], 250)
    weekly = get_result(returns[0]['Return'], market_returns[0]['Return'], 52)
    monthly = get_result(returns[1]['Return'], market_returns[1]['Return'], 12)
    yearly = get_result(returns[2]['Return'], market_returns[2]['Return'], 1)

    parameters = ['Number of Returns',
                  'Period Expected Return',
                  'Annualized Expected Return',
                  'Period Return Variance',
                  'Period Return Standard Deviation',
                  'Annualized Return Standard Deviation',
                  'Period Return Skewness',
                  'Period Return Kurtosis',
                  'Beta']
    final_result = pd.DataFrame({'Daily': daily, 'Weekly': weekly, 'Monthly': monthly, 'Yearly': yearly}).map(
        lambda x: format(x, '.2%'))
    final_result.index = parameters
    return final_result

def get_data(ticker, startDate, endDate):
    data = yf.Ticker(ticker).history(start=startDate, end=endDate).reset_index()
    data['YearID'] = np.nan
    data['WeekID'] = np.nan
    data['MonthID'] = np.nan
    for i in range(len(data['Date'])):
        data['YearID'][i] = data['Date'][i].year
        data['MonthID'][i] = data['Date'][i].year * 12 + data['Date'][i].month
        data['WeekID'][i] = data['Date'][i].year * 53 + data['Date'][i].week

    list = ['Year', 'Month', 'Week']
    for i in range(len(list)):
        data['Is' + list[i] + 'End'] = np.nan
        data['Is' + list[i] + 'End'][0] = 'Yes'
        for j in range(1, len(data['Date'])):
            if data[list[i] + 'ID'][j] == data[list[i] + 'ID'][j - 1]:
                data['Is' + list[i] + 'End'][j] = 'No'
            else:
                data['Is' + list[i] + 'End'][j] = 'Yes'

    data['Return'] = data['Close'] / data['Close'].shift(1) - 1
    return data
# return a dataframe that includes Daily return series, W/M/Y id, and start date check result

def get_return_series(Price, IsYearEnd, IsMonthEnd, IsWeekEnd):
    weekly = pd.concat([Price, IsWeekEnd], axis=1)
    weekly = weekly.drop(weekly[weekly['IsWeekEnd'] == 'No'].index)
    weekly['Return'] = weekly['Close'] / weekly['Close'].shift(1) - 1
    monthly = pd.concat([Price, IsMonthEnd], axis=1)
    monthly = monthly.drop(monthly[monthly['IsMonthEnd'] == 'No'].index)
    monthly['Return'] = monthly['Close'] / monthly['Close'].shift(1) - 1
    yearly = pd.concat([Price, IsYearEnd], axis=1)
    yearly = yearly.drop(yearly[yearly['IsYearEnd'] == 'No'].index)
    yearly['Return'] = yearly['Close'] / yearly['Close'].shift(1) - 1
    return weekly, monthly, yearly
# return a list that contains three dataframes: W/M/Y return

def get_result(Return, market_return, factor):
    Number = len(Return)
    ExpReturn = Return.mean()
    AExpReturn = (1 + ExpReturn) ** factor - 1
    Var = get_var(Return)
    Std = np.sqrt(Var)
    AVar = Std * np.sqrt(factor)
    Skew = get_skew(Return)
    Kurtosis = get_kurtosis(Return)
    Beta = get_beta(Return, market_return)
    return Number, ExpReturn, AExpReturn, Var, Std, AVar, Skew, Kurtosis, Beta

def get_var(Return):
    Return = np.array(Return)
    mean = Return.mean()
    var = 0
    for i in range(len(Return)):
        var = var + (Return[i] - mean) ** 2
    var = var / (len(Return) - 1)
    return var

def get_skew(Return):
    Return = np.array(Return)
    mean = Return.mean()
    a = 0
    for i in range(len(Return)):
        a = a + ((Return[i] - mean) / get_var(Return)) ** 3
    skew = a / (len(Return) - 1)
    return skew

def get_kurtosis(Return):
    Return = np.array(Return)
    mean = Return.mean()
    b = 0
    for i in range(len(Return)):
        b = b + ((Return[i] - mean) / get_var(Return)) ** 4
    kurtosis = b / (len(Return) - 1)
    return kurtosis

def get_beta(Return, market):
    Return = np.array(Return)
    mean_stock = Return.mean()
    market = np.array(market)
    mean_market = market.mean()
    c = 0
    for i in range(len(Return)):
        c = c + ((Return[i] - mean_stock) * (market[i] - mean_market)) / get_var(market)
    beta = c / (len(Return) - 1)
    return beta
