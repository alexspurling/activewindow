
import re
from operator import itemgetter

logfile = "activewindows"
f = open(logfile, 'r')

windowtimes = {}

lasttime = 0

for line in f:
        
	m = re.search('([0-9]+) (.*)', line)

	curtime = long(m.group(1))
	title = m.group(2)

	if lasttime != 0:
		time = curtime - lasttime

		totaltime = time
		if title in windowtimes:
			totaltime += windowtimes[title]

		windowtimes[title] = totaltime
		print "title: %s time: %s" % (title, time)
	
	lasttime = curtime


sortedtimes = sorted(windowtimes.iteritems(), key=itemgetter(1), reverse=True)

print sortedtimes
