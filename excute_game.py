import os
import socket
import subprocess


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
        self.pid = ""

    def set_config(self, selectconfig, extype):
        self.selectconfig = selectconfig
        self.extype = extype
        Name = self.selectconfig.split('.')[1]

        if self.extype == "event-driven":
            _CMD = S_EVD + self.selectconfig
        else: # self.extype == "periodic"
            _CMD = S_PD + self.selectconfig
                process = subprocess.Popen(gamepath + f"{Name}\\{Name}\\{Name}.exe")
                self.pid = process.pid
'''not find file
            except FileNotFoundError:
                os.popen(gamepath + f"{Name}\\{Name}\\{Name}.exe")
'''
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

    def get_PID(self):
        if self.pid != "":
            print("get pid")
        else:
            print("lost pid")
        return self.pid






# selectconfig = "server.neverball.conf"

''' win powershell get pid
Get-Process | Where-Object { $_.ProcessName -eq 'cmd' } | ForEach-Object { $_.Id }
'''
