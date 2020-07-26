from selectomatic import selectomatic
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


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

def loadPandasDF(file_name = 'data/Denver20192020.csv'):
    df = pd.read_csv(file_name)
    return df

def filterDFToHaveTMAX(df):
    return df[df.TMAX.notna()]

def fetchAndFilter(file_name = 'data/Denver20192020.csv'):
    return filterDFToHaveTMAX(loadPandasDF(file_name))

def selectYearAndMonthFromDataframe(df):
    years = set([ d.split('-')[0] for d in df.DATE])
    selected_year = selectomatic(list(years))
    months = set( d.split('-')[1] for d in df[df.DATE.str.contains(selected_year)].DATE)
    selected_month = selectomatic(list(months))
    return selected_year, selected_month

def sliceDataframeToYear(df, year = '2020'):
    return df[df.DATE.str.contains(year)]

def sliceDataframeToMonth(df, month = '01'):
    return df[df.DATE.str.contains('-' + month + '-')]

def sliceDataframeToYearAndMonth(df, year = '2020', month = None):
    sliced_df = sliceDataframeToYear(df, year)
    if month:
        sliced_df = sliceDataframeToMonth(sliced_df, month)
    return sliced_df

def chartDataColumn(df, column='TMAX', title=None):
    if not title:
        title = column
    ax = plt.gca()
    df.plot(kind='line', x='DATE', y=column, ax=ax, title=title)
    # plt.show()

def calculateTmaxRollingMean(df, window=3, win_type=None):
    df['rolling_mean'] = df['TMAX'].rolling(window, win_type=win_type).mean()
    return df

# print(fetchAndFilter().head(15))
df = filterDFToHaveTMAX(loadPandasDF())
print(df.head(15))
year, month = selectYearAndMonthFromDataframe(df)
sliced_df = sliceDataframeToYearAndMonth(df, year, month)
print(sliced_df)
sliced_df = calculateTmaxRollingMean(sliced_df)
# print(sliced_df.columns)

chartDataColumn(sliced_df, 'rolling_mean', 'poopy')
chartDataColumn(sliced_df, 'TMAX', 'butthole')
plt.show()
