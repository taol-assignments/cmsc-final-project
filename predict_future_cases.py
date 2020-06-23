from typing import List, Dict, Tuple
from pandas import Timestamp
from utils import *
from pmdarima.arima import auto_arima
import matplotlib.pyplot as plt
from province_wise_plots import init_date_xaxis


def plot(
        dates: List[Timestamp],
        actual: List[int],
        predict: List[int]) -> None:
    """Plot the predict cases.

    Plot the predicted number of cases and actual numbers. And
    save the image to ./future_cases.png.

    Arguments:
        dates: The date list.
        actual: Actual data list.
        predict: Predicted data list.

    Returns:
        None
    """

    init_date_xaxis()
    plt.plot(dates[:len(actual)], actual, label='Actual', color='blue')
    plt.plot(dates[len(actual):], predict, label='Predict',  color='green')
    plt.legend()

    # Eliminate the margin on the x axis.
    plt.margins(x=0)

    plt.ylim(bottom=0)

    plt.title('Predicted New Cases per Day')

    # Set bbox_inches to 'tight' to remove padding.
    plt.savefig('future_cases.png', bbox_inches='tight')


def main():
    """The main function."""

    data, dates, provinces = get_csv()

    plen = 30

    # Extend the date list.
    for i in range(plen):
        dates.append(dates[-1] + pd.Timedelta(days=1))

    num_today = data[data['prname'] == 'Canada']['numtoday'].tolist()

    model = auto_arima(
        num_today,
        trend='ct',
        seasonal=False)

    predict = list(map(int, model.predict(plen)))

    plot(dates, num_today, predict)


if __name__ == '__main__':
    main()
