import argparse
import pandas as pd
import numpy as np

parser = argparse.ArgumentParser(description='calculates the doubling rate')
parser.add_argument('province', help="the name of province", type=str)
# parser.add_argument('number', help="the number of cases or number of deaths", type=int)
# parser.add_argument('date', help="the corresponding date", type=str)
args = parser.parse_args()
province = args.province
#number = args.number
#date = args.date
data = pd.read_csv("https://health-infobase.canada.ca/src/data/covidLive/covid19.csv")
# query = 'prname =="' + province + '" & date ==' + '"' + date + '"'
info_of_province = data[data["prname"] == province]
result = {}
pr_names = []
num_confs = []
dates = []
doubling_rates = []
for index, row in info_of_province.iterrows():
    pr_names.append(province)
    number = row['numconf']
    num_confs.append(number)
    date = row['date']
    dates.append(date)
    percent_today = row['percentoday']
    if percent_today == 0.0:
        doubling_rates.append(float('inf'))
    else:
        # percent_today = percent_today[percent_today.index][0]
        doubling_rate = np.ceil(np.log(2) / np.log(percent_today / 100 + 1))
        doubling_rates.append(int(doubling_rate))
result['prname'] = pr_names
result['numconf'] = num_confs
result['date'] = dates
result['doublingrate'] = doubling_rates
df = pd.DataFrame(data=result)
df.to_csv('covid19-' + province + '.csv')

