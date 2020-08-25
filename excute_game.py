import os
import socket

    
exepath = "C:\\gaminganywhere-0.8.0\\bin\\"
configpath = "C:\\gaminganywhere-0.8.0\\bin\\config\\"
gamepath = "C:\\gamefile\\"

S_EVD = "start ga-server-event-driven config//"
S_PD = "start ga-server-periodic config//"

_hostname = socket.gethostname()
_IPadrr = socket.gethostbyname(_hostname)

IP = ""
selectconfig = ""


class IP_config:
    def __init__(self):
        self.status = 1

    def set_config(self, selectconfig, extype):
        self.selectconfig = selectconfig
        self.extype = extype

        if self.extype == "event-driven":
            CMD = S_EVD + self.selectconfig
        else:
            Name = self.selectconfig.split('.')[1]
            CMD = S_PD + self.selectconfig
            os.popen(gamepath + f"{Name}\\{Name}\\{Name}.exe")

    # start gaminganywhere
        os.chdir(exepath)
        self.status = os.system(CMD)
        if self.status == 0:
            print("game excuted")
        else:
            print("game failed")

    def get_IP(self):
        if self.status == 0:
            return _IPadrr
        else:
            return IP


# selectconfig = "server.neverball.conf"



        