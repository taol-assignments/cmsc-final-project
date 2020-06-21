import matplotlib.pyplot as plt
import pandas as pd


def plot_doubling_rate(filename, province):
    data = pd.read_csv(filename)
    x_date = data.iloc[:, 3].values
    # y_num_confirmed = data.iloc[:, 2].values
    y_doubling_rate = data.iloc[:, 4].values

    fig1, ax = plt.subplots()
    ax.plot(x_date, y_doubling_rate)
    ax.set_ylabel('Doubling Rate')
    xticks = list(range(0, len(x_date), 7))
    xlabels = [x_date[x] for x in xticks]
    xticks.append(len(x_date))
    xlabels.append(x_date[-1])
    ax.set_xticks(xticks)
    ax.set_xticklabels(xlabels, rotation=40)
    plt.title("The change of doubling rate in " + province)
    plt.tight_layout()
    fig1.savefig('Doubling-rate-' + province + '.png')


plot_doubling_rate('covid19-Alberta.csv', 'Alberta')
plot_doubling_rate('covid19-Ontario.csv', 'Ontario')
plot_doubling_rate('covid19-Quebec.csv', 'Quebec')
