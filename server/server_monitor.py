import os, sys, subprocess
import socket, time
from socketserver import BaseRequestHandler, ThreadingTCPServer
import logging, json
import SQL_connect
import config_editor

# excute game command
exepath = "C:\\gaminganywhere-0.8.0\\bin\\"
configpath = "C:\\gaminganywhere-0.8.0\\bin\\config\\"
gamepath = "C:\\gamefile\\"

S_EVD = "start ga-server-event-driven config//"
S_PD = "start /min ga-server-periodic config//"
TER = "taskkill /F /IM "

hostname = socket.gethostname()
IPadrr = socket.gethostbyname(hostname)
nowgame = ()
IP = ""
FORMAT = "%(asctime)s %(levelname)s:%(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

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
        global nowgame
        while True:
            self.data = self.request.recv(1024).strip()
            logging.debug(f"send length = {len(self.data)}")
            if len(self.data) > 0:
                raw = self.data.decode('utf-8')
                logging.info(f"server receive =  {raw}")
                self.brokercmd = json.loads(raw)
                if "gameId" and "excuteMode" and "configfile" in self.brokercmd:
                        gameID = self.brokercmd["gameId"]
                        exmode = self.brokercmd["excuteMode"]   
                        config = self.brokercmd["configfile"]
                        logging.info(f"Now game number : {len(nowgame)}")
                        game = excute_game()
                        if len(nowgame) == 0:
                            game.set_config(config, exmode)
                            IPadr = game.get_IP()
                            PID = game.get_PID()
                            nowgame = (PID,)
                        elif len(nowgame) == 1:
                            os.system(f"taskkill /F /PID {nowgame[0]}")
                            game.set_config(config, exmode)
                            IPadr = game.get_IP()
                            PID = nowgame[0]
                            nowgame = (PID,)
                        else:
                            logging.error("to many process")
                        
                        if IPadr == "" and PID == "":
                            retdata = {"gamestatus":"FALSE", "gameIP":IPadr, "PID":PID}
                        else:
                            retdata = {"gamestatus":"TRUE", "gameIP":IPadr, "PID":PID}
                        self.request.sendall(json.dumps(retdata).encode('utf-8'))
                else:
                    logging.error("api receive wrong args")
            else:
                logging.warning("didn't receive by broker")
                break


class configfile:
    pass

'''
class system_monitor:
    def __init__(self):
        pass
'''

if __name__ == "__main__":# server_socket
    PORT = 8000
    ADDR = (IPadrr, PORT)
    server = ThreadingTCPServer(ADDR, Handler)
    logging.info("server_socket start")
    server.serve_forever()

