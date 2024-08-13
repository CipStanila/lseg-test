import argparse
import sys
import os
import pandas
from datetime import datetime, timedelta
import random

STOCK_EXCHANGE_FOLDER = '.\\stock_price_data_files'

def generate_random_date(start, end):
    date_range = (end - start).days + 1
    random_date = start + timedelta(random.randrange(0, date_range))
    return random_date
    
def predict_stocks(data_points):
    print("hello")

def proccess_stocks(number_of_files):
    print(number_of_files)
    stock_exchanges_list = os.listdir(STOCK_EXCHANGE_FOLDER)
    for stock_exchange in stock_exchanges_list:
        stocks = os.listdir(STOCK_EXCHANGE_FOLDER + '\\' + stock_exchange)
        for i in range(number_of_files):
            if i > len(stocks) - 1:
                print(stock_exchange + " Does not have enough files")
                break;           
            csvFile = pandas.read_csv(STOCK_EXCHANGE_FOLDER + '\\' + stock_exchange + '\\' + stocks[i], header = None)
            minimum_timestamp = csvFile[1].min()
            maximum_timestamp = csvFile[1].max()
            
            print("Minimum Timestamp of", stocks[i], "is", minimum_timestamp)
            split = minimum_timestamp.split("-")
            #print(minimum_timestamp)
            min_datetime = datetime.strptime(minimum_timestamp, '%d-%m-%Y').date()
            max_datetime = datetime.strptime(maximum_timestamp, '%d-%m-%Y').date()
            random_datetime = generate_random_date(min_datetime, max_datetime)
            
            random_datetime = random_datetime.strftime('%d-%m-%Y')
            print(random_datetime)
            start_timestamp = next(x for x, val in enumerate(csvFile[1]) if val > random_datetime) - 1
            print(start_timestamp)
            end_timestamp = start_timestamp + 9
            if end_timestamp > len(csvFile):
                end_timestamp = len(csvFile) - 1
            out_dataframe = []
            for i in range(start_timestamp, start_timestamp + 9): 
                out_dataframe.append(csvFile.iloc[i])
            out_dataframe = pandas.DataFrame(out_dataframe)
            out_dataframe.to_csv('test.csv')
            ###TODO###
            #Eliminate weird shit in output
            #create dynamic output
            #Predict
            
if __name__ == "__main__":
    os.listdir(".")
    parser = argparse.ArgumentParser(
    )
    parser.add_argument("--numfiles", required=True, type=int, help="Enter the recommended number of files to be sampled. It must be either 1 or 2")
    args = parser.parse_args()
    number_of_files = args.numfiles

    if(number_of_files != 1 and number_of_files != 2):
        print("Invalid input! Recommended number of files must be either 1 or 2")
        sys.exit(1)
    proccess_stocks(number_of_files)

