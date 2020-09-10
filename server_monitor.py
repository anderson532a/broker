import os, sys
import socket
from socketserver import BaseRequestHandler, ThreadingTCPServer
import subprocess
import time
import logging

# excute game command
exepath = "C:\\gaminganywhere-0.8.0\\bin\\"
configpath = "C:\\gaminganywhere-0.8.0\\bin\\config\\"
gamepath = "C:\\gamefile\\"

S_EVD = "start ga-server-event-driven config//"
S_PD = "start /min ga-server-periodic config//"
TER = "taskkill /F /IM "

hostname = socket.gethostname()
IPadrr = socket.gethostbyname(hostname)

IP = ""
FORMAT = "%(asctime)s %(levelname)s:%(message)s"
logging.basicConfig(level=logging.DEBUG, filename='server.log', format=FORMAT)

class excute_game:
    def __init__(self):
        self.status = 1
        self.pid = ""

    def set_config(self, config, exmode):
        self.config = config
        self.exmode = exmode
        Name = self.config.split('.')[1]
        if self.exmode == "event-driven":
            _CMD = S_EVD + self.config
            os.chdir(exepath)
            self.status = os.system(_CMD)  # start gaminganywhere
            time.sleep(1)
            get = subprocess.getoutput(f"WMIC PROCESS WHERE Name=\"{Name}.exe\" get Processid")
            self.pid = get.split()[-1]

        else:  # self.exmode == "periodic"
            _CMD = S_PD + self.config
            process = subprocess.Popen(
                gamepath + f"{Name}\\{Name}\\{Name}.exe")
            self.pid = process.pid
            os.chdir(exepath)
            self.status = os.system(_CMD)
            # except FileNotFoundError:    #not find file
        if self.status == 0:
            logging.info("game excuted")
        else:
            logging.info("game failed")

    def get_IP(self):
        if self.status == 0:
            return IPadrr
        else:
            return IP

    def get_PID(self):
        if self.pid != "":
            logging.info("get pid")
        else:
            logging.info("lost pid")
        return self.pid


class Handler(BaseRequestHandler):
    def handle(self):
        while True:
            self.data = self.request.recv(1024).strip()
            if len(self.data) > 0:
                brockercmd = self.data.decode('utf-8')
                logging.info("receive = ", brockercmd)
                
            else:
                logging.warning("didn't receive by broker")
                break

class system_monitor:
    def __init__(self):
        nowgame = set()
    def gamecheck(self, pid):
        self.gamepid = pid
        if len(self.nowgame) == 0:
            self.nowgame.add(self.gamepid)
            return True
        elif len(self.nowgame) == 1:
            return True

        else:
            return False
            


if __name__ == "__main__":# server_socket
    PORT = 8000
    ADDR = (IPadrr, PORT)
    server = ThreadingTCPServer(ADDR, Handler)
    server.serve_forever()

    
