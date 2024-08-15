import argparse
import sys
import os
import pandas
from datetime import datetime, timedelta
import random

STOCK_EXCHANGE_FOLDER = '.\\stock_price_data_files'
NUMBER_OF_DAYS = 3

def predict_stocks(out_dataframe, days):
    #Compute First Prediction
    predict_dataframe = out_dataframe
    last_day = predict_dataframe.iat[-1,1] 
    predicted_datapoints = []
    first_datapoint = predict_dataframe[2].nlargest(2).iloc[-1] #second largest value in samples
    stock_name = predict_dataframe.iat[0,0] 
    
    first_datapoint_timestamp = (datetime.strptime(last_day, '%d-%m-%Y').date() + timedelta(days = 1)).strftime('%d-%m-%Y')
    #append to the output file for this stock
    pandas.DataFrame([[stock_name, first_datapoint_timestamp, first_datapoint]]).to_csv('outputs\\' + stock_name + '.csv', header = False, index = False, mode = 'a')
    
    exp = 1
    #Predict the next days and append the prediction to the stock file
    for day in range(2, days+1):
        new_timestamp = (datetime.strptime(last_day, '%d-%m-%Y').date() + timedelta(days = day)).strftime('%d-%m-%Y')
        prediction = predict_dataframe.iat[len(predict_dataframe) - 1, 2] + (predict_dataframe.iat[len(predict_dataframe) - 1, 2] - predict_dataframe.iat[len(predict_dataframe) - 2, 2]) / 2**exp 

        pandas.DataFrame([[stock_name, new_timestamp, prediction]]).to_csv('outputs\\' + stock_name + '.csv', header = False, index = False, mode = 'a')        
        exp += 1


def generate_random_date(start, end):
    date_range = (end - start).days + 1
    random_date = start + timedelta(random.randrange(0, date_range))
    return random_date
    

def proccess_stocks(number_of_files):
    stock_exchanges_list = os.listdir(STOCK_EXCHANGE_FOLDER)
    for stock_exchange in stock_exchanges_list:
        stocks = os.listdir(STOCK_EXCHANGE_FOLDER + '\\' + stock_exchange)
        for i in range(number_of_files):
            #Check if we don't exceed the files that we can read 
            if i > len(stocks) - 1:
                print(stock_exchange + " Does not have enough files")
                break;
            #Check if file is a csv
            if (not (STOCK_EXCHANGE_FOLDER + '\\' + stock_exchange + '\\' + stocks[i]).endswith('.csv')):
                print(stocks[i], "is not a csv. Skipping")
                continue
            #Check if file is empty
            if (os.stat(STOCK_EXCHANGE_FOLDER + '\\' + stock_exchange + '\\' + stocks[i]).st_size == 0):
                print(stocks[i], "This file is empty. Skipping")
                continue      
            csvFile = pandas.read_csv(STOCK_EXCHANGE_FOLDER + '\\' + stock_exchange + '\\' + stocks[i], header = None)
            #First and last elements of the CSV Files have the minimum and maximum timestamp
            minimum_timestamp = csvFile[1][0]
            maximum_timestamp = csvFile[1][len(csvFile[1])-1]
            stock_name = csvFile[0][1]
            split = minimum_timestamp.split("-")
            min_datetime = datetime.strptime(minimum_timestamp, '%d-%m-%Y').date()
            max_datetime = datetime.strptime(maximum_timestamp, '%d-%m-%Y').date()
            #Generate a random date to start sampling
            random_datetime = generate_random_date(min_datetime, max_datetime)
            
            random_datetime = random_datetime.strftime('%d-%m-%Y')
            #get the index where we need to start collecting the samples (first value greater or equal than the random date)
            start_timestamp = next(x for x, val in enumerate(csvFile[1]) if val >= random_datetime) - 1


            end_timestamp = start_timestamp + 10
            #Check if we exceed the length of the csv file
            if end_timestamp > len(csvFile):
                end_timestamp = len(csvFile) - 1


            out_dataframe = []
            
            for idx in range(start_timestamp, end_timestamp): 
                out_dataframe.append(csvFile.iloc[idx])

            out_dataframe = pandas.DataFrame(out_dataframe)
            #Save samples in an outputs folder
            if (not os.path.exists('outputs')):
                os.mkdir('outputs')
            out_dataframe.to_csv('outputs/' + stocks[i], header = False, index = False)           

            #Predict the next 3 values
            out_dataframe = predict_stocks(out_dataframe, NUMBER_OF_DAYS)



        
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
    )
    parser.add_argument("--numfiles", required=True, type=int, help="Enter the recommended number of files to be sampled. It must be either 1 or 2")
    args = parser.parse_args()
    number_of_files = args.numfiles

    #As per the Challenge Document, the possible input values are either 1 or 2

    if(number_of_files != 1 and number_of_files != 2):
        print("Invalid input! Recommended number of files must be either 1 or 2")
        sys.exit(1)


    proccess_stocks(number_of_files)

