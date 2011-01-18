from subprocess import Popen, PIPE
import re
import time
import datetime

class ActiveWindow:

    #Taken from: http://stackoverflow.com/questions/3983946/get-active-window-title-in-x
    def get_active_window_title(self):
        root = Popen(['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout=PIPE)

        for line in root.stdout:
            m = re.search('^_NET_ACTIVE_WINDOW.* ([\w]+)$', line)
            if m != None:
                id_ = m.group(1)
                id_w = Popen(['xprop', '-id', id_, 'WM_NAME'], stdout=PIPE)
                break

        if id_w != None:
            id_w.wait()
            for line in id_w.stdout:
                match = re.match("WM_NAME\([A-Z]+\) = (?P<name>.+)$", line)
                if match != None:
                    return match.group("name")

        return "Unknown"
        
    def get_current_time(self):
        return "%d" % (time.time() * 1000)
        
    def log_window(self, f, currentwindow):
        logstring = "%s %s\n" % (self.get_current_time(), currentwindow)
        f.write(logstring)
        f.flush()

    def monitor_active_window(self):
        logfile="activewindow.log"
        with open(logfile, "a+") as f:

            lastwindow = None
            
            try:
                while True:
                    currentwindow = self.get_active_window_title()
                    if currentwindow != lastwindow:
                        self.log_window(f, currentwindow)
                        lastwindow = currentwindow
                    
                    time.sleep(1)
            except KeyboardInterrupt:
                self.log_window(f, "ActiveWindow terminated")
                print ""

aw = ActiveWindow()

aw.monitor_active_window()


