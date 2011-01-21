
import re
from operator import itemgetter

logfile = "activewindow.log"
f = open(logfile, 'r')

windowtimes = {}

lasttime = 0

def get_all_string_tokens(str):
    alltokens = re.split("[^\w]+", str)
    nonemptytokens = [token for token in alltokens if len(token) > 0]
    print "Split: %s" % nonemptytokens
    return get_all_list_tokens(nonemptytokens)

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

def record_window_time(titlestr, time):
    alltitletokens = get_all_string_tokens(titlestr)
    
    for titletoken in alltitletokens:
        totaltime = time
        if titletoken in windowtimes:
            totaltime += windowtimes[titletoken]

        windowtimes[titletoken] = totaltime

for line in f:

    m = re.match('^([0-9]+) "(.*[^\\\\"])" "(.*)"$', line)

    if m != None:
        curtime = long(m.group(1))
        command = m.group(2)
        title = m.group(3)

        if lasttime != 0:
            time = curtime - lasttime
            print "Title: %s time: %s" % (title, time)
            record_window_time(title, time)

        lasttime = curtime


sortedtimes = sorted(windowtimes.iteritems(), key=itemgetter(1), reverse=True)

print sortedtimes
