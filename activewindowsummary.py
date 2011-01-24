
import re
from operator import itemgetter
from itertools import groupby

logfile = "activewindow.log"
f = open(logfile, 'r')

commandtimes = {}

lasttime = 0

def get_all_string_tokens(str):
    alltokens = re.split("[^\w]+", str)
    nonemptytokens = [token for token in alltokens if len(token) > 0]
    return set(get_all_list_tokens(nonemptytokens))

def get_all_list_tokens(list):
    if len(list) <= 1:
        return list
    else:
        tokenlist = []
        #Get all the sequences of strings that begin with the first token in the string
        for i in range(len(list), 0, -1):
            tokenlist.append(" ".join(list[0:i]))
        
        tokenlist.extend(get_all_list_tokens(list[1:]))
        return tokenlist

def record_window_time(command, titlestr, time):
    #Get the window times for this command
    windowtimes = commandtimes.get(command, {})
    commandtimes[command] = windowtimes

    windowtimes[titlestr] = time

    #Break the title up into word groups
    alltitletokens = get_all_string_tokens(titlestr)
    
    #For each word group string, record the time for this command
    for titletoken in alltitletokens:
        windowtimes[titletoken] = windowtimes.get(titletoken, 0) + time
        if command == "/usr/bin/gedit":
            print "titletoken: %s, time: %s, totaltime: %s" % (titletoken, time, windowtimes[titletoken])

for line in f:

    m = re.match('^([0-9]+) "(.*[^\\\\"])" "(.*)"$', line)

    if m != None:
        curtime = long(m.group(1))
        command = m.group(2)
        title = m.group(3)

        if lasttime != 0:
            time = curtime - lasttime
            print "Title: %s command: %s, time: %s" % (title, command, time)
            record_window_time(command, title, time)

        lasttime = curtime

for command in commandtimes:
    windowtimes = commandtimes[command]
    sortedwindowtimes = sorted(windowtimes.iteritems(), key=itemgetter(1), reverse=True)
    
    for timespent, windowtitles in groupby(sortedwindowtimes, lambda key: key[1]):
        for title in windowtitles:
            print "Title %s, time: %s" % (title, timespent)
        print " "

print sortedtimes
