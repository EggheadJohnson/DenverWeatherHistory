from os import listdir

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

print listdir('./data')

def listFiles():
    dataFiles = listdir('./data')
    for i, dataFile in enumerate(dataFiles):
        print "  " + str(i+1) + ": " + dataFile
    return dataFiles

def selectFile():
    print "Make a selection, number or filename from below:"
    files = listFiles()
    fileOrNumber = raw_input("Selection: ")
    if fileOrNumber.isdigit():
        number = int(fileOrNumber)
        fileName = files[number - 1]
    else:
        fileName = fileOrNumber
    return fileName

def loadFile(fileName):

    file = open('data/'+fileName)
    keys = splitLine(file.readline().strip())

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
        station = today['STATION']

        for key in today:
            if station not in dailyWeather:
                dailyWeather[station] = {}
            if date not in dailyWeather[station]:
                year, month, day = date.split('-')
                dailyWeather[station][date] = {
                  'zipcode': 80238,
                  'year': year,
                  'month': month,
                  'day': day
                }
            if key not in dailyWeather[station][date] or dailyWeather[station][date][key] == '':
                dailyWeather[station][date][key] = today[key]
    return {
        'dataSet': fileName,
        'dailyWeather': dailyWeather,
    }
