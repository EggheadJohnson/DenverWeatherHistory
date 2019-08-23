from selectomatic import selectomatic, selectMonth, selectYear

class Slicer:
    def __init__(self, dailyWeather):
        self.dailyWeather = dailyWeather

    def returnTMAXForSorting(self, k):
        return int(self.dailyWeather[k]['TMAX'])

    def getExtremeDaysInList(self, listOfDates, hottest = True, count = 5):
        return sorted(listOfDates, reverse = hottest, key = self.returnTMAXForSorting)[:count]

    def getDatesFromKey(self,key):
        return filter(lambda x: key in x, self.dailyWeather.keys())

    def getHottestDaysInYear(self,year, count = 5):
        listOfDates = self.getDatesFromKey(year)
        return self.getExtremeDaysInList(listOfDates, True, count)

    def getHottestDaysInYearAndMonth(self,year, month, count = 5):
        dateString = year + '-' + month
        listOfDates = self.getDatesFromKey(dateString)
        return self.getExtremeDaysInList(listOfDates, True, count)

    def getHottestDaysInMonthAcrossYears(self,month, count = 5):
        dateString = '-' + month + '-'
        listOfDates = self.getDatesFromKey(dateString)
        return self.getExtremeDaysInList(listOfDates, True, count)

    def getColdestDaysInYear(self,year, count = 5):
        listOfDates = self.getDatesFromKey(year)
        return self.getExtremeDaysInList(listOfDates, False, count)

    def getColdestDaysInYearAndMonth(self,year, month, count = 5):
        dateString = year + '-' + month
        listOfDates = self.getDatesFromKey(dateString)
        return self.getExtremeDaysInList(listOfDates, False, count)

    def getColdestDaysInMonthAcrossYears(self,month, count = 5):
        dateString = '-' + month + '-'
        listOfDates = self.getDatesFromKey(dateString)
        return self.getExtremeDaysInList(listOfDates, False, count)

    def displayHighsFromListOfDates(self,listOfDates):
        for date in listOfDates:
            print date + ': ' + self.dailyWeather[date]['TMAX']

def slicePicker(weatherData):
    selection = -1

    stations = weatherData['dailyWeather'].keys()
    stations.append('Exit')
    selection = selectomatic(stations)
    if selection != 'Exit':
        dataSet = weatherData['dailyWeather'][selection]
        slicer = Slicer(dataSet)

    extrema = ['Hottest', 'Coldest', 'Exit']
    periods = ['Month', 'Year', 'Month and Year', 'Exit']
    while selection != 'Exit':
        extreme = selectomatic(extrema)
        while extreme != 'Exit':
            period = selectomatic(periods)
            while period != 'Exit':
                if period == 'Month':
                    month = zeroPrefix(selectMonth())
                    month = zeroPrefix(month)
                    if extreme == 'Hottest':
                        slicer.displayHighsFromListOfDates(slicer.getHottestDaysInMonthAcrossYears(month))
                    elif extreme == 'Coldest':
                        slicer.displayHighsFromListOfDates(slicer.getColdestDaysInMonthAcrossYears(month))
                elif period == 'Year':
                    year = selectYear(getEarliestYearInDataSet(dataSet))
                    if extreme == 'Hottest':
                        slicer.displayHighsFromListOfDates(slicer.getHottestDaysInYear(year))
                    elif extreme == 'Coldest':
                        slicer.displayHighsFromListOfDates(slicer.getColdestDaysInYear(year))
                elif period == 'Month and Year':
                    year = selectYear(getEarliestYearInDataSet(dataSet))
                    month = zeroPrefix(selectMonth())
                    if extreme == 'Hottest':
                        slicer.displayHighsFromListOfDates(slicer.getHottestDaysInYearAndMonth(year, month))
                    elif extreme == 'Coldest':
                        slicer.displayHighsFromListOfDates(slicer.getColdestDaysInYearAndMonth(year, month))
                period = selectomatic(periods)
            extreme = selectomatic(extrema)
        selection = selectomatic(stations)



def zeroPrefix(number, targetLength = 2):
    string = str(number)
    return '0'*(targetLength - len(string)) + string

def getEarliestYearInDataSet(dataSet):
    minYear = False
    for date in dataSet:
        year = int(date.split('-')[0])
        if not year or year < minYear:
            minYear = year
    return minYear
