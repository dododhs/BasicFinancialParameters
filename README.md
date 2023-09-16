# BasicFinancialParameters: Returns, Variations, STD, Skew, Kurtosis, and Beta
My computer is MacBook Pro 2021 (Apple M1), IDE is Pycharm, python version is 3.9.5

In this section, we are going to extract historical data from Yahoo Finance in Python. 
Firt and foremost, please run this: pip install yfinance.

For Macbook M1 users, you might get below error while installing "yfinance": Could not build wheels for lxml, which is required to install pyproject.toml-based projects.
The lxml package seems to cause such errors when Xcode Command Line Tools are not correctly installed or some paths are missing/broken. 
As implied in your terminal, please try: xcode-select --install, and then run this: pip install lxml.

*Solution introduced by bkaankuguoglu
** Background information: Xcode
XCode, Apple’s proprietary Integrated Development Environment (IDE), is akin to the construction site and tools, specifically designed for erecting structures within the Apple ecosystem. It’s a comprehensive suite that facilitates the development, testing, and debugging of software for macOS, iOS, WatchOS, and tvOS. 
Now, imagine being tasked to build a skyscraper (an application) on an Apple construction site (XCode) using a Python blueprint (Python script). This combination allows developers to leverage the robustness of XCode’s tools and the flexibility of Python, creating a unique structure that is both sturdy (runs smoothly on Apple platforms) and versatile (utilizes the power of Python).
By using Python in XCode, they can develop applications that run smoothly on Apple platforms while harnessing the power of Python.
