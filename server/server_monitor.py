import os, sys
import subprocess
from zipfile import ZipFile
import socket
from socketserver import BaseRequestHandler, ThreadingTCPServer
import logging, json, time
import config_editor
import SQL_connect
###
# excute game command
exepath = "C:\\gaminganywhere-0.8.0\\bin\\"
configpath = "C:\\gaminganywhere-0.8.0\\bin\\config\\"
gamepath = "C:\\gamefile\\"
oripath = os.getcwd()
S_EVD = "start ga-server-event-driven config//"
S_PD = "start /min ga-server-periodic config//"
TER = "taskkill /F /IM "
brokerIP = '192.168.43.196'

hostname = socket.gethostname()
IPadrr = socket.gethostbyname(hostname)
IP = ""
FORMAT = "%(asctime)s -%(levelname)s : %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)


class game_status:
    def __init__(self):
        self.nowpid = ''
        self.gamepid = {}  # {nowpid: gamename}
        self.log()

    def log(self):
        logging.info(f"now game: {self.gamepid}")

    def initial(self):
        self.nowpid = ''
        self.gamepid = {}
        self.log()

    def update_status(self, pid, name):
        self.nowpid = pid
        self.gamepid = {}
        self.gamepid[pid] = name
        self.log()

    def get_nowpid(self):
        return self.nowpid

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
            logging.info(f"NEW game pid : {self.pid}")
        else:
            logging.info("lost pid")
        return str(self.pid)

    def auto(self, A, B):
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
    data = None
    def __init__(self, PID):
        #self.S = SQL_connect.readSQL()
        self.I = SQL_connect.writeSQL()
        self.pid = PID

    @classmethod
    def DB_check(cls):
        # select gamename, pid, status from gaconnection where serverIp = IPadrr
        cls.data = SQL_connect.readSQL().select(*("gamename", "pid", "status"),
                            **{"serverIp": IPadrr})
        if len(cls.data) == 0:
            logging.info("server IP has no read in select CMD")
        else:
            TF = list(zip(*cls.data))
            return TF

    # 同步DB server 之 PID 狀態

    def pid_check(self):
        logging.info('-- pid_check start --')
        if self.pid == '':
            logging.info("NO game pid in server")
            '''
            DB = self.S.select(*("pid", "status"), **{"serverIp":IPadrr})
            
            if len(DB) == 0:
                logging.info("server IP has no read in select CMD")
            else:
                TF = list(zip(*DB))
                '''
            CK = self.DB_check()
            if CK != None:
                if 'TRUE' in CK[2]:
                    self.I.update(col="status", val="TRUE",
                                  **{"status": "FALSE"})
        elif psutil.pid_exists(int(self.pid)) != True:
            logging.info("pid diff & change")
            self.I.update(col="pid", val=self.pid, **{"status": "FALSE"})

        else:
            logging.info("pid exist")

    def gameDB_check(self):
        logging.info('-- gameDB_check start --')
        ppid = ''
        CK = self.DB_check()
        DB = True
        for i in range(5):
            if 'TRUE' in CK[2]:
                DB = True
                break
            else:
                DB = False
                logging.info(f'no TRUE in select data {i}')
                time.sleep(1)
                CK = self.DB_check()
                # logging.info(f'{CK[2]}')

        if DB == False:
            # 由DB 關遊戲
            if self.pid != '':
                excute_game.kill_game(self.pid)
                return "k"
            else:
                pass
        else:
            for line in reversed(self.data):
                # 檢查DB status
                if 'TRUE' in line:
                    if line[1] == str(self.pid):
                        logging.info('server & DB pid sync')
                    else:
                        logging.info('server & DB diff pid')
                        # update gaconnection set status='FALSE' where PID=self.pid
                        self.I.update(
                            col="pid", val=line[1], **{"status": "FALSE"})


class Handler(BaseRequestHandler):
    def handle(self):
        while True:
            now = GS.get_nowpid()
            logging.info("-- socket server listen loop --")
            logging.info(f"nowpid : {now}")
            sync_DB(now).pid_check()
            PAR = sync_DB(now).gameDB_check()
            if PAR == "k":
                GS.initial()
                now = GS.get_nowpid()
            self.data = self.request.recv(2048).strip()
            logging.info(f"send length = {len(self.data)}")
            logging.info(f"server receive = {self.data}")

            if len(self.data) > 0:
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
                        [IPadr, PID] = game.auto(config, exmode)
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
                            [IPadr, PID] = game.auto(config, exmode)
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

                elif "refresh" in self.brokercmd.values():
                    GS.initial()
                    logging.info("-- server status refresh --")
                    retdata = {"gamestatus": "IDLE"}

                elif "gamename" and "file" in self.brokercmd:
                    gname = self.brokercmd["gamename"]
                    self.filename = self.brokercmd["file"]
                    os.chdir(oripath)
                    NEWconf = config_editor.create_new(name=gname).create()
                    retdata = {f"{IPadrr}": NEWconf}
                
                elif  "finishfile" in self.brokercmd:
                    File = self.brokercmd["finishfile"]
                    gname = self.brokercmd["gamename"]
                    os.chdir(gamepath)
                    try:
                        with ZipFile(File) as zf:
                            zf.extractall(gname)
                        zf.close()
                        os.remove(File)
                        logging.info(f"serverIP : {IPadrr} upload finish")
                        retdata = {f"{IPadrr}": "TRUE"}
                    except:
                        retdata = {f"{IPadrr}": "FALSE"}


                elif "gamename" and 'config' in self.brokercmd:
                    gname = self.brokercmd["gamename"]
                    MODIconf = self.brokercmd['config']
                    resconf = []
                    for i in range(len(MODIconf)):
                        data = {}
                        data['dictionary'] = MODIconf[i]['dictionary']
                        data['gaColumn'] = MODIconf[i]['gaColumn']
                        if MODIconf[i].get('value'):
                            data['value'] = MODIconf[i]['value']
                        elif MODIconf[i].get('newValue'):
                            data['newValue'] = MODIconf[i]['newValue']
                        resconf.append(config_editor.edit_config(
                            gname).match_modify(**data))
                    retdata = {f"{IPadrr}": resconf}

                else:
                    logging.error("server can't recognize args")

                self.request.sendall(json.dumps(retdata).encode('utf-8'))
                logging.info(f'server send = {retdata}')
            else:
                logging.warning("didn't receive by broker")
                break


if __name__ == "__main__":  # server_socket
    PORT = 8000
    ADDR = (IPadrr, PORT)
    GS = game_status()
    sync_DB(GS.get_nowpid()).pid_check()
    server = ThreadingTCPServer(ADDR, Handler)
    logging.info(f"server_socket start IP : {IPadrr}")
    server.serve_forever()
