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
        Name = self.selectconfig.split('.')[1]
        k = kill_process(f"{Name}.exe")
        k.check_dupli()

        if self.extype == "event-driven":
            _CMD = S_EVD + self.selectconfig
        else:
            _CMD = S_PD + self.selectconfig
            os.popen(gamepath + f"{Name}\\{Name}\\{Name}.exe")

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
        self.CMD = TER + f"{self.Name}"

    def terminate(self):
        os.system(self.CMD)
    
    def check_dupli(self):
        for proc in psutil.process_iter():           
            if proc.name() == self.Name:
                os.system(self.CMD)


# selectconfig = "server.neverball.conf"
