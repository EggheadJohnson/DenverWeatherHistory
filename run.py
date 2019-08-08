from random import choice
import re

def stripQuotes(string):
    return string.strip('"')

def removeQuotesFromLine(line):
    return map(stripQuotes, line)

def splitLine(line):
    result = []
    quoteOn = False
    curr = ''
    prevC = ''
    for c in line:
        if c == '"' and not quoteOn:
            quoteOn = True
        elif c == ',' and prevC == ',' and not quoteOn:
            result.append('')
        elif c == '"' and quoteOn:
            result.append(curr)
            curr = ''
            quoteOn = False
        elif quoteOn:
            curr += c
        prevC = c
    return result


file = open('1832465.csv', 'r')

keys = splitLine(file.readline().strip())
# keys = re.split('\,\S', keys)

# keys = removeQuotesFromLine(keys)

# print keys
# print len(keys)

dailyWeather = {}

for line in file:
    # line = removeQuotesFromLine(re.split('\,\S', line.strip()))
    line = removeQuotesFromLine(splitLine(line.strip()))
    # print line
    # print len(line)
    today = {}
    for i in range(len(line)):

        today[keys[i]] = line[i]
    # print today
    date = today['DATE']

    for key in today:
        if date not in dailyWeather:
            dailyWeather[date] = {}
        if key not in dailyWeather[date] or dailyWeather[date][key] == '':
            dailyWeather[date][key] = today[key]
    # if date == '2019-03-11':
    #     print today, line, today['TMAX'], dailyWeather[date]['TMAX']
#
# for x in range(10):
#     date = choice(dailyWeather.keys())
#     day = dailyWeather[date]
#     print "date: " + day['DATE']
#     print "  TMAX: " + day['TMAX']
#     print "  TAVG: " + day['TAVG']
#     print "  TMIN: " + day['TMIN']

# hottestDay = '2019-01-01'
# for date in dailyWeather:
#     print date, hottestDay, dailyWeather[date]['TMAX'], dailyWeather[hottestDay]['TMAX']
#     if 'TMAX' in dailyWeather[date] and dailyWeather[date]['TMAX'] > dailyWeather[hottestDay]['TMAX']:
#         hottestDay = date
#
# print "date: " + hottestDay
# print "  TMAX: " + dailyWeather[hottestDay]['TMAX']
# print "  TAVG: " + dailyWeather[hottestDay]['TAVG']
# print "  TMIN: " + dailyWeather[hottestDay]['TMIN']

# for date in dailyWeather:
#     if dailyWeather[date]['SNOW'] != '' and dailyWeather[date]['SNOW'] != '0.0':
#         print date
#         for key in dailyWeather[date]:
#             print "  " + key + ": " + dailyWeather[date][key]

def returnTMAXForSorting(k):
    return dailyWeather[k]['TMAX']

def getExtremeDaysInList(listOfDates, hottest = True, count = 5):
    return sorted(listOfDates, reverse = hottest, key = returnTMAXForSorting)[:count]
#
# for date in sorted(dailyWeather.keys(), key = returnTMAXForSorting, reverse = True)[:15]:
#     print date + ": " + dailyWeather[date]['TMAX'] +"   " + dailyWeather[date]['DATE']
def getDatesFromKey(key):
    return filter(lambda x: key in x, dailyWeather.keys())

def getHottestDaysInYear(year, count = 5):
    listOfDates = getDatesFromKey(year)
    return getExtremeDaysInList(listOfDates, True, count)

def getHottestDaysInYearAndMonth(year, month, count = 5):
    dateString = year + '-' + month
    listOfDates = getDatesFromKey(dateString)
    return getExtremeDaysInList(listOfDates, True, count)

def getHottestDaysInMonthAcrossYears(month, count = 5):
    dateString = '-' + month + '-'
    listOfDates = getDatesFromKey(dateString)
    return getExtremeDaysInList(listOfDates, True, count)

def getColdestDaysInYear(year, count = 5):
    listOfDates = getDatesFromKey(year)
    return getExtremeDaysInList(listOfDates, False, count)

def getColdestDaysInYearAndMonth(year, month, count = 5):
    dateString = year + '-' + month
    listOfDates = getDatesFromKey(dateString)
    return getExtremeDaysInList(listOfDates, False, count)

def getColdestDaysInMonthAcrossYears(month, count = 5):
    dateString = '-' + month + '-'
    listOfDates = getDatesFromKey(dateString)
    return getExtremeDaysInList(listOfDates, False, count)

def displayHighsFromListOfDates(listOfDates):
    for date in listOfDates:
        print date + ': ' + dailyWeather[date]['TMAX']

# print displayHighsFromListOfDates(getHottestDaysInYear('2015'))
# print displayHighsFromListOfDates(getHottestDaysInYearAndMonth('2016', '05'))
# print displayHighsFromListOfDates(getHottestDaysInMonthAcrossYears('03'))

print displayHighsFromListOfDates(getColdestDaysInYear('1982'))
# print displayHighsFromListOfDates(getColdestDaysInYearAndMonth('2016', '05'))
# print displayHighsFromListOfDates(getColdestDaysInMonthAcrossYears('03'))
