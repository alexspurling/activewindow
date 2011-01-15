from subprocess import Popen, PIPE
import re
import time
import datetime

class ActiveWindow:

    #Taken from: http://stackoverflow.com/questions/3983946/get-active-window-title-in-x
    def get_active_window_title(self):
        root_check = ''
        root = Popen(['xprop', '-root'],  stdout=PIPE)

        if root.stdout != root_check:
            root_check = root.stdout

        for i in root.stdout:
            if '_NET_ACTIVE_WINDOW(WINDOW):' in i:
                id_ = i.split()[4]
                id_w = Popen(['xprop', '-id', id_], stdout=PIPE)
        id_w.wait()
        buff = []
        for j in id_w.stdout:
            buff.append(j)

        for line in buff:
            match = re.match("WM_NAME\((?P<type>.+)\) = (?P<name>.+)", line)
            if match != None:
                type = match.group("type")
                if type == "STRING" or type == "COMPOUND_TEXT":
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


