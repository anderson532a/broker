import os, sys
import subprocess, psutil
from zipfile import ZipFile
import socket
import time
from socketserver import BaseRequestHandler, ThreadingTCPServer
import logging, json
import config_editor, SQL_connect

# excute game command
exepath = "C:\\gaminganywhere-0.8.0\\bin\\"
configpath = "C:\\gaminganywhere-0.8.0\\bin\\config\\"
gamepath = "C:\\gamefile\\"
oripath = os.getcwd()
S_EVD = "start ga-server-event-driven config//"
S_PD = "start /min ga-server-periodic config//"
TER = "taskkill /F /IM "

hostname = socket.gethostname()
IPadrr = socket.gethostbyname(hostname)
IP = ""
FORMAT = "%(asctime)s -%(levelname)s : %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

class game_status:
    def __init__(self):
        self.nowgame = ''
        self.gamepid = {} # {nowgame: gamename}
        self.log()
    
    def log(self):
        logging.info(f"now game: {self.gamepid}")

    def initial(self):
        self.nowgame = ''
        self.gamepid = {}
        self.log()

    def update_status(self, pid, name):
        self.nowgame = pid
        self.gamepid = {}
        self.gamepid[pid] = name
        self.log()

    def get_nowgame(self):
        return self.nowgame
    
    def get_len(self):
        return len(self.gamepid)

    def get_dict(self):
        return self.gamepid


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
            time.sleep(3)
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
            logging.info(f"{Name} game excuted")
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

    @classmethod
    def kill_game(cls, pid):
        os.system(f"taskkill /F /PID {pid}")
        cmd = "TASKLIST", "/FI", "imagename eq ga-server-periodic.exe"
        GA = subprocess.check_output(cmd).decode('big5').split()
        if "ga-server-periodic.exe" in GA:
            os.system(TER + "ga-server-periodic.exe")
        logging.info(f"kill pid {pid}")


class sync_DB:
    def __init__(self, PID):
        self.S = SQL_connect.readSQL()
        self.I = SQL_connect.writeSQL()
        self.pid = PID

    # 同步DB server 之 PID 狀態
    def pid_check(self):
        logging.info('-- pid_check start --')
        if self.pid == '':
            logging.info("NO game pid in server")
            DB = self.S.select(*("pid", "status"), **{"serverIp":IPadrr})
            # logging.debug(f"{DB}")
            TF = list(zip(*DB))
            if 'TRUE' in TF[1]:
                self.I.update(col = "status", val = "TRUE", **{"status":"FALSE"})
        elif psutil.pid_exists(int(self.pid)) != True:
            logging.info("pid diff & change")
            self.I.update(col = "pid", val = self.pid, **{"status":"FALSE"})
            
        else:
            logging.info("pid exist")

    def gameDB_check(self):
        # select gamename, pid, status from gaconnection where serverIp = IPadrr
        Data = self.S.select(*("gamename", "pid", "status"), **{"serverIp":IPadrr})
        ppid = ''
        logging.info('-- gameDB_check start --')
        TF = list(zip(*Data))
        # 由DB 關遊戲
        
        if 'TRUE' not in TF[2]:
            if self.pid != '':
                excute_game.kill_game(self.pid)
                return "k"
        else:
            for line in reversed(Data):
                # 檢查DB status
                if 'TRUE' in line:
                    if line[1] == str(self.pid):
                        logging.info('server & DB pid sync')
                    else:
                        logging.info('server & DB diff TRUE')
                        # update gaconnection set status='FALSE' where PID=self.pid
                        self.I.update(col="pid", val = line[1], **{"status":"FALSE"})
                '''
                # 重複PID
                if line[1] == ppid:
                    logging.info('DB has double pid')
         '''


