import os
import sys
import subprocess, psutil
import socket
import time
from socketserver import BaseRequestHandler, ThreadingTCPServer
import logging
import json
import config_editor, SQL_connect

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
gamepid = {} # {nowgame[]: gamename}
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
            get = subprocess.getoutput(
                f"WMIC PROCESS WHERE Name=\"{Name}.exe\" get Processid")
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
            logging.info(f" {Name} game excuted")
        else:
            logging.info("game failed")

    def get_IP(self):
        if self.status == 0:
            return IPadrr
        else:
            return IP

    def get_PID(self):
        if self.pid != "":
            logging.info(f"get pid : {self.pid}")
        else:
            logging.info("lost pid")
        return self.pid

class sync_DB:
    def __init__(self, PID): 
        self.S = SQL_connect.readSQL()
        self.I = SQL_connect.writeSQL()
        self.pid = PID

    def pid_check(self):
        if psutil.pid_exists(self.pid) != True:
            self.I.update(col="pid", val = self.pid, **{"status":"FALSE"})
        logging.info("pid check")

    def gameDB_check(self):
        # select gamename, pid, status,  from gaconnection where serverIp = IPadrr
        Data = self.S.select(*("gamename", "pid", "status"), **{"serverIp":IPadrr})
        ppid = ''
        for line in reversed(Data):
            # 檢查DB status
            if 'TRUE' in line:
                if line[1] == self.pid:
                    logging.info('server & DB pid sync')
                else:
                    logging.info('server & DB double TRUE')
                    # update gaconnection set status='FALSE' where PID=self.pid
                    self.I.update(col="pid", val = line[1], **{"status":"FALSE"})
            # 重複PID
            if line[1] == ppid:
                logging.info('DB has double pid')
 

                      
class Handler(BaseRequestHandler):
    def handle(self):
        global nowgame
        SYN = sync_DB()
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
                    gamename = config.split('.')[1]
                    logging.info(f"Now game number : {len(nowgame)}")
                    game = excute_game()

                    if len(nowgame) == 0:
                        game.set_config(config, exmode)
                        IPadr = game.get_IP()
                        PID = game.get_PID()
                        nowgame = (PID, )
                        gamepid = {nowgame[0]: gamename}
                        logging.info(f"{gamepid}")

                    elif len(nowgame) == 1:
                        if gamename in gamepid.values():
                            pass
                        else:
                            os.system(f"taskkill /F /PID {nowgame[0]}")
                            game.set_config(config, exmode)
                            IPadr = game.get_IP()
                            PID = game.get_PID()
                            nowgame = (PID,)
                            gamepid = {nowgame[0]: gamename}
                            logging.info(f"kill pid {gamepid}")

                    else:
                        logging.error("to many process")

                    if IPadr == "" and PID == "":
                        retdata = {"gamestatus": "FALSE",
                                   "gameIP": IPadr, "PID": PID}
                    else:
                        retdata = {"gamestatus": "TRUE",
                                   "gameIP": IPadr, "PID": PID}

                elif "gamename" and "excuteMode" in self.brokercmd:
                    gname = self.brokercmd["gamename"]
                    exmode = self.brokercmd["excuteMode"]
                    NEWmes = config_editor.create_new(gname, mode=exmode).create()
                    retdata = {f"{IPadrr}": NEWmes}

                else:
                    logging.warnings("server can't recognize args")

                self.request.sendall(json.dumps(retdata).encode('utf-8'))
            else:
                logging.error("didn't receive by broker")
                break


if __name__ == "__main__":  # server_socket
    PORT = 8000
    ADDR = (IPadrr, PORT)
    server = ThreadingTCPServer(ADDR, Handler)
    logging.info("server_socket start")
    server.serve_forever()
