from typing import List, Dict, Tuple
from pandas import Timestamp
from utils import *
from pmdarima.arima import auto_arima
import matplotlib.pyplot as plt
from province_wise_plots import init_date_xaxis


def plot(
        dates: List[Timestamp],
        predict_len: int,
        original: List[int],
        compare: List[int],
        actual: List[int],
        predict: List[int]) -> None:
    """Plot the predict cases.

    Plot the predicted number of cases, actual numbers and previous numbers. And
    save the image to ./future_cases.png.

    Arguments:
        dates: The date list.
        predict_len: The predict time length.
        original: The original data list before the prediction date.
        predict: Predicted data list.
        actual: Actual data list.

    Returns:
        None
    """

    init_date_xaxis()
    plt.plot(dates[:len(original)], original, label='Original', color='blue')
    plt.plot(dates[len(original):len(original) + predict_len], compare, label='Predict', color='yellow')
    plt.plot(dates[len(original):len(original) + predict_len], actual, label='Actual',  color='red')
    plt.plot(dates[len(original) + predict_len:], predict, label='Future Prediction',  color='green')
    plt.legend()

    # Eliminate the margin on the x axis.
    plt.margins(x=0)

    plt.title('Predicted New Cases per Day')

    # Set bbox_inches to 'tight' to remove padding.
    plt.savefig('future_cases.png', bbox_inches='tight')


def main():
    """The main function."""

    data, dates, provinces = get_csv()

    plen = 14

    # Extend the date list.
    for i in range(plen):
        dates.append(dates[-1] + pd.Timedelta(days=1))

    num_total = data[data['prname'] == 'Canada']['numtoday'].tolist()

    model = auto_arima(
        num_total[:-plen],
        trend='ct',
        seasonal=False)
    compare = list(map(int, model.predict(plen)))

    model = auto_arima(
        num_total,
        P=15,
        trend='ct',
        seasonal=False)

    predict = list(map(int, model.predict(plen)))

    plot(
        dates,
        plen,
        num_total[:-plen],
        compare,
        num_total[-plen:],
        predict)


if __name__ == '__main__':
    main()
