from typing import List, Dict, Tuple
from pandas import Timestamp
import numpy as np
import matplotlib.ticker
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from utils import *


def init_date_xaxis() -> None:
    """Initialize the x axis and set the plot image size to 12 inch."""

    # Set the unit of x axis to month.
    months = mdates.MonthLocator()
    days = mdates.DayLocator()

    plt.gca().xaxis.set_major_locator(months)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    plt.gca().xaxis.set_minor_locator(days)

    # Rotate the date ticks.
    plt.gcf().autofmt_xdate()

    # Clear previous legend.
    legend = plt.gca().get_legend()
    if legend is not None:
        legend.remove()

    plt.gcf().set_size_inches(12, 12)


def make_data_list_and_max_total(
        data: Dict[Tuple[Timestamp, str], int],
        provinces: List[str],
        dates: List[Timestamp]) -> Tuple[List[List[int]], int]:
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
    y_tick_max = 0
    y = np.zeros((len(provinces), len(dates)), dtype=int).tolist()
    for k, v in data.items():
        date, province = k
        y[provinces.index(province)][dates.index(date)] = v
        y_tick_max = max(y_tick_max, v)
    y_tick_max = (int(str(y_tick_max)[0]) + 1) * 10 ** (len(str(y_tick_max)) - 1)

    return y, y_tick_max


def remove_zeros(
        y: List[List[int]],
        dates: List[Timestamp]) -> Tuple[List[List[int]], List[Timestamp]]:
    """Remove all-zero columns in the 2D data matrix.

    Cut all-zero columns at the beginning and the end of the data matrix. And
    remove dates that correspond to a all-zero column in the date list.

    Args:
        y: The 2D data matrix.
        dates: The date list.

    Returns:
        y: Sliced 2D data matrix.
        dates: Sliced dates List."""
    y = np.array(y)
    while not np.any(y[:, 0]):
        y = y[:, 1:]
        dates = dates[1:]

    while not np.any(y[:, -1]):
        y = y[:, :-1]
        dates = dates[:-1]

    return y.tolist(), dates


def make_line_plot_over_time(
        title: str,
        data: Dict[Tuple[Timestamp, str], int],
        provinces: List[str],
        dates: List[Timestamp],
        filename: str) -> None:
    """Create a line plot.

    Make a line plot for the given data and dates and save the image to the given file name.
    The y axis is shown in log scale.

    Args:
        title: Title of the plot.
        data: The data dictionary where keys are date-province tuples.
        provinces: List of all province names.
        dates: List of all dates.
        filename: The file name to save.

    Returns:
        None
    """
    init_date_xaxis()

    y, y_tick_max = make_data_list_and_max_total(data, provinces, dates)
    y, dates = remove_zeros(y, dates)

    labels = []
    handles = []
    for i, province in enumerate(provinces):
        labels.append(PROVINCE_ABBR[province])
        handles.append(plt.plot(dates, y[i], color=COLORS[i])[0])

    # Generate y axis ticks.
    y_ticks = [1]
    while y_ticks[-1] * 10 < y_tick_max:
        y_ticks.append(y_ticks[-1] * 10)
    y_ticks.append(y_tick_max)

    plt.yscale('log')

    # Disable the scientific notation on y axis.
    plt.gca().yaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
    plt.gca().ticklabel_format(useOffset=False, style='plain', axis='y')

    # Eliminate the margin on the x axis.
    plt.margins(x=0)

    plt.ylim(bottom=1, top=y_tick_max)
    plt.gca().set_yticks(y_ticks)

    plt.legend(handles, labels)
    plt.title(title)

    # Set bbox_inches to 'tight' to remove padding.
    plt.savefig(filename, bbox_inches='tight')


def make_bar_chart_over_time(
        title: str,
        data: Dict[Tuple[Timestamp, str], int],
        provinces: List[str],
        dates: List[Timestamp],
        filename: str) -> None:
    """Create a bar chart.

    Create and a bar chart with given data and dates and save the image to the given file name.

    Args:
        title: Title of the plot.
        data: The data dictionary where keys are date-province tuples.
        provinces: List of all province names.
        dates: List of all dates.
        filename: The file name to save.

    Returns:
        None
    """
    y, _ = make_data_list_and_max_total(data, provinces, dates)
    y, dates = remove_zeros(y, dates)

    # Start from the day which total value is large than 10.
    for i in range(0, len(dates)):
        s = 0
        for j in range(0, len(provinces)):
            s += y[j][i]

        if s >= 10:
            y = [l[i:] for l in y]
            dates = dates[i:]
            break

    fig, axs = plt.subplots(2, 1, sharex='all', gridspec_kw={'height_ratios': [1, 15]})
    init_date_xaxis()

    labels = []
    handles = []
    bottoms = np.zeros(len(dates))
    for a, province, color in zip(y, provinces, COLORS):
        for i, ax in enumerate(axs):
            h = ax.bar(dates, a, label=PROVINCE_ABBR[province], color=color, bottom=bottoms)[0]
            if i == 1:
                handles.append(h)
                labels.append(PROVINCE_ABBR[province])
        bottoms += a

    # Eliminate the margin on the x axis.
    plt.xlim(dates[0], dates[-1])

    # Find out the break position and set the limits of y axis.
    sums = np.sort(bottoms)
    axs[0].set_ylim(sums[-1] - 5, sums[-1] + 5)
    axs[1].set_ylim(0, sums[-2] + 5)

    # Hide the axis between the break.
    axs[0].spines['bottom'].set_visible(False)
    axs[0].tick_params(axis='x', which='both', bottom=False)
    axs[1].spines['top'].set_visible(False)

    # Draw the break tick.
    break_len = 0.010
    left_break_x = (-break_len, break_len)
    right_break_x = (1 - break_len, 1 + break_len)
    top_break_y = (break_len, break_len)
    bottom_break_y = (1 - break_len, 1 - break_len)

    kwargs = dict(transform=axs[0].transAxes, color='black', clip_on=False)
    axs[0].plot(left_break_x, top_break_y, **kwargs)
    axs[0].plot(right_break_x, top_break_y, **kwargs)
    kwargs.update(transform=axs[1].transAxes)
    axs[1].plot(left_break_x, bottom_break_y, **kwargs)
    axs[1].plot(right_break_x, bottom_break_y, **kwargs)

    plt.legend(handles, labels, loc='upper left')
    plt.suptitle(title, y=0.90)
    plt.savefig(filename, bbox_inches='tight')


def main() -> None:
    """Main function."""

    data, dates, provinces = get_csv()
    data = data[data['prname'] != 'Canada']

    num_total = data.groupby(['date', 'prname']).sum()['numtotal'].to_dict()
    make_line_plot_over_time("Total Cases", num_total, provinces, dates, 'total_cases.png')

    num_tested = data.groupby(['date', 'prname']).sum()['numtested'].astype('int32').to_dict()
    make_line_plot_over_time("Individuals Tested", num_tested, provinces, dates, 'individuals_tested.png')

    num_today = data.groupby(['date', 'prname']).sum()['numtoday'].astype('int32').to_dict()
    make_bar_chart_over_time("New Cases Per Day", num_today, provinces, dates, 'new_cases_per_day.png')


if __name__ == '__main__':
    main()
