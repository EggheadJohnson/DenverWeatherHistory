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
    meta = {}

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

        if station not in meta:
            meta[station] = {
                'seen': 0,
                'hadTmax': 0,
            }

        if 'earliest' not in meta[station] or date < meta[station]['earliest']:
            meta[station]['earliest'] = date
        if 'latest' not in meta[station] or date > meta[station]['latest']:
            meta[station]['latest'] = date
        meta[station]['seen'] += 1
        if 'TMAX' in today and today['TMAX'] != '':
            meta[station]['hadTmax'] += 1


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

    summaries = {}
    for station in meta:
        summaries[station] = '{} - {} {}'.format(meta[station]['earliest'], meta[station]['latest'], 100.*meta[station]['hadTmax']/meta[station]['seen'])

    return {
        'dataSet': fileName,
        'meta': meta,
        'summaries': summaries,
        'dailyWeather': dailyWeather,
    }
