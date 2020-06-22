from math import pi
import numpy as np
import pandas as pd
from bokeh.io import output_file, show
from bokeh.palettes import Category20c
from bokeh.plotting import figure
from bokeh.transform import cumsum


def draw_pie_chart(data, file_name):
    """draw a pie chart with the input data

    Parameters:
    argument1 (DataFrame): the data read from covid19.csv
    argument2 (str): the file name to store pie chart

    Returns:
    None

   """
    # get the most recent date
    today = data['date'].values[-1]
    # filter the data by the most recent date
    info_of_today = data[data["date"] == today]
    # sort the filtered data according to confirmed number
    info_of_today = info_of_today.sort_values(by=['numconf'], ascending=False)
    # reset the index for the filtered and sorted data
    info_of_today.index = np.arange(0, len(info_of_today))
    # remove the row of Canada
    info_of_today = info_of_today[info_of_today['prname'] != 'Canada']

    # save pie chart into a file
    output_file(file_name)

    # add two more columns for data
    info_of_today['angle'] = info_of_today['numconf'] / info_of_today['numconf'].sum() * 2 * pi
    info_of_today['color'] = Category20c[len(info_of_today)]

    # set parameters for the figure
    p = figure(plot_height=400, title="Pie Chart of Confirmed numbers in Different provinces", toolbar_location=None,
               tools="hover", tooltips="@prname: @numconf", x_range=(-0.5, 1.0))
    p.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend_field='prname', source=info_of_today)

    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None

    show(p)


data = pd.read_csv("https://health-infobase.canada.ca/src/data/covidLive/covid19.csv")
draw_pie_chart(data, 'pie.html')
