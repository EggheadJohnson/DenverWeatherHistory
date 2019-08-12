import credentials
import mysql.connector
from mysql.connector import errorcode

BREAKING_MISSES = ['TMAX', 'TMIN']
OVERRIDE_MISSES = ['SNOW', 'SNWD', 'PRCP']

def into_daily_histories(daily_history):
    creds = credentials.get()

    cnx = mysql.connector.connect(user=creds['user'], password=creds['password'],
                                  host='127.0.0.1',
                                  database=creds['database'])


    for k in BREAKING_MISSES:
        if daily_history[k] == '':
            return

    for k in OVERRIDE_MISSES:
        if daily_history[k] == '':
            daily_history[k] = 0.0

    cursor = cnx.cursor()
    # prs = "INSERT INTO ping_result_summary (run_date, min, max, avg, mdev, total, loss, traceroute_dump) values ({run_date}, {min}, {max}, {avg}, {mdev}, {total}, {loss}, '{traceroute_dump}')".format(run_date=ping_results['run_date'])
    prs = ("INSERT INTO daily_histories "
        "(zipcode,STATION,NAME,DATE,DAPR,MDPR,PRCP,SNOW,SNWD,TMAX,TMIN,TOBS,WESD,WESF,year,month,day) "
        "values (%(zipcode)s, %(STATION)s, %(NAME)s, %(DATE)s, %(DAPR)s, %(MDPR)s, %(PRCP)s, %(SNOW)s, %(SNWD)s, %(TMAX)s, %(TMIN)s, "
        " %(TOBS)s, %(WESD)s, %(WESF)s, %(year)s, %(month)s, %(day)s)")

    # print prs
    cursor.execute(prs, daily_history)

    lastrowid = cursor.lastrowid

    cnx.commit()

    cursor.close()
    cnx.close()

    return lastrowid
