# This should allow us to calculate the mean, median, mode, max, and min of the highs and lows for a each month
import pandas as pd, argparse, pprint, statistics as stats
from datetime import date
from math import floor
pp = pprint.PrettyPrinter(indent=4)

parser=argparse.ArgumentParser()
parser.add_argument('--input', help='File to read in, defaults to data/Denver20112022WithPrecip.csv', default='data/Denver20112022WithPrecip.csv')
parser.add_argument('--date', help='Defaults to today\'s date; must be in MM-DD format')

args = parser.parse_args()

def loadFileName():
    return args.input

def loadPandasDF(filename):
    df = pd.read_csv(filename)
    return df

def sliceDataframeToDate(df, dateString):
    return df[df.DATE.str.contains(dateString)]

def loadDateString():
    if args.date:
        return args.date
    return date.today().isoformat()[-6:]

def loadTodayInHistory():
    filename = loadFileName()
    df = loadPandasDF(filename)
    dateString = loadDateString()
    df = sliceDataframeToDate(df, dateString)[['DATE', 'TMAX', 'TMIN']]
    print(df)

loadTodayInHistory()