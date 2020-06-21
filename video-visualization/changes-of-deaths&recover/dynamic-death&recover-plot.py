import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.animation import FFMpegWriter
plt.rcParams['animation.ffmpeg_path'] = "D:\\ffmpeg-20200619-2f59946-win64-static\\bin\\ffmpeg.exe"

data = pd.read_csv("https://health-infobase.canada.ca/src/data/covidLive/covid19.csv")
province = 'Alberta'
info_of_province = data[data["prname"] == province]
dates = info_of_province.iloc[:, 3].values
num_deaths = info_of_province.iloc[:, 6].values
info_of_province['numrecover'] = info_of_province['numrecover'].fillna(method='ffill')
num_recovers = info_of_province.iloc[:, 9].values
length = len(dates)

fig, ax = plt.subplots()
ax.set_ylabel('Number of people')
plt.title("The change of Deaths and Recovers in " + province)
metadata = dict(title='Dynamic changes of deaths and recovers', artist='Matplotlib',
                comment='Movie support!')
writer = FFMpegWriter(fps=2, metadata=metadata)
with writer.saving(fig, "Dynamic-death-change-" + province + '.mp4', 100):
    for i in range(0, int(length / 5) + 1):
        i += 1
        right = i * 5
        if right > length:
            right = length
        x = dates[0:right]
        y = num_deaths[0:right]
        y1 = num_recovers[0:right]
        ax.plot(x, y, '-o', markevery=[right - 1], color='black', markerfacecolor='red', label="number of deaths")
        ax.plot(x, y1, '-o', markevery=[right - 1], color='green', markerfacecolor='blue', label="number of recovers")
        if i == 1:
            ax.legend(loc='upper left')
        ax.axis([0, 10, 0, num_recovers[-1] + 2])
        xticks = list(range(0, len(dates), 7))
        xlabels = [dates[i] for i in xticks]
        # xticks.append(len(dates))
        # xlabels.append(dates[-1])
        ax.set_xticks(xticks)
        ax.set_xticklabels(xlabels, rotation=40)
        plt.tight_layout()
        writer.grab_frame()
        # fig.savefig('death-changes-' + str(i) + "-" + province + '.png')