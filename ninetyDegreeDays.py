import pandas as pd, argparse

parser=argparse.ArgumentParser()
parser.add_argument('--input', help='File to read in, defaults to denver20192020', default='data/Denver20162020USW00023062.csv')
parser.add_argument('--output', help='Optional output file to dump the data into', default='')
parser.add_argument('--over_temps', help='Comma separated list of temps to calculate first/last time the temperature exceeded', default='90,100')
parser.add_argument('--under_temps', help='Comma separated list of temps to calculate last/first time the temperature fell below', default='32')
parser.add_argument('--split_date', help='The date (mm-dd) that should be used to separate the last and first low temp days', default='06-01')


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

def parseExtremeList(extremes_list, reverse=False):
    return sorted(map(int, extremes_list.split(',')), reverse=reverse)

def parseExtrema(args):
    overs = parseExtremeList(args.over_temps)
    unders = parseExtremeList(args.under_temps, True)
    return {
        'overs': overs,
        'unders': unders
    }

def buildDataFrame(extrema):
    columns = ['year']

    for temp in extrema['overs']:
        columns.extend([
            'first_over_{}'.format(temp),
            'last_over_{}'.format(temp),
            'total_over_{}'.format(temp)
        ])
    for temp in extrema['unders']:
        columns.extend([
            'last_under_{}'.format(temp),
            'first_under_{}'.format(temp),
            'total_under_{}'.format(temp)
        ])
    return pd.DataFrame([], columns=columns)

def buildDataDictForYearFromDF(year, df):
    data_dict = {}
    for col in df.columns:
        if col[:5] == 'total':
            data_dict[col] = 0
        else:
            data_dict[col] = None

    data_dict['year'] = year
    return data_dict

# blank_df = buildDataFrame(parseExtrema(args))
# print(buildDataDictForYearFromDF(2020, blank_df))
def updateYearDataDict(row, input_extrema, data_dict):
    june_first = data_dict['year'] + '-{}'.format(args.split_date)
    for over in input_extrema['overs']:
        if row['TMAX'] >= over:
            if not data_dict['first_over_{}'.format(over)]:
                data_dict['first_over_{}'.format(over)] = row['DATE']
            data_dict['last_over_{}'.format(over)] = row['DATE']
            data_dict['total_over_{}'.format(over)] += 1
    for under in input_extrema['unders']:
        if row['TMIN'] <= under:
            if row['DATE'] < june_first:
                data_dict['last_under_{}'.format(under)] = row['DATE']
            if row['DATE'] >= june_first and data_dict['first_under_{}'.format(under)] is None:
                data_dict['first_under_{}'.format(under)] = row['DATE']
            data_dict['total_under_{}'.format(under)] += 1
    return data_dict

def findExtremeTemps():
    input_extrema = parseExtrema(args)
    df_output = buildDataFrame(input_extrema)
    df_input = filterDFToHaveTMAX(loadPandasDF(args.input))
    years = sorted(distinctYearsFromDataframe(df_input))
    for year in years:
        curr_year_df = sliceDataframeToYear(df_input, year)
        curr_year_data_dict = buildDataDictForYearFromDF(year, df_output)
        for index, row in curr_year_df.iterrows():
            curr_year_data_dict = updateYearDataDict(row, input_extrema, curr_year_data_dict)
        df_output = df_output.append(curr_year_data_dict, ignore_index=True)
    return df_output


df_output = findExtremeTemps()

print(df_output)

if args.output:
    df_output.to_csv(args.output, index=False)
