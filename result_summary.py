from calculation import result_summary
import pandas as pd

startDate = input("What's the start date (%Y-%m-%d): ")
endDate = input("What's the end date (%Y-%m-%d): ")
ticker = input("What are the tickers you need: ")

result_summary = result_summary(ticker,startDate, endDate)
print("Result Summary for " + ticker)
print("--------------------------------")
with pd.option_context('display.max_rows', None,
                       'display.max_columns', None,
                       'display.precision', 3,
                       ):
    print(result_summary)
