import credentials
import mysql.connector
from mysql.connector import errorcode

creds = credentials.get()

TABLES = {}
TABLES['daily_histories'] = (
    "DROP TABLE IF EXISTS `daily_histories`;"
    "CREATE TABLE `daily_histories` ("
    "  `date_id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `date` varchar(15) NOT NULL,"
    "  `year` int,"
    "  `month` int,"
    "  `day` int,"
    "  `zipcode` int NOT NULL,"
    "  `station` varchar(15),"
    "  `name` varchar(30),"
    "  `dapr` varchar(15),"
    "  `mdpr` varchar(15),"
    "  `prcp` decimal(8,4),"
    "  `snow` decimal(8,4),"
    "  `snwd` decimal(8,4),"
    "  `tavg` decimal(8,4),"
    "  `tmin` int,"
    "  `tmax` int,"
    "  `tobs` varchar(15),"
    "  `wesd` varchar(15),"
    "  `wesf` varchar(15),"
    "  `wt10` varchar(15),"
    "  `wt03` varchar(15),"
    "  `wt04` varchar(15),"
    "  `wt05` varchar(15),"
    "  `wt06` varchar(15),"
    "  `wt11` varchar(15),"
    "  PRIMARY KEY (`date_id`, `date`, `zipcode`)"
    ") ENGINE=InnoDB")

# "STATION","NAME","DATE","DAPR","MDPR","PRCP","SNOW","SNWD","TAVG","TMAX","TMIN","TOBS","WESD","WESF","WT01","WT03","WT04","WT05","WT06","WT11"
cnx = mysql.connector.connect(user=creds['user'], password=creds['password'],
                              host='127.0.0.1',
                              database=creds['database'])

cursor = cnx.cursor()

for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name))
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)

cursor.close()
cnx.close()
