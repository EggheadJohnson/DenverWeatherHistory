import pandas as pd, argparse, pprint, statistics as stats
from datetime import date
from math import floor
pp = pprint.PrettyPrinter(indent=4)

parser=argparse.ArgumentParser()
parser.add_argument('--input', help='File to read in, defaults to data/Denver20112022WithPrecip.csv', default='data/Denver20112022WithPrecip.csv')

args = parser.parse_args()

def loadPandasDF(file_name = 'data/Denver20112022WithPrecip.csv'):
    df = pd.read_csv(file_name)
    return df

def filterDFToHaveTMAX(df):
    return df[df.TMAX.notna()]

def sliceDataframeToYear(df, year = '2020'):
    return df[df.DATE.str.contains(year)]

def sliceDataframeToMonth(df, month):
    return df[df.DATE.str.contains(month)]

def extractYearsFromArgs():
    return [ y for y in args.years.split(',') ]

def printHighsAndLows(highsAndLowsDict):
    
    for month in sorted(highsAndLowsDict.keys()):
        monthDict = highsAndLowsDict[month]
        print("\t{}\t{}\t{}\t{}\t{}".format(month, monthDict['high'], monthDict['highDate'], monthDict['low'], monthDict['lowDate']))

def findHighsAndLows():
    df_input = filterDFToHaveTMAX(loadPandasDF(args.input))
    resultDict = {}
    for month in [ '{:02d}'.format(i) for i in range(1, 13) ]:
        currMonth = {
            'high': None,
            'highDate': None,
            'low': None,
            'lowDate': None
        }
        monthDf = sliceDataframeToMonth(df_input, '-{}-'.format(month))
        for index, row in monthDf.iterrows():
            if currMonth['high'] is None or row['TMAX'] > currMonth['high']:
                currMonth['high'] = row['TMAX']
                currMonth['highDate'] = row['DATE']
            if currMonth['low'] is None or row['TMIN'] < currMonth['low']:
                currMonth['low'] = row['TMIN']
                currMonth['lowDate'] = row['DATE']
        resultDict[month] = currMonth
    return resultDict

printHighsAndLows(findHighsAndLows())