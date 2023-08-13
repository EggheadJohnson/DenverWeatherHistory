# This should allow us to calculate the mean, median, mode, max, and min of the highs and lows for a each month
import pandas as pd, argparse, pprint, statistics as stats
from datetime import date
from math import floor
pp = pprint.PrettyPrinter(indent=4)

parser=argparse.ArgumentParser()
parser.add_argument('--input', help='File to read in, defaults to data/Denver20112022WithPrecip.csv', default='data/Denver20112022WithPrecip.csv')
parser.add_argument('--extreme', help='high or low, high is default', default='high')


args = parser.parse_args()

def loadExtreme():
    if args.extreme not in ('high', 'low'):
        return 'high'
    return args.extreme

def loadMethods():
    return ['max', 'mean', 'median', 'mode', 'min']

def loadPandasDF(file_name = 'data/Denver20112022WithPrecip.csv'):
    df = pd.read_csv(file_name)
    return df

def filterDFToHaveExtreme(df):
    if loadExtreme() == 'high':
        return df[df.TMAX.notna()]
    return df[df.TMIN.notna()]

def sliceDataframeToYear(df, year = '2020'):
    return df[df.DATE.str.contains(year)]

def sliceDataframeToMonth(df, month):
    return df[df.DATE.str.contains(month)]

def getValuesAsList(df, highLow):
    if highLow == 'high':
        return df['TMAX'].tolist()
    return df['TMIN'].tolist()

def printMonthlyMetrics(metricsDict):
    print("month\tmax\tmean\tmedian\tmode\tmin")
    for month in sorted(metricsDict.keys()):
        monthValues = metricsDict[month]
        print(" {}\t{:.2f}\t{:.2f}\t{:.2f}\t{:.2f}\t{:.2f}".format(month, monthValues['max'], monthValues['mean'], monthValues['median'], monthValues['mode'], monthValues['min']))


def getStatsValues(values, methods):
    result = {
        'mean': stats.mean(values),
        'median': stats.median(values),
        'mode': stats.mode(values),
        'max': max(values),
        'min': min(values)
    }
    return result

def findMonthlyMetrics():
    df_input = filterDFToHaveExtreme(loadPandasDF(args.input))
    resultDict = {}
    for month in [ '{:02d}'.format(i) for i in range(1, 13) ]:
        monthDf = sliceDataframeToMonth(df_input, '-{}-'.format(month))
        values = getValuesAsList(monthDf, loadExtreme())
        currMonth = getStatsValues(values, loadMethods())
        resultDict[month] = currMonth
    return resultDict

printMonthlyMetrics(findMonthlyMetrics())