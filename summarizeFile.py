import pandas as pd, argparse, pprint
pp = pprint.PrettyPrinter(indent=4)

parser=argparse.ArgumentParser()
parser.add_argument('--input', help='The shorter of the two rolling averages', default='data/Denver20162020USW00023062.csv')

args = parser.parse_args()

def loadPandasDF(file_name = 'data/Denver20162020USW00023062.csv'):
    df = pd.read_csv(file_name)
    return df

df = loadPandasDF(args.input)

station_summary = {}

for index, row in df.iterrows():
    station = row['STATION']
    if station not in station_summary:
        station_summary[station] = {
            'earliest_date': None,
            'latest_date': None,
            'count': 0,
            'hadTmax': 0
        }
    if not station_summary[station]['earliest_date'] or row['DATE'] < station_summary[station]['earliest_date']:
        station_summary[station]['earliest_date'] = row['DATE']
    if not station_summary[station]['latest_date'] or row['DATE'] > station_summary[station]['latest_date']:
        station_summary[station]['latest_date'] = row['DATE']
    station_summary[station]['count'] += 1
    if not pd.isnull(row['TMAX']):
        station_summary[station]['hadTmax'] += 1
    # print(row['TMAX'])

pp.pprint(station_summary)
