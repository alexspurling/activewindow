#!/bin/bash

function getCurWindowName {
	read D1 D2 D3 D4 windowid <<< "`xprop -root _NET_ACTIVE_WINDOW`"
	read D1 D2 windowname <<< "`xprop -id $windowid WM_NAME`"
}

logfile="activewindows"

#Create the active window log file if it doesn't already exist
if [ ! -e "$logfile" ]
then
	touch "$logfile"
fi

lastline=`tail -1 "$logfile"`
lastwindowname=`echo $lastline | awk '{print $2}'`

while [ "true" ]
do
	getCurWindowName

	if [ "$windowname" != "$lastwindowname" ]
	then
		curtime=$(($(date +%s%N)/1000000))
		echo "$curtime $windowname" >> $logfile
		echo "$curtime $windowname"
		lastwindowname=$windowname
	fi

	sleep 1
done


