class Slicer:
    def __init__(self, dailyWeather):
        self.dailyWeather = dailyWeather

    def returnTMAXForSorting(self, k):
        return self.dailyWeather['dailyWeather'][k]['TMAX']

    def getExtremeDaysInList(self, listOfDates, hottest = True, count = 5):
        return sorted(listOfDates, reverse = hottest, key = self.returnTMAXForSorting)[:count]

    def getDatesFromKey(self,key):
        return filter(lambda x: key in x, self.dailyWeather['dailyWeather'].keys())

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
            print date + ': ' + self.dailyWeather['dailyWeather'][date]['TMAX']
