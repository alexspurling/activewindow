from subprocess import Popen, PIPE
import os
import re
import time
import datetime

class ActiveWindow:

    #Taken from: http://stackoverflow.com/questions/3983946/get-active-window-title-in-x
    def get_active_window(self):
        root = Popen(['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout=PIPE)

        for line in root.stdout:
            m = re.search('^_NET_ACTIVE_WINDOW.* ([\w]+)$', line)
            if m != None:
                id_ = m.group(1)
                id_w = Popen(['xprop', '-id', id_, '_NET_WM_PID', 'WM_NAME'], stdout=PIPE)
                break

        pid = 0
        name = "Unknown"

        if id_w != None:
            for line in id_w.stdout:
                match = re.match("_NET_WM_PID\(\w+\) = (?P<pid>.+)$", line)
                if match != None:
                    pid = match.group("pid")

                match = re.match("WM_NAME\(\w+\) = \"(?P<name>.+)\"$", line)
                if match != None:
                    name = match.group("name")

        return (pid, name)

    def get_process_command_from_id(self, processid):
        if processid == 0:
            return ""

        command = os.readlink("/proc/%s/exe" % processid)
        return command

    def escape(self, str):
        #Surround the string in double quotes and escape any pre-existing double quotes
        return '"%s"' % str.replace("\"", "\\\"")

    def unescape(self, str):
        #Remove surrounding double quotes and replace escaped double quotes
        m = re.match("^\"(.*)\"$", a)
        if m != None:
            str = m.group(1)

        return str.replace("\"", "\\\"")
        
    def get_current_time(self):
        return "%d" % (time.time() * 1000)
        
    def log_window(self, f, currentcommand, currentwindow):
        logstring = "%s %s %s\n" % (self.get_current_time(), self.escape(currentcommand), self.escape(currentwindow))
        f.write(logstring)
        f.flush()

    def monitor_active_window(self):
        logfile="activewindow.log"
        with open(logfile, "a+") as f:

            lastwindow = None
            
            try:
                while True:
                    curpid, currentwindow = self.get_active_window()
                    if currentwindow != lastwindow:
                        currentcommand = self.get_process_command_from_id(curpid)
                        self.log_window(f, currentcommand, currentwindow)
                        lastwindow = currentwindow
                    
                    time.sleep(1)
            except KeyboardInterrupt:
                self.log_window(f, 'activewindow', 'ActiveWindow terminated')
                print ""

aw = ActiveWindow()

aw.monitor_active_window()


