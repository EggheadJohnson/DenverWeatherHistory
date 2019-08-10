import credentials
import mysql.connector
from mysql.connector import errorcode



def into_ping_result_summary(ping_results):
    creds = credentials.get()

    cnx = mysql.connector.connect(user=creds['user'], password=creds['password'],
                                  host='127.0.0.1',
                                  database=creds['database'])

    cursor = cnx.cursor()
    # prs = "INSERT INTO ping_result_summary (run_date, min, max, avg, mdev, total, loss, traceroute_dump) values ({run_date}, {min}, {max}, {avg}, {mdev}, {total}, {loss}, '{traceroute_dump}')".format(run_date=ping_results['run_date'])
    prs = ("INSERT INTO ping_result_summary "
        "(run_date, min, max, avg, mdev, total, loss, traceroute_dump) "
        "values (%(run_date)s, %(min)s, %(max)s, %(avg)s, %(mdev)s, %(total)s, %(loss)s, %(traceroute_dump)s)")

    cursor.execute(prs, ping_results)

    lastrowid = cursor.lastrowid

    cnx.commit()

    cursor.close()
    cnx.close()

    return lastrowid

def into_raw_ping_data(ping_result):
    creds = credentials.get()

    cnx = mysql.connector.connect(user=creds['user'], password=creds['password'],
                                  host='127.0.0.1',
                                  database=creds['database'])

    cursor = cnx.cursor()
    rpd = ("INSERT INTO raw_ping_data "
        "(run_date, ping_result_summary_id, icmp_seq, ping_time) "
        "values(%(run_date)s, %(ping_result_summary_id)s, %(icmp_seq)s, %(ping_time)s)")

    cursor.execute(rpd, ping_result)

    cnx.commit()

    cursor.close()
    cnx.close()
