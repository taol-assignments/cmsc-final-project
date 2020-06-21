import numpy as np
import matplotlib.ticker
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from utils import *


def init_data_xaxis():
    months = mdates.MonthLocator()
    days = mdates.DayLocator()

    plt.gca().xaxis.set_major_locator(months)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    plt.gca().xaxis.set_minor_locator(days)

    plt.gcf().autofmt_xdate()
    plt.gcf().set_size_inches(12, 12)


def make_data_list_and_max_total(data, provinces, dates):
    max_total = 0
    y = np.zeros((len(provinces), len(dates)), dtype=int).tolist()
    for k, v in data.items():
        date, province = k
        y[provinces.index(province)][dates.index(date)] = v
        max_total = max(max_total, v)
    max_total = (int(str(max_total)[0]) + 1) * 10 ** (len(str(max_total)) - 1)

    return y, max_total


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
    plt.title(title)
    plt.savefig(filename, bbox_inches='tight')


def make_bar_chart_over_time(title, data, provinces, dates, filename):
    y, _ = make_data_list_and_max_total(data, provinces, dates)

    for i in range(0, len(dates)):
        s = 0
        for j in range(0, len(provinces)):
            s += y[j][i]

        if s >= 10:
            y = [l[i:] for l in y]
            dates = dates[i:]
            break

    fig, axs = plt.subplots(2, 1, sharex=True, gridspec_kw={'height_ratios': [1, 15]})

    bottoms = np.zeros(len(dates))
    for a, province, color in zip(y, provinces, COLORS):
        for ax in axs:
            ax.bar(dates, a, label=PROVINCE_ABBR[province], color=color, bottom=bottoms)
        bottoms += a

    sums = sorted(bottoms.tolist())

    axs[0].set_ylim(sums[-1] - 5, sums[-1] + 5)
    axs[1].set_ylim(0, sums[-2] + 5)

    axs[0].spines['bottom'].set_visible(False)
    axs[0].tick_params(axis='x', which='both', bottom=False)
    axs[1].spines['top'].set_visible(False)

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

    init_data_xaxis()
    plt.legend(loc='upper left')
    plt.suptitle(title, y=0.90)
    plt.savefig(filename, bbox_inches='tight')


def main():
    data, dates, provinces = get_csv()

    data = data[(data['prname'] != 'Canada') & (data["prname"] != "Repatriated travellers")].fillna(0)

    num_total = data.groupby(['date', 'prname']).sum()['numtotal'].to_dict()
    make_line_plot_over_time("Total Cases", num_total, provinces, dates, 'total_cases.png')

    num_tested = data.groupby(['date', 'prname']).sum()['numtested'].astype('int32').to_dict()
    make_line_plot_over_time("Individuals Tested", num_tested, provinces, dates, 'individuals_tested.png')

    num_today = data.groupby(['date', 'prname']).sum()['numtoday'].astype('int32').to_dict()
    make_bar_chart_over_time("New Cases Per Day", num_today, provinces, dates, 'new_cases_per_day.png')


if __name__ == '__main__':
    main()
