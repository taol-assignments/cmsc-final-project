import argparse
import pandas as pd
import numpy as np


def doubling_rate_of_province(province, data):
    """ Calculate the doubling rates for the input province and save it into a file

    Parameters:
    argument1 (str): The name of province
    argument2 (DataFrame): the data read from covid19.csv by pandas

    Returns:
    None

   """
    # filter data by province name
    info_of_province = data[data["prname"] == province]
    # initialize the variables needed for result data
    result = {}
    pr_names = []
    num_confs = []
    dates = []
    doubling_rates = []
    # go through the filtered data row by row
    for index, row in info_of_province.iterrows():
        # get the data in a row
        pr_names.append(province)
        number = row['numconf']
        num_confs.append(number)
        date = row['date']
        dates.append(date)
        percent_today = row['percentoday']
        # calculate the doubling rate with the current confirmed number and the spreading rate
        if percent_today == 0.0:
            # if the current spreading rate is 0, then the doubling rate is infinite
            doubling_rates.append(float('inf'))
        else:
            # calculate the doubling rate when spreading rate != 0
            doubling_rate = np.ceil(np.log(2) / np.log(percent_today / 100 + 1))
            # put the doubling rate into results
            doubling_rates.append(int(doubling_rate))
    # construct the result data
    result['prname'] = pr_names
    result['numconf'] = num_confs
    result['date'] = dates
    result['doublingrate'] = doubling_rates
    # change the result data into DataFrame type
    df = pd.DataFrame(data=result)
    # save the result data as .csv for future query
    df.to_csv('covid19-' + province + '.csv')


# read the argument from command line
parser = argparse.ArgumentParser(description='calculates the doubling rate')
parser.add_argument('province', help="the name of province", type=str)
args = parser.parse_args()
# get the province name from argument
province = args.province
# dynamically read data from covid19.csv by pandas
data = pd.read_csv("https://health-infobase.canada.ca/src/data/covidLive/covid19.csv")
# calculate the doubling rate for this province
doubling_rate_of_province(province, data)
