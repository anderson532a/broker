import os
import socket
import psutil


exepath = "C:\\gaminganywhere-0.8.0\\bin\\"
configpath = "C:\\gaminganywhere-0.8.0\\bin\\config\\"
gamepath = "C:\\gamefile\\"

S_EVD = "start ga-server-event-driven config//"
S_PD = "start ga-server-periodic config//"
TER = "taskkill /F /IM "

_hostname = socket.gethostname()
_IPadrr = socket.gethostbyname(_hostname)

IP = ""

class IP_config:
    def __init__(self):
        self.status = 1

    def set_config(self, selectconfig, extype):
        self.selectconfig = selectconfig
        self.extype = extype

        if self.extype == "event-driven":
            _CMD = S_EVD + self.selectconfig
        else:
            Name = self.selectconfig.split('.')[1]
            _CMD = S_PD + self.selectconfig
            p = psutil.popen(gamepath + f"{Name}\\{Name}\\{Name}.exe")

    # start gaminganywhere
        os.chdir(exepath)
        self.status = os.system(_CMD)
        if self.status == 0:
            print("game excuted")
        else:
            print("game failed")

    def get_IP(self):
        if self.status == 0:
            return _IPadrr
        else:
            return IP


class kill_process:
    def __init__(self, Name, pid=None):
        self.Name = Name
        self.pid = pid

    def terminate(self):
        _CMD = TER + f"{self.Name}.exe"
        os.system(_CMD)
    
'''
    def check_kill(self):
'''


# selectconfig = "server.neverball.conf"
