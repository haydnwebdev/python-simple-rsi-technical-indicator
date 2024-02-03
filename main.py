import pandas as pd
from pandas_datareader import data as web
import matplotlib.pyplot as plt
import datetime as dt
import yfinance as yf
import warnings
import os

# Turn off deprecated warnings
warnings.filterwarnings("ignore")


def clear_screen():
    """
    Clear the console on Windows, Mac and Linux.
    """
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


clear_screen()

# Initialise ticker
ticker = ""

# Check if we have a ticker, convert to uppercase
while not ticker:
    ticker = (
        input("Enter a YF ticker symbol ticker symbol (e.g BBSN.L) 'q' to quit : ")
        .upper()
        .strip()
    )

    # Allow user to quit program
    if ticker.lower() == "q":
        print("Exiting the program.")
        exit(0)


def get_date(prompt, lower_bound, upper_bound):
    """Take date input from the user and check it is within acceptable bounds."""
    while True:
        try:
            input_date = input(prompt)
            year, month, day = map(int, input_date.split("-"))
            date_obj = dt.datetime(year, month, day)
            if lower_bound <= date_obj <= upper_bound:
                return date_obj
            else:
                print(
                    f"Date must be between {lower_bound.date()} and {upper_bound.date()}."
                )
        except ValueError:
            print("Invalid date format or date. Please use YYYY-M-DD format.")


def get_time_period():
    """Define the allowed time periods, allow user to make a choice."""
    time_periods = [
        "1d",
        "5d",
        "1wk",
        "1mo",
        "3mo",
        "6mo",
        "1y",
        "2y",
        "5y",
        "10y",
        "ytd",
        "max",
    ]

    # Display the options to the user
    print("Available time periods are: " + ", ".join(time_periods))

    while True:
        # Prompt for user input
        user_input = input("Please enter your desired time period: ").strip()

        # Check if the input is valid
        if user_input in time_periods:
            return user_input
        else:
            print("Invalid input. Please choose one of the available time periods.")


# Setting the bounds
lower_bound_date = dt.datetime(1970, 1, 1)
current_date = dt.datetime.now()

# Sssign the start date
start_date = get_date(
    "Enter the start date in YYYY-MM-DD format : ", lower_bound_date, current_date
)

# Assign the end date
end_date = get_date(
    "Enter the end date in YYYY-MM-DD format : ", start_date, current_date
)

# Assign the interval period
interval_period = get_time_period()

# Replace broken yahoo-finance from pandas
yf.pdr_override()

# retrieve data from yf
data = web.DataReader(ticker, start=start_date, end=end_date, interval=interval_period)

# The difference or change in values across intervals.
delta = data["Adj Close"].diff(1)
delta.dropna(inplace=True)

positive = delta.copy()
negative = delta.copy()

positive[positive < 0] = 0
negative[negative > 0] = 0

days = 14

average_gain = positive.rolling(window=days).mean()
average_loss = abs(negative.rolling(window=days).mean())

# Perform rsi calc
relative_strength = average_gain / average_loss
RSI = 100.0 - (100.0 / (1.0 + relative_strength))

combined = pd.DataFrame()

combined["Adj Close"] = data["Adj Close"]
combined["RSI"] = RSI

# Define figure size
plt.figure(figsize=(12, 8))

# Define axis 1
ax1 = plt.subplot(211)
ax1.plot(combined.index, combined["Adj Close"], color="lightgray")
ax1.set_title("Adjusted Close Price", color="white")

ax1.grid(True, color="#555555")
ax1.set_axisbelow(True)
ax1.set_facecolor("black")
ax1.figure.set_facecolor("#121212")
ax1.tick_params(axis="x", colors="white")
ax1.tick_params(axis="y", colors="white")

# Define axis 2
ax2 = plt.subplot(212, sharex=ax1)
ax2.plot(combined.index, combined["RSI"], color="lightgray")

ax2.axhline(0, linestyle="--", alpha=0.5, color="#ff0000")
ax2.axhline(10, linestyle="--", alpha=0.5, color="#ffaa00")
ax2.axhline(20, linestyle="--", alpha=0.5, color="#00ff00")
ax2.axhline(30, linestyle="--", alpha=0.5, color="#cccccc")
ax2.axhline(70, linestyle="--", alpha=0.5, color="#cccccc")
ax2.axhline(80, linestyle="--", alpha=0.5, color="#00ff00")
ax2.axhline(90, linestyle="--", alpha=0.5, color="#ffaa00")
ax2.axhline(100, linestyle="--", alpha=0.5, color="#ff0000")

ax2.set_title("RSI Value", color="white")
ax2.grid(False)
ax2.set_axisbelow(True)
ax2.set_facecolor("black")
ax2.tick_params(axis="x", colors="white")
ax2.tick_params(axis="y", colors="white")

# Show the graph(s)
plt.show()
