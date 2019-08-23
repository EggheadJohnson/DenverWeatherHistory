from random import choice
from os import listdir
from openFile import loadFile, selectFile
from create_tables import drop_and_rewrite_tables
from selectomatic import selectomatic
import re
import insert
import sys
import sliceData


options = [
    'Load file',
    'Reset tables - caution this deletes all data',
    'Exit',
]

print "Hi and welcome to this weather thing I built"

selection = -1
dailyWeather = {}

while selection != 'Exit':
    if dailyWeather:
        print "You have the data set " + dailyWeather['dataSet'] + " open"
        if 'Slice data' not in options: options.insert(1, 'Slice data')
        if 'Write data' not in options: options.insert(2, 'Write data')
    selection = selectomatic(options)

    if selection == 'Load file':
        dailyWeather = loadFile(selectFile())
    elif selection == 'Slice data':
        sliceData.slicePicker(dailyWeather)
    elif selection == 'Write data':
        insert.all_data(dailyWeather['dailyWeather'])
    elif selection == 'Reset tables - caution this deletes all data':
        drop_and_rewrite_tables()








#
#
#
#
# dailyWeather = loadFile()
#
# slicer = sliceData.Slicer(dailyWeather)
#
# slicer.displayHighsFromListOfDates(slicer.getHottestDaysInYearAndMonth('2018', '08', 15))
#
#



# print displayHighsFromListOfDates(getHottestDaysInYear('2015'))
# print displayHighsFromListOfDates(getHottestDaysInYearAndMonth('2016', '05'))
# print displayHighsFromListOfDates(getHottestDaysInMonthAcrossYears('03'))

# print displayHighsFromListOfDates(getColdestDaysInYear('1982'))
# print displayHighsFromListOfDates(getColdestDaysInYearAndMonth('2016', '05'))
# print displayHighsFromListOfDates(getColdestDaysInMonthAcrossYears('03'))

# totalDays = len(dailyWeather.keys())
# separatorLength = totalDays/50
# i = 0
#
# errors = []
#
# for date in dailyWeather:
#     try:
#         insert.into_daily_histories(dailyWeather[date])
#     except:
#         errors.append(sys.exc_info()[1])
#         # print 'added error'
#         # print errors
#         # sys.exit()
#     i += 1
#     if i % separatorLength == 0:
#         sys.stdout.write("\r[{0}{1}]".format("."*(i/separatorLength), " "*(50-(i/separatorLength))))
#         sys.stdout.flush()
#
# print errors
