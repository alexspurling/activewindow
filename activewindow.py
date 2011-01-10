from subprocess import Popen, PIPE
import re

class ActiveWindow:

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


aw = ActiveWindow()

print aw.get_active_window_title()


