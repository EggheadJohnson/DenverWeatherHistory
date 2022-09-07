# The goal here was to see the days that were hotter than any that followed
# Then I added the ability to see:
#  1. Days that were hotter than any that followed
#  2. Days that were hotter than any that had preceded it (hottest so far)
#  3. Days that were colder than any that followed
#  4. Days that were colder than any that had preceded it (coldest so far)
# Hottest days are for one calendar year
# Coldest days find the hottest day from the previous year and go to the hottest day in the requested year

import pandas as pd, argparse, pprint
pp = pprint.PrettyPrinter(indent=4)

parser=argparse.ArgumentParser()
parser.add_argument('--input', help='File to read in, defaults to Denver20112021USW00023062.csv', default='data/Denver20112021USW00023062.csv')
parser.add_argument('--output', help='Optional output file to dump the data into', default='')
parser.add_argument('--year', help='The year you want to analyze, defaults to 2021', default='2021')
parser.add_argument('--over_temps', help='Comma separated list of temps to calculate first/last time the temperature exceeded', default='90,100')
parser.add_argument('--under_temps', help='Comma separated list of temps to calculate last/first time the temperature fell below', default='32')
parser.add_argument('--split_date', help='The date (mm-dd) that should be used to separate the last and first low temp days', default='06-01')


args = parser.parse_args()

def loadPandasDF(file_name = 'data/Denver20112021USW00023062.csv'):
    df = pd.read_csv(file_name)
    return df

def filterDFToHaveTMAX(df):
    return df[df.TMAX.notna()]

def filterDFToHaveTMIN(df):
    return df[df.TMIN.notna()]

def sliceDataframeToYear(df, year):
    return df[df.DATE.str.contains(year)]

def buildDaysArray(df, reverse=False):
    days = []
    for row in df.itertuples():
        days.append({
            'date': row.DATE,
            'max': row.TMAX,
            'min': row.TMIN,
        })
    days = sorted(days, key=lambda x: x['date'], reverse=reverse)
    return days

def getHottestSeries(days):
    hottestSeen = None
    for day in days:
        if hottestSeen is None or day['max'] > hottestSeen:
            print(day['date'], day['max'])
            hottestSeen = day['max']

def getColdestSeries(days):
    coldestSeen = None
    for day in days:
        if coldestSeen is None or day['max'] < coldestSeen:
            print(day['date'], day['max'])
            coldestSeen = day['max']

def sliceDaysToMaxima(days):
    yearA = days[0]['date'][:4]
    yearB = days[-1]['date'][:4]
    yearAMaxIdx = 0
    yearBMaxIdx = len(days) - 1

    for i, day in enumerate(days):
        if yearA in day['date'] and day['max'] > days[yearAMaxIdx]['max']:
            yearAMaxIdx = i
        if yearB in day['date'] and day['max'] > days[yearBMaxIdx]['max']:
            yearBMaxIdx = i

    return days[yearAMaxIdx:yearBMaxIdx+1]
def run():
    df = loadPandasDF(args.input)
    year = args.year
    sliced = sliceDataframeToYear(df, year)
    days = buildDaysArray(sliced, True)
    getHottestSeries(days)
    print()
    days = buildDaysArray(sliced)
    getHottestSeries(days)
    print()
    sliced = pd.concat([sliceDataframeToYear(df, '{}'.format(int(year)-1)), sliceDataframeToYear(df, year)])
    days = buildDaysArray(sliced)
    days = sliceDaysToMaxima(days)
    getColdestSeries(days)
    print()
    days = buildDaysArray(sliced, True)
    days = sliceDaysToMaxima(days)
    getColdestSeries(days)

run()