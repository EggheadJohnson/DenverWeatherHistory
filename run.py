from random import choice
from os import listdir
from openFile import loadFile
import re
import insert
import sys
import sliceData

options = [
    'Load file',
    'Exit',
]

print "Hi and welcome to this weather thing I built"

selection = -1

dailyWeather = {}
dailyWeather = loadFile()

while selection != 'Exit':
    if dailyWeather:
        print "You have the data set " + dailyWeather['dataSet'] + " open"
        if 'Slice data' not in options: options.insert(1, 'Slice data')
    print "Please make a selection by number, letter, or full text"
    for i, option in enumerate(options):
        print "  " + str(i+1) + ": " + option
    selection = raw_input(" Selection: ")
    if selection.isdigit():
        selection = int(selection) - 1
        if selection >= len(options):
            print "Invalid selection"
        else:
            selection = options[selection]
    elif len(selection) == 1:
        selection = selection.upper()
        found = False
        for option in options:
            if option[0] == selection:
                selection = option
                found = True
                break
        if not found:
            print "Invalid selection"
    elif selection not in options:
        print "Invalid selection"

    print "Your selection was " + str(selection)

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
