import matplotlib.pyplot as plt
import pandas as pd


def plot_doubling_rate(file_path, province):
    """ plot the doubling rates for the input province and save it into a file

      Parameters:
      argument1 (str): The file path of the saved data for doubling rate
      argument2 (str): the name of province

      Returns:
      None

     """
    # read the saved data for doubling rate
    data = pd.read_csv(file_path)
    # get the values of 'date' column
    x_date = data.iloc[:, 3].values
    # get the values of 'doubling rate' column
    y_doubling_rate = data.iloc[:, 4].values

    fig1, ax = plt.subplots()
    ax.plot(x_date, y_doubling_rate)
    ax.set_ylabel('Doubling Rate')
    # prepare data for horizontal-axis
    xticks = list(range(0, len(x_date), 7))
    xlabels = [x_date[x] for x in xticks]
    xticks.append(len(x_date))
    xlabels.append(x_date[-1])
    # set horizontal ticks and labels
    ax.set_xticks(xticks)
    ax.set_xticklabels(xlabels, rotation=40)
    plt.title("The change of doubling rate in " + province)
    plt.tight_layout()
    # save the plotted curve into images
    fig1.savefig('Doubling-rate-' + province + '.png')


# plot the curve for Alberta
plot_doubling_rate('../calculate-doubling-rate/covid19-Alberta.csv', 'Alberta')
# plot the curve for Ontario
plot_doubling_rate('../calculate-doubling-rate/covid19-Ontario.csv', 'Ontario')
# plot the curve for Quebec
plot_doubling_rate('../calculate-doubling-rate/covid19-Quebec.csv', 'Quebec')
# plot the curve for Newfoundland
plot_doubling_rate('../calculate-doubling-rate/covid19-Newfoundland and Labrador.csv', 'Newfoundland and Labrador')