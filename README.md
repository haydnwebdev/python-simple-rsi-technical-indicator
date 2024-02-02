# python-simple-rsi-technical-indicator

A simple RSI technical indicator example programmed in Python.

This program was based on an old video tutorial on YouTube by @NeuralNine that needed to be updated to work. Full credit to @NeuralNine for the orginal video and code. I simply fixed the errors, including some additional features, and it now works.

Features added include:
* Allow the user to input a ticker symbol of their choice.
* Allow the user to specify start and end dates.
* Allow the user to specify interval times.
* Added additional error-checking functionality.

USAGE:

Open a terminal and type: python main.py
Enter a ticker symbol (in Yahoo Finance format); e.g., BBSN.L would get the data for Brave Bison, a UK Aim Listed company.
Enter a start date (not before 1970) and an end date (not after the current date)
Choose an interval from the valid options provided. I suggest using 1wk initially.
The application will then spawn a window with two graphs. The first graph shows the price over the interval period, and the bottom graph shows the RSI
technical indicator.
When the RSI is above 70, it usually suggests the stock is getting overbought.
When the RSI is below 30, it usually suggests the stock has been oversold and could be entering value territory.

This application is intended for educational purposes only.


