from selectomatic import selectomatic
import numpy as np
import matplotlib.pyplot as plt


def displayChart(weatherData):

    selection = -1

    stations = weatherData['dailyWeather'].keys()
    meta = weatherData['meta']
    stations.append('Exit')
    selection = selectomatic(stations, weatherData['summaries'])
    if selection != 'Exit':
        dataSet = weatherData['dailyWeather'][selection]
        # slicer = Slicer(dataSet)

    extrema = ['Highs', 'Lows', 'Exit']
    periods = ['Month', 'Year', 'Month and Year', 'Forever', 'Exit']
