# Project 3 Team 7 Main File
import csv
import os
import requests
from io import StringIO
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import tempfile
import webbrowser

API_KEY = 'Demo'  # Replace with your API key!!!!

def Get_Symbol():
    CSV_URL = f'https://www.alphavantage.co/query?function=LISTING_STATUS&apikey={API_KEY}' # gets stock symbol list. Found under Listings and Delisting Status
    download = requests.get(CSV_URL)
    decoded_content = download.content.decode('utf-8')
    symbols_in_file = [] # used to store symbols column from csv file

    # pulls symbol column and stores it in symbols_in_file
    csv_reader = csv.DictReader(StringIO(decoded_content)) # converts each row into a dictionary and column headers are the keys.
    for col in csv_reader:
        symbols_in_file.append(col['symbol'])

    # Asks for user input, compares it to values in symbols_in_file. loops until a valid stock symbol is entered
    while True:
        symbol = input("Enter the stock symbol you are looking for: ")
        if symbol in symbols_in_file:
            return symbol
        else:
            print("Symbol not listed. Please enter a valid stock symbol.")

def Get_Chart_Type():
    print("Chart Types")
    print("---------------")
    print("1. Bar")
    print("2. Line")
    while True: # loops until either 1 or 2 is entered
        chart_type = input("Enter the chart type you want (1, 2): ") # asking user for chart type input
        if chart_type == '1' or chart_type == '2':
            return chart_type
        else:
            print("Invalid input. Please enter either 1 for bar chart or 2 for line chart.")

def Get_Time_Series():
    print("\nSelect the Time Series of the chart you want to Generate")
    print("--------------------------------------------------------")
    print("1. Intraday")
    print("2. Daily")
    print("3. Weekly")
    print("4. Monthly")
    
    while True: # loops until either 1,2,3,4 is entered
        time_series = input("\nEnter time series option (1, 2, 3, 4): ") # asking user for time series input
        if time_series == '1' or time_series == '2' or time_series == '3' or time_series == '4':
            return time_series
        else:
            print("\nInvalid input. Please enter either 1 for Intraday, 2 for Daily, 3 for Weekly, or 4 for Monthly.")

def Get_Start_Date():  
    while True: 
        start_date = input("\nEnter the start Date (YYYY-MM-DD): ") # asking user to enter end date
        try:
            date_format = datetime.strptime(start_date, "%Y-%m-%d") # makes sure date is in the correct format 
            return date_format
        except ValueError:
            print("\nInvalid input. Please enter the correct date format (YYYY-MM-DD).")

def Get_End_Date(start_date):  
    while True: 
        end_date = input("\nEnter the end Date (YYYY-MM-DD): ") # asking user to enter end date
        try:
            date_format2 = datetime.strptime(end_date, "%Y-%m-%d") # makes sure date is in the correct format 
            if date_format2 > start_date:
                return date_format2
            else:
                print("\nInvalid input. The end date must be after the start date.")
        except ValueError:
            print("\nInvalid input. Please enter the correct date format (YYYY-MM-DD).")

