# The goal of this is to find the highest high minus the lowest high and then also the highest high minus the lowest low
import pandas as pd, argparse, pprint, statistics as stats
from datetime import date, timedelta
from math import floor
pp = pprint.PrettyPrinter(indent=4)

parser=argparse.ArgumentParser()
parser.add_argument('--input', help='File to read in, defaults to data/Denver20112022WithPrecip.csv', default='data/Denver20112022WithPrecip.csv')
parser.add_argument('--month', help='Defaults to today\'s date; must be in MM format')

args = parser.parse_args()

def loadFileName():
    return args.input

def loadPandasDF(filename):
    df = pd.read_csv(filename)
    return df

def sliceDataframeToDate(df, dateString):
    return df[df.DATE.str.contains(dateString)]

def findExtrema(df):
    result = {
        'highHigh': None,
        'lowHigh': None,
        'highLow': None,
        'lowLow': None
    }

    for row in df.iterrows():
        if result['highHigh'] is None or row[1]['TMAX'] > result['highHigh']:
            result['highHigh'] = row[1]['TMAX']
        if result['lowHigh'] is None or row[1]['TMAX'] < result['lowHigh']:
            result['lowHigh'] = row[1]['TMAX']
        if result['highLow'] is None or row[1]['TMIN'] > result['highLow']:
            result['highLow'] = row[1]['TMIN']
        if result['lowLow'] is None or row[1]['TMIN'] < result['lowLow']:
            result['lowLow'] = row[1]['TMIN']
    return result
        
def generateDates(month = None):
    curr = date(2020, 1, 1)
    end = date(2021, 1, 1)
    if not month is None:
        curr = date(2020, int(month), 1)
        nextMonth = curr + timedelta(31)
        end = date(nextMonth.year, nextMonth.month, 1)
    dates = []
    while curr < end:
        dates.append(curr.isoformat()[-6:])
        curr += timedelta(days=1)
    return dates

def loadExtrema():
    filename = loadFileName()
    df = loadPandasDF(filename)
    results = {}
    for dateString in generateDates(args.month):
        dateStringDF = sliceDataframeToDate(df, dateString)[['DATE', 'TMAX', 'TMIN']]
        extrema = findExtrema(dateStringDF)
        results[dateString] = {
            'highHighLowHigh': extrema['highHigh'] - extrema['lowHigh'],
            'highHighLowLow': extrema['highHigh'] - extrema['lowLow']
        }
    return results

def getLargestDifferences(extrema):
    largestHighHigh = 0
    largestHighHighDate = None

    largestHighLow = 0
    largestHighLowDate = None
    for k, v in extrema.items():
        if largestHighHigh < v['highHighLowHigh']:
            largestHighHigh = v['highHighLowHigh']
            largestHighHighDate = k
        if largestHighLow < v['highHighLowLow']:
            largestHighLow = v['highHighLowLow']
            largestHighLowDate = k
    print('The largest high high difference was {} on {}'.format(largestHighHigh, largestHighHighDate))
    print('The largest high low difference was {} on {}'.format(largestHighLow, largestHighLowDate))

def getSmallestDifferences(extrema):
    smallestHighHigh = 10000
    smallestHighHighDate = None

    smallestHighLow = 10000
    smallestHighLowDate = None
    for k, v in extrema.items():
        if smallestHighHigh > v['highHighLowHigh']:
            smallestHighHigh = v['highHighLowHigh']
            smallestHighHighDate = k
        if smallestHighLow > v['highHighLowLow']:
            smallestHighLow = v['highHighLowLow']
            smallestHighLowDate = k
    print('The smallest high high difference was {} on {}'.format(smallestHighHigh, smallestHighHighDate))
    print('The smallest high low difference was {} on {}'.format(smallestHighLow, smallestHighLowDate))

def largestHighHighDifferences(extrema, limit=10):
    return [ (k, extrema[k]) for k in sorted(extrema.keys(), key=lambda x: extrema[x]['highHighLowHigh'], reverse=True)[:10]]


extrema = loadExtrema()
# pp.pprint(extrema)
pp.pprint(largestHighHighDifferences(extrema))
getLargestDifferences(extrema)
getSmallestDifferences(extrema)