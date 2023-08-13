# This should allow us to calculate the mean, median, mode, max, and min of the highs and lows for a given month
import pandas as pd, argparse, pprint, statistics as stats
from datetime import date
from math import floor
from calendar import monthrange
pp = pprint.PrettyPrinter(indent=4)

parser=argparse.ArgumentParser()
parser.add_argument('--input', help='File to read in, defaults to data/Denver20112022WithPrecip.csv', default='data/Denver20112022WithPrecip.csv')
parser.add_argument('--month', help='Which month to analyze, will default to the current month', default='00')
parser.add_argument('--extreme', help='high or low, high is default', default='high')
parser.add_argument('--round', help='values are rounded down to multiples of this number', default=1)


args = parser.parse_args()

def loadMultiple():
    round = int(args.round)
    if round < 1:
        return 1
    return round

def loadExtreme():
    if args.extreme not in ('high', 'low'):
        return 'high'
    return args.extreme

def loadMethods():
    return ['max', 'mean', 'median', 'mode', 'min']

def loadMonth():
    if args.month in [ '{:02d}'.format(i) for i in range(1, 13) ]:
        return args.month
    return '{:02d}'.format(date.today().month)

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

def performRounding(valuesList, multiple):
    return list(map(lambda x: multiple*(x//multiple), valuesList))

def getValuesAsList(df, highLow):
    if highLow == 'high':
        return performRounding(df['TMAX'].tolist(), loadMultiple())
    return performRounding(df['TMIN'].tolist(), loadMultiple())

def printMonthlyMetrics(metricsDict):
    print("date\tmax\tmean\tmedian\tmode\tmin")
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
    for dateVal in range(1, monthrange(2020, int(loadMonth()))[1]+1):
        dateValStr = '{:02d}'.format(dateVal)
        dateDf = sliceDataframeToMonth(df_input, '-{}-{}'.format(loadMonth(), dateValStr))
        values = getValuesAsList(dateDf, loadExtreme())
        currDate = getStatsValues(values, loadMethods())
        resultDict[dateValStr] = currDate
    return resultDict

printMonthlyMetrics(findMonthlyMetrics())