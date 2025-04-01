#Project 3 Team 7 Main File
import csv
import requests
from io import StringIO
from datetime import datetime

API_KEY = 'RNNX6G5V6FI46SB4'  #Replace with your API key!!!!

def Get_Symbol():
    CSV_URL = f'https://www.alphavantage.co/query?function=LISTING_STATUS&apikey={API_KEY}' # gets stock symbol list. Found under Listings and Delisting Status
    download = requests.get(CSV_URL)
    decoded_content = download.content.decode('utf-8')
    symbols_in_file = [] #used to store symbols column from csv file

    #pulls symbol column and stores it in symbols_in_file
    csv_reader = csv.DictReader(StringIO(decoded_content)) #converts each row into a dictionary and column headers are the keys.
    for col in csv_reader:
        symbols_in_file.append(col['symbol'])

    #Asks for user input, compares it to values in symbols_in_file. loops until a valid stock symbol is entered
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
        chart_type = input("Enter the chart type you want (1, 2): ") #asking user for chart type input
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
        time_series = input("\nEnter time series option (1, 2, 3, 4): ") #asking user for time series input
        if time_series == '1' or time_series == '2'or time_series == '3' or time_series == '4':
            return time_series
        else:
            print("\nInvalid input. Please enter either 1 for Intraday, 2 for Daily, 3 for Weekly, or 4 for Monthly.")

def Get_Start_Date():  
    while True: 
        start_date = input("\nEnter the start Date (YYYY-MM-DD): ") #asking user to enter end date
        try:
            date_format = datetime.strptime(start_date, "%Y-%m-%d") #makes sure date is in the corect format 
            return date_format
        except ValueError:
            print("\nInvalid input. Please enter the correct date format (YYYY-MM_DD).")

def Get_End_Date(start_date):  
    while True: 
        end_date = input("\nEnter the end Date (YYYY-MM-DD): ") #asking user to enter end date
        try:
            date_format2 = datetime.strptime(end_date, "%Y-%m-%d") #makes sure date is in the correct format 
            if date_format2 > start_date:
                return date_format2
            else:
                print("\nInvalid input. The end date must be after the start date.")
        except ValueError:
            print("\nInvalid input. Please enter the correct date format (YYYY-MM_DD).")

def main():
    print("Stock Data Visualizer")
    print("------------------------")
    symbol = Get_Symbol() # gets stock symbol
    Chart_Type = Get_Chart_Type() #gets chart type
    Time_Series = Get_Time_Series() #gets time series
    Start_Date = Get_Start_Date() #gets start date
    End_Date = Get_End_Date(Start_Date) #gets end date


if __name__ == "__main__":
    main()



# Used to help read single column from csv file
# https://www.geeksforgeeks.org/python-read-csv-columns-into-list/