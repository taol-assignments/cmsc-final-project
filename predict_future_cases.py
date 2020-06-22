from utils import *
from pmdarima.arima import auto_arima
import matplotlib.pyplot as plt
from province_wise_plots import init_date_xaxis


def plot(dates, original, predict, actual):
    init_date_xaxis()
    plt.plot(dates[:len(original)], original, color='blue')
    plt.plot(dates[len(original):], predict, color='red')
    plt.plot(dates[len(original):], actual, color='green')
    plt.show()


def main():
    data, dates, provinces = get_csv()
    num_total = data[data['prname'] == 'Canada']['numtotal'].tolist()

    plen = 20
    model = auto_arima(num_total[:-plen])
    plot(dates, num_total[:-plen], list(map(int, model.predict(plen))), num_total[-plen:])


if __name__ == '__main__':
    main()
