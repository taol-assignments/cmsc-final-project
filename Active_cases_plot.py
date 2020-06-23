import random
import pandas as pd
import numpy as np
import matplotlib.ticker
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#Assigning abbreviations to the province name for easy access
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
# declaring the list of different colors for better visualization while plotting
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

# Assing the link from where we are downloading the data to CSV_URL
CSV_URL = "https://health-infobase.canada.ca/src/data/covidLive/covid19.csv"

#Function for implementing the dates in specified format for X-axis of the plots
def init_data_xaxis():
    months = mdates.MonthLocator()
    days = mdates.DayLocator()

    plt.gca().xaxis.set_major_locator(months)                                   #Sets month the locator of the major ticker.
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%b"))             # %b used in months gives the values as "Jan" "Feb" "Mar"......
    plt.gca().xaxis.set_minor_locator(days)                                     #Sets the locator of the minor ticker as days

    plt.gcf().autofmt_xdate()                                                   #formats the date "%d-%m-%y"
    plt.gcf().set_size_inches(12, 12)                                           #declaring the size of x-axis label as 12 inches

    """Convert data dictionary to matrix.
        Convert a data dictionary to a matrix. The matrix is a 2D matrix where the # of rows
        is the # of provinces and the # of columns is the # of dates.
        Args:
            data: The data dictionary which keys are date-province tuples.
            provinces: All provinces in the data dictionary.
            dates: All dates in the data dictionary.
        Returns:
            y: The 2D data matrix.
            y_tick_max: The maximum y axis tick value in log scale.
        """
def make_data_list_and_max_total(data, provinces, dates):
    max_total = 0
    y = np.zeros((len(provinces), len(dates)), dtype=int).tolist()              #initializing Zeros in case of any missed data and NA
    for k, v in data.items():
        date, province = k
        y[provinces.index(province)][dates.index(date)] = v
        max_total = max(max_total, v)
    max_total = (int(str(max_total)[0]) + 1) * 10 ** (len(str(max_total)) - 1)

    return y, max_total
"""Create a line plot.
 Make a line plot for the given data and dates and save the image to the given file name.
    The y axis is shown in log scale.
    Args:
        title: Title of the plot.
        data: The data dictionary where keys are date-province tuples.
        provinces: List of all province names.
        dates: List of all dates.
        filename: The file name to save.
        
        plt.legend()              ->places legend on the axis
        plt.xlabel(),plt.ylabel() -> sets the label for x-axis,y-axis
        plt.show()                -> to view the plot
        plt.savefig()             -> to save the image as a file
    Returns:
        line plot
        """
def make_line_plot_over_time(title, data, provinces, dates, filename):
    y, max_total = make_data_list_and_max_total(data, provinces, dates)

    found_non_zero = False
    for i in range(0, len(dates)):
        for j in range(0, len(provinces)):
            if y[j][i] != 0:
                y = [l[i:] for l in y]
                dates = dates[i:]
                found_non_zero = True
                break

        if found_non_zero:
            break

    for i, province in enumerate(provinces):
        plt.plot(dates, y[i], label=PROVINCE_ABBR[province], color=COLORS[i])

    y_ticks = [1]
    while y_ticks[-1] * 10 < max_total:
        y_ticks.append(y_ticks[-1] * 10)
    y_ticks.append(max_total)

    init_data_xaxis()

    plt.yscale('log')

    plt.gca().yaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
    plt.gca().ticklabel_format(useOffset=False, style='plain', axis='y')
    plt.ylim(top=max_total)
    plt.gca().set_yticks(y_ticks)

    plt.legend()
    plt.xlabel("period of time")
    plt.ylabel("Number of cases")
    plt.title(title)
    plt.show()
    plt.savefig(filename, bbox_inches='tight')


def main():
    data = pd.read_csv(CSV_URL)                                                                         #reading the covid-19 data CSV file from the URL
    data['date'] = pd.to_datetime(data['date'], format="%d-%m-%Y")                                      # sets the date to "%d-%m-%y" format
    data = data[(data['prname'] != 'Canada') & (data["prname"] != "Repatriated travellers")].fillna(0)  # eliminating the Canada and Repatriated travelers data from the covid data

    dates = sorted(list(set(data['date'])))                                                             # creating a list with date values from data and then sorts the list
    provinces = list(set(data['prname']))                                                               # creating a list with all the available provinces name in the taken data

    num_total = data.groupby(['date', 'prname']).sum()['numtotal'].to_dict()                            #grouping the data for particular province on given dates and then caluculates the sum of totalcases
    make_line_plot_over_time("Total Cases", num_total, provinces, dates, 'total_cases.png')             # Function call to plot the total cases of each province over time

    data["Active"] = " "                                                                                #initializing new column Active to the date to store the details of Active cases count
    for row in data:
        data['Active'] = data['numtotal'] - data['numdeaths'] - data['numrecover']                      #Active cases count is calculated by subtraction of numdeaths and numrecovered from total cases
    Active = data.groupby(['date', 'prname']).sum()['Active'].astype('int32').to_dict()                 #grouping the Active cases data for each province on given dates and caluculates the total sum and sets data type as integer
    make_line_plot_over_time("Active cases", Active, provinces, dates, 'active_cases.png')              #Function call to plot the Active cases on each province over the time


if __name__ == '__main__':
    main()