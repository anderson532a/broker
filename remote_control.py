import os
import socket
import subprocess
import time

exepath = "C:\\gaminganywhere-0.8.0\\bin\\"
configpath = "C:\\gaminganywhere-0.8.0\\bin\\config\\"
gamepath = "C:\\gamefile\\"

S_EVD = "start ga-server-event-driven config//"
S_PD = "start ga-server-periodic config//"
TER = "taskkill /F /IM "

_hostname = socket.gethostname()
_IPadrr = socket.gethostbyname(_hostname)

IP = ""

class excute_game:
    def __init__(self):
        self.status = 1
        self.pid = ""

    def set_config(self, selectconfig, exmode):
        self.selectconfig = selectconfig
        self.exmode = exmode
        Name = self.selectconfig.split('.')[1]
        if self.exmode == "event-driven":
            _CMD = S_EVD + self.selectconfig
            os.chdir(exepath)
            self.status = os.system(_CMD)  # start gaminganywhere
            time.sleep(1)
            get = subprocess.getoutput(f"WMIC PROCESS WHERE Name=\"{Name}.exe\" get Processid")
            self.pid = get.split()[-1]
        else:  # self.exmode == "periodic"
            _CMD = S_PD + self.selectconfig
            process = subprocess.Popen(
                gamepath + f"{Name}\\{Name}\\{Name}.exe")
            self.pid = process.pid
            os.chdir(exepath)
            self.status = os.system(_CMD)
            # except FileNotFoundError:    #not find file
        if self.status == 0:
            print("game excuted")
        else:
            print("game failed")

    def get_IP(self):
        if self.status == 0:
            return _IPadrr
        else:
            return IP

    def get_PID(self):
        if self.pid != "":
            print("get pid")
        else:
            print("lost pid")
        return self.pid

