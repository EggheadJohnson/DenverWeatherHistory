import datetime

def selectomatic(options, optionalSummaries = {}):
    found = False
    while not found:
        print "Please make a selection by number, letter, or full text"
        for i, option in enumerate(options):
            if option in optionalSummaries:
                summary = optionalSummaries[option]
            else:
                summary = ''
            print "  " + str(i+1) + ": " + option + " " + summary
        selection = raw_input(" Selection: ")
        if selection.isdigit():
            selection = int(selection) - 1
            if selection >= len(options):
                print "Invalid selection"
                selection += 1
            else:
                selection = options[selection]
                found = True
        elif len(selection) == 1:
            selection = selection.upper()
            found = False
            for option in options:
                if option[0].upper() == selection:
                    selection = option
                    found = True
                    break
            if not found:
                print "Invalid selection"
        elif selection not in options:
            print "Invalid selection"
        elif selection in options:
            found = True
        print "Your selection was " + str(selection)
    return selection

def selectMonth():
    options = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    month = selectomatic(options)
    return options.index(month)+1

def selectYear(oldest = 1980):
    year = -1
    while not validYear(year, oldest):
        year = raw_input(" Select year: " )
    return year


def validYear(year, oldest = 0):
    try:
        year = int(year)
    except:
        return False
    if year > datetime.datetime.today().year:
        return False
    if year < oldest:
        return False
    return True
