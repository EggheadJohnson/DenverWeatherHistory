import pandas as pd, argparse, pprint, statistics as stats
from datetime import date
from math import floor
pp = pprint.PrettyPrinter(indent=4)

parser=argparse.ArgumentParser()
parser.add_argument('--input', help='File to read in, defaults to data/Denver20112022WithPrecip.csv', default='data/Denver20112022WithPrecip.csv')

args = parser.parse_args()

def loadPandasDF(file_name = 'data/Denver20162020USW00023062.csv'):
    df = pd.read_csv(file_name)
    return df

def filterDFToHaveTMAX(df):
    return df[df.TMAX.notna()]

def distinctYearsFromDataframe(df):
    return set([ d.split('-')[0] for d in df.DATE])

def sliceDataframeToYear(df, year = '2020'):
    return df[df.DATE.str.contains(year)]

def printHighsAndLows(highsAndLowsDict):
    for year in sorted(highsAndLowsDict.keys()):
        yearDict = highsAndLowsDict[year]
        print(" {}\t{}\t{}\t{}\t{}\t{}\t{}".format(year, yearDict['high'], yearDict['highDate'], yearDict['highCount'], yearDict['low'], yearDict['lowDate'], yearDict['lowCount']))

def extractHighDate(highsAndLowsDict):
    highDates = []
    for year in highsAndLowsDict:
        yearDict = highsAndLowsDict[year]
        highDate = date.fromisoformat(yearDict['highDate'])
        dateCount = highDate.toordinal() - date(highDate.year - 1, 12, 31).toordinal()
        highDates.append(dateCount)
    # print("Mean: {} Median: {} Mode: {}".format(date.fromordinal(floor(stats.mean(highDates))), date.fromordinal(floor(stats.median(highDates))), date.fromordinal(floor(stats.mode(highDates)))))
    mean = date.fromordinal(floor(stats.mean(highDates)))
    median = date.fromordinal(floor(stats.median(highDates)))
    mode = date.fromordinal(floor(stats.mode(highDates)))
    print("Mean: {0:%B} {0:%d}".format(mean))
    print("Median: {0:%B} {0:%d}".format(median))
    print("Mode: {0:%B} {0:%d}".format(mode))


def findHighsAndLows():
    df_input = filterDFToHaveTMAX(loadPandasDF(args.input))
    years = sorted(distinctYearsFromDataframe(df_input))
    resultDict = {}
    for year in years:
        currYearDf = sliceDataframeToYear(df_input, year)
        currYearDataDict = {
            'high': None,
            'highDate': None,
            'highCount': 0,
            'low': None,
            'lowDate': None,
            'lowCount': 0
        }
        for index, row in currYearDf.iterrows():
            if currYearDataDict['high'] is None or row['TMAX'] > currYearDataDict['high']:
                currYearDataDict['high'] = row['TMAX']
                currYearDataDict['highDate'] = row['DATE']
                currYearDataDict['highCount'] = 0
            if currYearDataDict['high'] == row['TMAX']:
                currYearDataDict['highCount'] += 1
            if currYearDataDict['low'] is None or row['TMIN'] < currYearDataDict['low']:
                currYearDataDict['low'] = row['TMIN']
                currYearDataDict['lowDate'] = row['DATE']
                currYearDataDict['lowCount'] = 0
            if currYearDataDict['low'] == row['TMIN']:
                currYearDataDict['lowCount'] += 1
        resultDict[year] = currYearDataDict
    return resultDict

printHighsAndLows(findHighsAndLows())

extractHighDate(findHighsAndLows())