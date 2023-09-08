# This calculates the high and the low temperatures for each month in the requested years

import pandas as pd, argparse, pprint, statistics as stats
from datetime import date
from math import floor
pp = pprint.PrettyPrinter(indent=4)

parser=argparse.ArgumentParser()
parser.add_argument('--input', help='File to read in, defaults to Denver20112022WithPrecip', default='data/Denver20112022WithPrecip.csv')
parser.add_argument('--years', help='Which years to display, comma separated', default='2021,2022')

args = parser.parse_args()

def loadPandasDF(file_name = 'data/Denver20162020USW00023062.csv'):
    df = pd.read_csv(file_name)
    return df

def filterDFToHaveTMAX(df):
    return df[df.TMAX.notna()]

def sliceDataframeToYear(df, year = '2020'):
    return df[df.DATE.str.contains(year)]

def sliceDataframeToYearMonth(df, yearMonth):
    return df[df.DATE.str.contains(yearMonth)]

def extractYearsFromArgs():
    return [ y for y in args.years.split(',') ]

def printHighsAndLows(highsAndLowsDict):
    for year in sorted(highsAndLowsDict.keys()):
        yearDict = highsAndLowsDict[year]
        print(year)
        for month in sorted(yearDict.keys()):
            monthDict = yearDict[month]
            print("\t{}\t{}\t{}\t{}\t{}".format(month, monthDict['high'], monthDict['highDate'], monthDict['low'], monthDict['lowDate']))

def findHighsAndLows():
    df_input = filterDFToHaveTMAX(loadPandasDF(args.input))
    resultDict = {}
    for year in extractYearsFromArgs():
        currYear = {}
        for month in [ '{:02d}'.format(i) for i in range(1, 13) ]:
            currMonth = {
                'high': None,
                'highDate': None,
                'low': None,
                'lowDate': None
            }
            monthDf = sliceDataframeToYearMonth(df_input, '{}-{}'.format(year, month))
            for index, row in monthDf.iterrows():
                if currMonth['high'] is None or row['TMAX'] > currMonth['high']:
                    currMonth['high'] = row['TMAX']
                    currMonth['highDate'] = row['DATE']
                if currMonth['low'] is None or row['TMIN'] < currMonth['low']:
                    currMonth['low'] = row['TMIN']
                    currMonth['lowDate'] = row['DATE']
            currYear[month] = currMonth
        resultDict[year] = currYear
    return resultDict

printHighsAndLows(findHighsAndLows())