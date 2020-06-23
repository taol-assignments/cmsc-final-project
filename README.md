# cmsc-final-project
This is the source code of the Final Project of CMSC 6950. It aims to process, analyze,
 and present current Canadian Covid-19 data (https://health-infobase.canada.ca/src/data/covidLive/covid19.csv).
## Getting started
The following instructions will show how to use the codes.
### Prerequisites
1. Change the current working directory to the source code directory:
```shell
$ cd cmsc-final-project
```
2. Initialize the virtual environment and install the required packages:
```shell
$ python -m venv venv
$ . ./venv/bin/activate
(venv) $ pip install -r requirements.txt
```
### Plot the total cases, tested cases and new cases over time
Run `province_wise_plots.py` in the main directory:
```shell
(venv) $ python province_wise_plots.py
```
### Calculate the doubling rate
Go to the directory `calculate-plot-doubling-rate/calculate-doubling-rate`, and type the
 following command to get the doubling rate for the given province:
```shell
(venv) $ python calculate-doubling-rate.py Alberta
```
### Plot the doubling rate
Go to the directory `calculate-plot-doubling-rate/plot-doubling-rate`, call the function
 `plot_doubling_rate()` in `plot-doubling-rate.py`:
```python
# plot the curve for Alberta
plot_doubling_rate('../calculate-doubling-rate/covid19-Alberta.csv', 'Alberta')
```
### Create pie chart of different provinces.
Go to the directory `reactive-graphs`, call the function `draw_pie_chart()` in `pie-chart.py`:
```python
draw_pie_chart(pd.read_csv("https://health-infobase.canada.ca/src/data/covidLive/covid19.csv"), 'pie.html')
```
### Create videos to visualize the changes of data over time
Go to the directory `video-visualization/changes-of-deaths&recover`, call the function dynamic_death_recover_plot() in `dynamic-death&recover-plot.py`:
```python
data = pd.read_csv("https://health-infobase.canada.ca/src/data/covidLive/covid19.csv")
province = 'Yukon'
dynamic_death_recover_plot(data, province)
```
## Authors
* **Tao Liu**
* **Shuaishaui Li**
* **Shammy Sriharsha Ambati**
