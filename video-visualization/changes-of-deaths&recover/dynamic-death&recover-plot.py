import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.animation import FFMpegWriter
plt.rcParams['animation.ffmpeg_path'] = "D:\\ffmpeg-20200619-2f59946-win64-static\\bin\\ffmpeg.exe"


def dynamic_death_recover_plot(data, province):
    """ generating a video to record the dynamic changes of deaths and recovers in the given province

       Parameters:
       argument1 (DataFrame): the data read from covid19.csv by pandas
       argument2 (str): The name of province


       Returns:
       None

      """
    # filter the data by province name
    info_of_province = data[data["prname"] == province]
    # get the column 'date'
    dates = info_of_province.iloc[:, 3].values
    # get the column number of deaths
    num_deaths = info_of_province.iloc[:, 6].values
    # fill in the column 'numrecover' with its previous value
    info_of_province['numrecover'] = info_of_province['numrecover'].fillna(method='ffill')
    # get the column number of recover
    num_recovers = info_of_province.iloc[:, 9].values
    length = len(dates)

    fig, ax = plt.subplots()
    ax.set_ylabel('Number of people')
    plt.title("The change of Deaths and Recovers in " + province)
    metadata = dict(title='Dynamic changes of deaths and recovers', artist='Matplotlib',
                    comment='Movie support!')
    # create a writer
    writer = FFMpegWriter(fps=2, metadata=metadata)
    # use writer to save into video
    with writer.saving(fig, "Dynamic-death-change-" + province + '.mp4', 100):
        # plotting pictures and use writer to capture it
        for i in range(0, int(length / 5) + 1):
            i += 1
            right = i * 5
            if right > length:
                right = length
            x = dates[0:right]
            y = num_deaths[0:right]
            y1 = num_recovers[0:right]
            ax.plot(x, y, '-o', markevery=[right - 1], color='black', markerfacecolor='red', label="number of deaths")
            ax.plot(x, y1, '-o', markevery=[right - 1], color='green', markerfacecolor='blue',
                    label="number of recovers")
            if i == 1:
                ax.legend(loc='upper left')
            ax.axis([0, 10, 0, num_recovers[-1] + 2])
            xticks = list(range(0, len(dates), 7))
            xlabels = [dates[i] for i in xticks]
            ax.set_xticks(xticks)
            ax.set_xticklabels(xlabels, rotation=40)
            plt.tight_layout()
            writer.grab_frame()


data = pd.read_csv("https://health-infobase.canada.ca/src/data/covidLive/covid19.csv")
province = 'Yukon'
dynamic_death_recover_plot(data, province)