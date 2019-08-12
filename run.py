from random import choice
from os import listdir
from openFile import loadFile
import re
import insert
import sys
import sliceData

dailyWeather = loadFile()

slicer = sliceData.Slicer(dailyWeather)

print slicer.displayHighsFromListOfDates(slicer.getHottestDaysInYear('2000'))



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
