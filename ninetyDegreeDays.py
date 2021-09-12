import pandas as pd, argparse

parser=argparse.ArgumentParser()
parser.add_argument('--input', help='The shorter of the two rolling averages', default='data/Denver20192020.csv')
parser.add_argument('--output', help='The shorter of the two rolling averages', default='')

args = parser.parse_args()

def loadPandasDF(file_name = 'data/Denver20192020.csv'):
    df = pd.read_csv(file_name)
    return df

def filterDFToHaveTMAX(df):
    return df[df.TMAX.notna()]

def distinctYearsFromDataframe(df):
    return set([ d.split('-')[0] for d in df.DATE])

def sliceDataframeToYear(df, year = '2020'):
    return df[df.DATE.str.contains(year)]

# df = filterDFToHaveTMAX(loadPandasDF('data/Denver19402020.csv'))
df = filterDFToHaveTMAX(loadPandasDF(args.input))
print(df.head(15))
years = sorted(distinctYearsFromDataframe(df))
print(years)
year_summary_df = pd.DataFrame([], columns=['year', 'first 90 deg day', 'last 90 deg day', 'total 90 deg days', 'first 100 deg day', 'last 100 deg day', 'total 100 deg days', 'last freeze', 'first freeze', 'days below freezing'])
for year in years:
    # print(sliceDataframeToYear(df,year).head(5))
    curr_year_df = sliceDataframeToYear(df,year)
    first_90_plus = None
    last_90_plus = None
    total_90_plus = 0
    first_100_plus = None
    last_100_plus = None
    total_100_plus = 0
    last_freeze = None
    first_freeze = None
    total_freezes = 0
    june_first = year + '-06-01'
    for index, row in curr_year_df.iterrows():
        # print(row)
        if row['TMAX'] >= 90:
            # print(row['DATE'], row['TMAX'])
            if not first_90_plus:
                first_90_plus = row['DATE']
            last_90_plus = row['DATE']
            total_90_plus += 1
        if row['TMAX'] >= 100:
            # print(row['DATE'], row['TMAX'])
            if not first_100_plus:
                first_100_plus = row['DATE']
            last_100_plus = row['DATE']
            total_100_plus += 1
        if row['TMIN'] <= 32:
            if row['DATE'] < june_first:
                last_freeze = row['DATE']
            if row['DATE'] >= june_first and not first_freeze:
                first_freeze = row['DATE']
            total_freezes += 1
    year_summary_df = year_summary_df.append({
        'year': year,
        'first 90 deg day': first_90_plus,
        'last 90 deg day': last_90_plus,
        'total 90 deg days': total_90_plus,
        'first 100 deg day': first_100_plus,
        'last 100 deg day': last_100_plus,
        'total 100 deg days': total_100_plus,
        'last freeze': last_freeze,
        'first freeze': first_freeze,
        'days below freezing': total_freezes
    }, ignore_index=True)
pd.set_option('display.max_rows', None)
print(year_summary_df)
pd.set_option('display.max_rows', 10)

if args.output:
    year_summary_df.to_csv(args.output, index=False)
