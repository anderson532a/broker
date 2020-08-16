import os
import socket

    
exepath = "C:\\gaminganywhere-0.8.0\\bin\\"
configpath = "C:\\gaminganywhere-0.8.0\\bin\\config\\"
gamepath = "C:\\gamefile\\"

S_EVD = "start ga-server-event-driven config//"
S_PD = "start ga-server-periodic config//"

hostname = socket.gethostname()
IPadrr = socket.gethostbyname(hostname)

IP = ""
selectconfig = ""


class IP_config:
    def __init__(self):
        self.status = 1

    def set_config(self, selectconfig):
        self.selectconfig = selectconfig

    # start game
        os.chdir(exepath)
        self.status = os.system(S_EVD + self.selectconfig)
        if self.status == 0:
            print("game excuted")
        else:
            print("game failed")

    def get_IP(self):
        if self.status == 0:
            return IPadrr
        else:
            return IP


# check match config
'''
os.chdir(configpath)
configfile = os.listdir("./")
for i in range(len(configfile)):
    if selectconfig == configfile[i]
    break

'''

# selectconfig = "server.neverball.conf"



        