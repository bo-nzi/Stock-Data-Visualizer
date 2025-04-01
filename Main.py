#Project 3 Team 7 Main File
import csv
import requests
from io import StringIO

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
        chart_type = input("\nEnter time series option (1, 2, 3, 4): ") #asking user for chart type input
        if chart_type == '1' or chart_type == '2'or chart_type == '3' or chart_type == '4':
            return chart_type
        else:
            print("\nInvalid input. Please enter either 1 for Intraday, 2 for Daily, 3 for Weekly, or 4 for Monthly.")

def main():
    print("Stock Data Visualizer")
    print("------------------------")
    symbol = Get_Symbol() # gets stock symbol
    Chart_Type = Get_Chart_Type() #gets chart type
    Time_Series = Get_Time_Series() #gets time series


if __name__ == "__main__":
    main()



# Used to help read single column from csv file
# https://www.geeksforgeeks.org/python-read-csv-columns-into-list/