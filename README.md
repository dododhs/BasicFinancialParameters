# BasicFinancialParameters: Returns, Variations, STD, Skew, Kurtosis, and Beta
My computer is MacBook Pro 2021 (Apple M1), IDE is Pycharm, python version is 3.9.5

In this section, we are going to extract historical data from Yahoo Finance in Python. 
Firt and foremost, please run this: pip install yfinance.

For Macbook M1 users, you might get below error while installing "yfinance": Could not build wheels for lxml, which is required to install pyproject.toml-based projects.
The lxml package seems to cause such errors when Xcode Command Line Tools are not correctly installed or some paths are missing/broken. 
As implied in your terminal, please try: xcode-select --install, and then run this: pip install lxml.

