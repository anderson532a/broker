from flask import Flask, jsonify, request
from flask_cors import CORS
import os, json
import remote_control

UPLOAD_FOLDER = os.getcwd()
ALLOWED_EXTENSIONS = set(['zip'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)
# server_ip = ("192.168.43.196",) # server ip   ###
# server_status = {server_ip[0]: None} # {server ip : player ip}
log = app.logger


class serverstatus:
    status = {}
    IP = ()
    def __init__(self):
        self.IP = ("192.168.43.196",) # server ip   ###
        for i in self.IP:
            self.status[i] = None # {server ip : player ip}
        self.Log()

    @classmethod
    def Log(cls):
        log.info(f'server status : {cls.status}')

    @classmethod
    def get_value(cls):
        return cls.status.values()

    @classmethod
    def get_IP(cls):
        log.info(f'server IP : {cls.IP}')
        return cls.IP

    def release(self, Sip):
        self.Log()
        self.status[Sip] = None
        self.Log()

    def asign(self, Cip):
        self.Log()
        AS = False
        for i in self.IP:
            if self.status[i] != None:
                log.info(f'ip : {i} running game')
            else:
                self.status[i] = Cip
                AS = True
                break
        self.Log()
        if AS == False:
            log.info('server full please wait')
    

class gameserver:
    _connection = None
    def __init__(self, ip):
        self.CMD = {"serverstatus":"refresh"}
        self.ip = ip
        self._connection = remote_control.client_socket(self.ip)

    def refresh(self):
        result = self._connection.jsncontrol(**self.CMD)
        SS.release(result["Idle"])


    def APICTL(self, **DIC):
        self.CMD = DIC
        result = self._connection.jsncontrol(**self.CMD)
        return result

@app.route("/")
def home():
    return "broker for gaminganywhere"


@app.route('/TEST', methods=['GET', 'POST'])
def test():
    if request.method == 'GET':
        A = dict(request.args)
        log.debug(f"{A}, {type(A)}")
        gameID = request.args.get("gameId", type=str)
        exmode = request.args.get("excuteMode", type=str)
        selectconfig = request.args.get("configfile", type=str)
        ip = request.remote_addr
        IPadr = "123.123.123.123"
        return jsonify(gamestatus="TRUE", gameIP=IPadr, clientIP=ip)
    elif request.method == 'POST':
        gname = request.form.get('gamename')
        DATA = dict(request.form)
        del DATA['gamename']
        IP = dict(request.args)
        print(gname)
        print(DATA, IP)
        return "good"


# api excute game
@app.route('/IP', methods=['GET'])
def startGame():
    # global server_status
    startapi = dict(request.args)
    conip = request.remote_addr
    for i in IP_T:

        if i in SS.get_value():
            retdata = {"gamestatus": "TRUE",
                                   "gameIP": i, "PID": ""}
            return jsonify(retdata)
        else:
            result = gameserver(i).APICTL(**startapi)
            log.debug(result)
            SS.asign(conip)
            return jsonify(result)


@app.route('/End', methods=['GET'])
def endGame():
    exmode = request.args.get("excuteMode", type=str)
    ip = request.args.get("serverIp", type=str)
    pid = request.args.get("pid", type=str)
    remote_status = remote_control.remote(ip).taskkill(exmode, pid)
    gameserver(ip).refresh()

    if remote_status == 0 :
        return jsonify(gamestatus="end game sucessful")
    else:
        return jsonify(gamestatus="failed")


@app.route('/Add', methods=['POST'])
def addgame():
    gname = request.args.get('gamename', type=str)
    CONFIG = dict(request.form)
    CONFIG['gamename'] = gname

    Zip = request.files['zip']
    Zip.save((os.path.join(app.config['UPLOAD_FOLDER'], Zip.filename)))
    log.info(f"API get zip : {Zip.filename}")
    File = f"{gname}.zip"
    CONFIG['file'] = File
    result = {}
    Finish = dict()
    Finish['gamename'] = gname
    Finish['finishfile'] = File
    for i in IP_T:
        A = gameserver(i).APICTL(**CONFIG)
        filetransfer = remote_control.SftpClient(i)
        filetransfer.upload(filename=Zip.filename, name=File)
        filetransfer.close()
        B = gameserver(i).APICTL(**Finish)
        result.update(A)
        result.update(B)
    
    os.remove(Zip.filename)
    if "false" in result.items():
        return {"status": "FALSE to upload"}
    else:
        return {"status": "TRUE"}
    
    

@app.route('/Conf', methods=['POST'])
def config():
    BODY= request.get_json()
    # log.debug(f"post body: {BODY}")
    C = BODY['config']
    
    if len(BODY['config']) < 1:
        log.warning("no data in config body")
        return "no config body"
    else:
        for i in IP_T:
            result = gameserver(i).APICTL(**BODY)
            if "false" in result.items():
                log.waring(f"wrong info: {result}")
                return {"status": "Edit failed"}
            
        return {"status": "Edit success"}


if __name__ == "__main__":
    SS = serverstatus()
    IP_T = SS.get_IP()
    app.run(host="0.0.0.0", debug=True)
    