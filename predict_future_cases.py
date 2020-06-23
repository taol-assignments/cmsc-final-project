from typing import List, Dict, Tuple
from pandas import Timestamp
from utils import *
from pmdarima.arima import auto_arima
import matplotlib.pyplot as plt
from province_wise_plots import init_date_xaxis


def plot(dates: List[Timestamp], original: List[int], predict: List[int], actual: List[int]) -> None:
    """Plot the predict cases.

    Plot the predicted number of cases, actual numbers and previous numbers. And
    save the image to ./future_cases.png.

    Arguments:
        dates: The date list.
        original: The original data list before the prediction date.
        predict: Predicted data list.
        actual: Actual data list.

    Returns:
        None
    """

    init_date_xaxis()
    plt.plot(dates[:len(original)], original, label='Original', color='blue')
    plt.plot(dates[len(original):], predict, label='Predict', color='red')
    plt.plot(dates[len(original):], actual, label='Actual',  color='green')
    plt.legend()

    # Eliminate the margin on the x axis.
    plt.margins(x=0)

    plt.title('Predicted Cases')

    # Set bbox_inches to 'tight' to remove padding.
    plt.savefig('future_cases.png', bbox_inches='tight')


def main():
    """The main function."""

    data, dates, provinces = get_csv()
    num_total = data[data['prname'] == 'Canada']['numtotal'].tolist()

    plen = 20
    model = auto_arima(num_total[:-plen])
    plot(dates, num_total[:-plen], list(map(int, model.predict(plen))), num_total[-plen:])


if __name__ == '__main__':
    main()
