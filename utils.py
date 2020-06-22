import pandas as pd


PROVINCE_ABBR = {
    "Alberta": "AB",
    "British Columbia": "BC",
    "Manitoba": "MB",
    "New Brunswick": "NB",
    "Newfoundland and Labrador": "NL",
    "Nova Scotia": "NS",
    "Northwest Territories": "NT",
    "Nunavut": "NU",
    "Ontario": "ON",
    "Prince Edward Island": "PE",
    "Quebec": "QC",
    "Saskatchewan": "SK",
    "Yukon": "YT"
}


COLORS = [
    'blue',
    'brown',
    'orange',
    'pink',
    'green',
    'gray',
    'red',
    'olive',
    'purple',
    'cyan',
    'lime',
    'deeppink',
    'moccasin'
]


CSV_URL = "https://health-infobase.canada.ca/src/data/covidLive/covid19.csv"


def get_csv():
    data = pd.read_csv(CSV_URL)
    data['date'] = pd.to_datetime(data['date'], format="%d-%m-%Y")
    data = data[(data['prname'] != 'Canada') & (data["prname"] != "Repatriated travellers")].fillna(0)

    dates = sorted(list(set(data['date'])))
    provinces = list(set(data['prname']))

    return data, dates, provinces
