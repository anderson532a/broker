import os, threading, sys
from zipfile import ZipFile
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
    
    def auto(self, A ,B):
        self.set_config(A, B)
        IPadr = self.get_IP()
        PID = self.get_PID()
        return [IPadr, PID]


class sync_DB(threading.Thread):
    def __init__(self, PID):
        self.S = SQL_connect.readSQL()
        self.I = SQL_connect.writeSQL()
        self.pid = PID

    # 同步DB server 之 PID 狀態
    def pid_check(self):
        logging.info('pid_check start')
        if self.pid == '':
            logging.info("NO game pid in server")
            self.I.update(col = "status", val = "TRUE", **{"status":"FALSE"})
        elif psutil.pid_exists(int(self.pid)) != True:
            logging.info("pid diff & change")
            self.I.update(col = "pid", val = self.pid, **{"status":"FALSE"})
            
        else:
            logging.info("pid exist")

    def gameDB_check(self):
        # select gamename, pid, status,  from gaconnection where serverIp = IPadrr
        Data = self.S.select(*("gamename", "pid", "status"), **{"serverIp":IPadrr})
        ppid = ''
        logging.info('gameDB_check start')
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

    def gameDBthread(self):
        t = threading.currentThread()
        while getattr(t, "loop", True):
            self.gameDB_check()
            time.sleep(20)

    def pidthread(self):
        t = threading.currentThread()
        while getattr(t, "loop", True):
            self.pid_check()
            time.sleep(5)

    def childthread(self, W):
        if W == "p":
            self.T = threading.Thread(target = self.pidthread())
        else:
            self.T = threading.Thread(target = self.gameDBthread())
        # self.T.setDaemon(True)
        self.T.start()
        self.T.join()   
    def stopthread(self):
        self.T.loop = False


class Handler(BaseRequestHandler):
    nowgame = ''
    def handle(self):
        global nowgame, gamepid
        logging.debug(f"nowpid : {nowgame}")
        while True:
            sync_DB(nowgame).pid_check()
            self.data = self.request.recv(1024).strip()
            logging.info(f"send length = {len(self.data)}")
            logging.debug(f"server receive = {self.data}")

            if self.data == bytes("sendfile".encode()) or self.data == bytes("done".encode()):
                logging.debug("server receive file")
                Zip = ZipFile("receive.zip" , 'w')
                try:
                    with open ("receive.zip", "wb") as wb:
                        while self.data != bytes("done".encode()):
                            self.data = self.request.recv(1024)
                            logging.info("server writing file....")
                            if not self.data:
                                break
                            wb.write(self.data)
                    self.request.sendall("TRUE".encode('utf-8'))
                    logging.info("file sending finish")

                except:
                    logging.error("file error", exc_info=True)
                    self.request.sendall("FAlSE".encode('utf-8'))
                
            elif len(self.data) > 0: # and len(self.data) < 100:
                raw = self.data.decode('utf-8')
                self.brokercmd = json.loads(raw)
                if "gameId" and "excuteMode" and "configfile" in self.brokercmd:
                    gameID = self.brokercmd["gameId"]
                    exmode = self.brokercmd["excuteMode"]
                    config = self.brokercmd["configfile"]
                    gamename = config.split('.')[1]
                    logging.info(f"Now game number : {len(nowgame)}")
                    game = excute_game()

                    if nowgame == '':
                        [IPadr, PID]= game.auto(config, exmode)
                        if PID != "":
                            nowgame = PID
                            gamepid = {nowgame: gamename}
                            # sync_DB(nowgame).childthread("g")
                            logging.info(f"now game: {gamepid}")

                    elif len(gamepid) == 1:
                        if gamename in gamepid.values():
                            pass
                        else:
                            os.system(f"taskkill /F /PID {nowgame}")
                            [IPadr, PID]= game.auto(config, exmode)
                            nowgame = PID
                            gamepid = {nowgame : gamename}
                            logging.info(f"kill pid {gamepid}")

                    else:
                        logging.error("to many process")

                    if IPadr == "" and PID == "":
                        retdata = {"gamestatus": "FALSE",
                                   "gameIP": IPadr, "PID": PID}
                    else:
                        retdata = {"gamestatus": "TRUE",
                                   "gameIP": IPadr, "PID": PID}

                elif "gamename" and "file" in self.brokercmd:
                    gname = self.brokercmd["gamename"]
                    self.filename = self.brokercmd["file"]
                    NEWmes = config_editor.create_new(name = gname).create()
                    retdata = {f"{IPadrr}": NEWme}

                else:
                    logging.error("server can't recognize args")

                self.request.sendall(json.dumps(retdata).encode('utf-8'))
            
            else:
                logging.warning("didn't receive by broker")
                break

if __name__ == "__main__":  # server_socket
    PORT = 8000
    ADDR = (IPadrr, PORT)
    server = ThreadingTCPServer(ADDR, Handler)
    logging.info("server_socket start")
    server.serve_forever()
