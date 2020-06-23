import random
import matplotlib
import pandas as pd
import numpy as np
import matplotlib.ticker
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

CSV_URL = "https://health-infobase.canada.ca/src/data/covidLive/covid19.csv"
data = pd.read_csv(CSV_URL)
today = data['date'].values[-1]                                                 #gets the current day date
info_of_today = data[data["date"] == today]                                     # gets the information of data matches with current date
info_of_today = info_of_today[info_of_today['prname'] != 'Canada']              # excluding the Canada data in provinces list

#info_of_today = info_of_today.sort_values(by=['numconf'], ascending=False)     # It helps to draw the pie chart in ascending order starts with maximum contributed variable

provinces = info_of_today['prname']
labels = provinces


#info_of_today.index = np.arange(0, len(info_of_today))

info_of_today['angle'] = info_of_today['numconf'] / info_of_today['numconf'].sum() * 2 * np.pi    #caluculating the Angle to draw the pie chart and calculating the total cases number and converting int 2 pi radians (360 degrees)
info_of_today['angle'].round(4)                                                                   # Rounding of data to 4 decimal points

labels = provinces                             #maintains the list of province names to variable labels
sizes = info_of_today['angle']


fig1, ax1 = plt.subplots()
ax1.pie(sizes,radius=5000,autopct='%1.1f%%',shadow=True)
ax1.axis('equal')                                                                                 # Equal aspect ratio ensures that pie is drawn as a circle.
total = sum(sizes)
# Sets the legend on the axes with province name and percentage of contribution on overall cases
plt.legend(
    loc='upper left',
    labels=['%s, %1.1f%%' % (
        l, (float(s) / total) * 100) for l, s in zip(labels, sizes)],
    prop={'size': 5}
)

plt.show()
