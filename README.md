# cmsc-final-project
The Final Project of CMSC 6950. It aims process, analyze and present current Canadian
Covid-19 data (https://health-infobase.canada.ca/src/data/covidLive/covid19.csv).
## Getting started
The following instructions will show how to use the codes.
### Prerequisites
1. Install python running environment.
2. Install the packages used in the python file.
### Plot of the total cases, tested cases and new cases over time
Just run the file 'province_wise_plots.py' under the main directory.
### Calculate doubling rate
Go to the directory 'calculate-plot-doubling-rate/calculate-doubling-rate', and type the following command to get the doubling rate for the given province:
```
> python calculate-doubling-rate.py Alberta
```
### Plot of the doubling rate
Go to the directory 'calculate-plot-doubling-rate/plot-doubling-rate', revoke the function plot_doubling_rate() in 'plot-doubling-rate.py'. For example:
```
# plot the curve for Alberta
plot_doubling_rate('../calculate-doubling-rate/covid19-Alberta.csv', 'Alberta')
```
### Create pie chart of different provinces.
Go to the directory 'reactive-graphs', revoke the function draw_pie_chart() in 'pie-chart.py'. For example:
```
draw_pie_chart(pd.read_csv("https://health-infobase.canada.ca/src/data/covidLive/covid19.csv"), 'pie.html')
```
### Create videos to visualize the changes of data over time
Go to the directory 'video-visualization/changes-of-deaths&recover', revoke the function dynamic_death_recover_plot() in 'dynamic-death&recover-plot.py'. For example:
```
data = pd.read_csv("https://health-infobase.canada.ca/src/data/covidLive/covid19.csv")
province = 'Yukon'
dynamic_death_recover_plot(data, province)
```
## Authors
* **Tao Liu**
* **Shuaishaui Li**
* **Shammy Sriharsha Ambati**