def Get_Stock_Data(symbol, time_series, start_date, end_date):
    time_series_map = {
        '1': 'Time_Intraday',
        '2': 'Time_Daily',
        '3': 'Time_Weekly',
        '4': 'Time_Monthly'
    }
    
    try:
        function = time_series_map.get(time_series, 'Time_Daily')
        url = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={API_KEY}'
        
        if time_series == '1':
            url += '&interval=60min'  # Using 60-minute intervals (for easy visualization) for intraday with specif outputsize
            url += '&outputsize=full'
        
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # searching different series to locate the correct series key based on the time series type
        series_key = None
        if time_series == '1':
            series_key = next((k for k in data.keys() if "Time Series (60min)" in k), None)
        elif time_series == '2':
            series_key = next((k for k in data.keys() if "Time Series (Daily)" in k), None)
        elif time_series == '3':
            series_key = next((k for k in data.keys() if "Weekly Time Series" in k), None)
        elif time_series == '4':
            series_key = next((k for k in data.keys() if "Monthly Time Series" in k), None)
        
        if not series_key:
            raise ValueError("No time series data found in response")
        
        processed_data = {}
        for date_str, values in data[series_key].items():
            # dealing with date parsing. specifically how for intraday differs from others in terms of formatting
            if time_series == '1':  # Intraday has datetime format with hours, minutes and seconds after year,month and day
                date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                date_str_formatted = date_obj.strftime("%Y-%m-%d %H:%M:%S")
            else:  # Daily, weekly, monthly have date (year,month and day)
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                date_str_formatted = date_obj.strftime("%Y-%m-%d")
            
            if start_date.date() <= date_obj.date() <= end_date.date():
                try:
                    processed_data[date_str_formatted] = {
                        'open': float(values.get('1. open', 0)),
                        'high': float(values.get('2. high', 0)),
                        'low': float(values.get('3. low', 0)),
                        'close': float(values.get('4. close', 0)),
                        'volume': int(values.get('5. volume', 0))
                    }
                except (ValueError, TypeError):
                    continue
        
        return processed_data if processed_data else None
        
    except Exception as e:
        print(f"Error retrieving stock data: {e}")
        return None

def Generate_Chart(data, chart_type, symbol, time_series, start_date, end_date):
    if not data:
        print("\nNo data available for the selected date range.")
        print(f"You requested: {start_date.date()} to {end_date.date()}")
        
        # If not data erros, syntax will handle it by trying to get the most recent data point in the symbol by looking at least two weeks (14 days) back
        recent_end_date = datetime.now()
        recent_start_date = recent_end_date - timedelta(days=30) 
        recent_data = Get_Stock_Data(symbol, time_series, recent_start_date, recent_end_date)
        
        if recent_data:
            all_dates = sorted(recent_data.keys())
            print("\nMost recent available data:")
            print(f"From: {all_dates[0].split()[0]}")
            print(f"To: {all_dates[-1].split()[0]}")
        else:
            # If no data error still shows up, syntax will try any available data timeline
            print("\nAttempting to find any available data for this symbol!")
            test_data = Get_Stock_Data(symbol, time_series, 
                                     datetime(1990, 1, 1),  
                                     datetime.now())        # # Syntax tries older date to current date set by user
            if test_data:
                all_dates = sorted(test_data.keys())
                print("\nAvailable date ranges for this stock:")
                print(f"Earliest date: {all_dates[0].split()[0]}")
                print(f"Latest date: {all_dates[-1].split()[0]}")
            else:
                print("\nCould not retrieve any data for this symbol/time series.")
     
        return
    
    dates = sorted(data.keys())
    closing_prices = [data[date]['close'] for date in dates]
    
    plt.figure(figsize=(12, 6))
    if chart_type == '1':
        plt.bar(dates, closing_prices, width=0.6, color='blue', alpha=0.7)
    else:
        plt.plot(dates, closing_prices, marker='o', linestyle='-', color='green')
    
    plt.title(f'{symbol} Stock Price ({start_date.date()} to {end_date.date()})')
    plt.xlabel('Date')
    plt.ylabel('Price ($)')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    temp_file = tempfile.mktemp(suffix='.html')
    plt.savefig(temp_file.replace('.html', '.png'))
    
    html_content = f"""
    <html>
        <body>
            <img src="{temp_file.replace('.html', '.png')}" style="width:100%">
            <p>Date range: {start_date.date()} to {end_date.date()}</p>
        </body>
    </html>
    """
    
    with open(temp_file, 'w') as f:
        f.write(html_content)
    
    webbrowser.open(f'file://{os.path.abspath(temp_file)}')
    plt.close()
    
def main():
    print("\nStock Data Visualizer")
    print("----------------------")
    
    # Get user inputs
    symbol = Get_Symbol()
    chart_type = Get_Chart_Type()
    time_series = Get_Time_Series()
    start_date = Get_Start_Date()
    end_date = Get_End_Date(start_date)
    
    # Retrieve and display data
    stock_data = Get_Stock_Data(symbol, time_series, start_date, end_date)
    Generate_Chart(stock_data, chart_type, symbol, time_series, start_date, end_date)
    
if __name__ == "__main__":
    main()