class Handler(BaseRequestHandler):
    def handle(self):
        i = 0
        while True:
            now = GS.get_nowgame()
            logging.info(f"nowpid : {now}")
            sync_DB(now).pid_check()
            if i > 0:
                time.sleep(2)
            PAR = sync_DB(now).gameDB_check()
            if PAR == "k":
                GS.initial()
                now = GS.get_nowgame()
            self.data = self.request.recv(1024).strip()
            logging.info(f"send length = {len(self.data)}")
            logging.debug(f"server receive = {self.data}")
            i += 1

            if self.data == bytes("sendfile".encode()) or self.data == bytes("done".encode()):
                filename = self.request.recv(1024).strip().decode('utf-8')
                logging.debug(f"server receive file : {filename}")
                try:
                    with open (filename, "wb") as wb:
                        while self.data != bytes("done".encode()):
                            self.data = self.request.recv(4096)
                            # logging.debug(f"data : {self.data}")
                            logging.info("server writing file....")
                            if not self.data:
                                break
                            wb.write(self.data)

                    self.request.sendall("TRUE".encode('utf-8'))
                    logging.info("file sending finish")
                    File = filename.strip('.zip')
                    with ZipFile(filename, 'r') as zp:
                        zp.extractall(os.path.join(gamepath, f"{File}"))
                        logging.info("unzip success")
                    os.remove(filename)

                except:
                    logging.error("file error", exc_info=True)
                    self.request.sendall("FALSE".encode('utf-8'))
                
            elif len(self.data) > 0:
                raw = self.data.decode('utf-8')
                self.brokercmd = json.loads(raw)
                if "gameId" and "excuteMode" and "configfile" in self.brokercmd:
                    # gameID = self.brokercmd["gameId"]
                    exmode = self.brokercmd["excuteMode"]
                    config = self.brokercmd["configfile"]
                    gamename = config.split('.')[1]
                    GS.log()
                    game = excute_game()

                    if now == '':
                        logging.info("--- first game start ---")
                        [IPadr, PID]= game.auto(config, exmode)
                        if PID != "":
                            GS.update_status(PID, gamename)

                    elif GS.get_len() == 1:
                        if gamename in GS.get_dict().values():
                            logging.info("--- same game ---")
                            IPadr = IPadrr
                            PID = GS.get_nowgame()
                        else:
                            logging.info("--- another game ---")
                            excute_game.kill_game(now)
                            [IPadr, PID]= game.auto(config, exmode)
                            if PID != "":
                                GS.update_status(PID, gamename)

                    else:
                        logging.error("--- out of range ---")

                    if IPadr == "" and PID == "":
                        retdata = {"gamestatus": "FALSE",
                                   "gameIP": IPadr, "PID": PID}
                    else:
                        retdata = {"gamestatus": "TRUE",
                                   "gameIP": IPadr, "PID": PID}

                elif "gamename" and "file" in self.brokercmd:
                    gname = self.brokercmd["gamename"]
                    self.filename = self.brokercmd["file"]
                    os.chdir(oripath)
                    NEWconf = config_editor.create_new(name = gname).create()
                    retdata = {f"{IPadrr}": NEWconf}

                elif "gamename" and "gaColumn" in self.brokercmd:
                    gname = self.brokercmd["gamename"]
                    data = {}
                    data['dictionary'] = self.brokercmd['dictionary']
                    data['gaColumn'] = self.brokercmd['gaColumn']
                    if self.brokercmd.get('value'):
                        data['value'] = self.brokercmd['value']
                    elif self.brokercmd.get('newValue'):
                        data['newValue'] = self.brokercmd['newValue']

                    MODIconf = config_editor.edit_config(gname).match_modify(**data)
                    retdata = {f"{IPadrr}": MODIconf}

                else:
                    logging.error("server can't recognize args")

                self.request.sendall(json.dumps(retdata).encode('utf-8'))
            
            else:
                logging.warning("didn't receive by broker")
                break

if __name__ == "__main__":  # server_socket
    PORT = 8000
    ADDR = (IPadrr, PORT)
    GS = game_status()
    sync_DB(GS.get_nowgame()).pid_check()
    server = ThreadingTCPServer(ADDR, Handler)
    logging.info("server_socket start")
    server.serve_forever()
