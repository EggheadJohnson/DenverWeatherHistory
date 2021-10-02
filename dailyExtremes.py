import pandas as pd, argparse
from datetime import date, timedelta



parser=argparse.ArgumentParser()
parser.add_argument('--input', help='The file to open as a source', default='data/Denver20162020USW00023062.csv')
parser.add_argument('--output', help='The file to write to', default='')
parser.add_argument('--date', help='The file to write to', default='')

args = parser.parse_args()

input_date = args.date
if not input_date:
    input_date = date.today().strftime("%m-%d")
    print("No date supplied, using {}".format(input_date))

input_date = '-' + input_date
def loadPandasDF(file_name = 'data/Denver20192020.csv'):
    df = pd.read_csv(file_name)
    return df

def filterDFToHaveTMAX(df):
    return df[df.TMAX.notna()]

def filterDFToHaveTMIN(df):
    return df[df.TMIN.notna()]

def distinctYearsFromDataframe(df):
    return set([ d.split('-')[0] for d in df.DATE])

def sliceDataframeToYear(df, year = '2020'):
    return df[df.DATE.str.contains(year)]

def extremesForDate(input_date, df):
    filtered_df = df[df['DATE'].str.contains(input_date)]



    ath = None
    atl = None
    ath_year = None
    atl_year = None
    lowest_high = None
    highest_low = None
    lowest_high_year = None
    highest_low_year = None

    for index, row in filtered_df.iterrows():
        if ath is None or row['TMAX'] >= ath:
            ath = row['TMAX']
            ath_year = row['DATE']
        if atl is None or row['TMIN'] < atl:
            atl = row['TMIN']
            atl_year = row['DATE']
        if highest_low is None or row['TMIN'] >= highest_low:
            highest_low = row['TMIN']
            highest_low_year = row['DATE']
        if lowest_high is None or row['TMAX'] < lowest_high:
            lowest_high = row['TMAX']
            lowest_high_year = row['DATE']
    return ath, atl, lowest_high, highest_low, ath_year, atl_year, lowest_high_year, highest_low_year

def printSingleDateExtremes(input_date, df):
    ath, atl, lowest_high, highest_low, ath_year, atl_year, lowest_high_year, highest_low_year = extremesForDate(input_date, df)
    print('All time high: {}'.format(ath))
    print(' Occurred on: {}'.format(ath_year))
    print('Lowest high: {}'.format(lowest_high))
    print(' Occurred on: {}'.format(lowest_high_year))
    print('Highest low: {}'.format(highest_low))
    print(' Occurred on: {}'.format(highest_low_year))
    print('All time low: {}'.format(atl))
    print(' Occurred on: {}'.format(atl_year))

def buildExtremesForWholeYear(df):
    date_to_check = date(2020, 1, 1)
    extremes_df = pd.DataFrame([], columns=[
        'date',
        'all time high',
        'all time high year',
        'lowest high',
        'lowest high year',
        'highest low',
        'highest low year',
        'all time low',
        'all time low year'
    ])
    while date_to_check < date(2021, 1, 1):
        ath, atl, lowest_high, highest_low, ath_year, atl_year, lowest_high_year, highest_low_year = extremesForDate(date_to_check.strftime("-%m-%d"), df)

        extremes_df = extremes_df.append({
            'date': date_to_check.strftime("%m-%d"),
            'all time high': ath,
            'all time high year': ath_year[:4],
            'lowest high': lowest_high,
            'lowest high year': lowest_high_year[:4],
            'highest low': highest_low,
            'highest low year': highest_low_year[:4],
            'all time low': atl,
            'all time low year': atl_year[:4]
        }, ignore_index=True)
        date_to_check += timedelta(days=1)
    return extremes_df

df = loadPandasDF(args.input)
df = filterDFToHaveTMAX(df)
df = filterDFToHaveTMIN(df)
# printSingleDateExtremes(input_date, df)

extremes_df = buildExtremesForWholeYear(df)
pd.set_option('display.max_rows', None)
print(extremes_df)
pd.set_option('display.max_rows', 10)

if args.output:
    extremes_df.to_csv(args.output, index=False)
