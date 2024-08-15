# LSEG Pre-Interview Coding Challenge

This solution consists of a Python 3.12 script containing 2 functions:
- one for sampling 10 entries in a csv starting with a random timeframe
- one for predicting the next 3 values in the samples

# Prerequisites
- python installed (I've used 3.12)
- pip installed
- user running the script needs to have R/W access to the folder in which the script is located (else, no outputs would be written)
- `pip install -r .\requirements.txt` 

# Input Folder Structure
- For each Stock Exchange, there must be a subfolder in the `stock_price_data_files` folder
- Each stock must be in a Stock Exchange subfolder

# Run The Script
`python .\stocks_sampling.py --numfiles <n>`
Where <n> must be either 1 or 2 (as per the Challenge File). The script won't run if:
- no input is provided
- --numfiles is different than 1 or 2
- For each stock found, there would be a CSV file created in an 'outputs' folder

# Cleanup
`python .\cleanup.py` -> removes the outputs folder
