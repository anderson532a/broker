from flask import Flask, jsonify, request
from flask_cors import CORS
import os, json
import remote_control

UPLOAD_FOLDER = os.getcwd()
ALLOWED_EXTENSIONS = set(['zip'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)
server_ip = ("192.168.43.196",) # server ip   #%#
server_status = {server_ip[0]: None} # {server ip :game pid}
log = app.logger


class gameserver_CMD:
    _connection = None
    def __init__(self, ip):
        self.CMD = {"serverstatus":"refresh"}
        self.ip = ip
        self._connection = remote_control.client_socket(self.ip)

    def refresh(self):
        self._connection.jsncontrol(**self.CMD)

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
    global server_status
    startapi = dict(request.args)
    conip = request.remote_addr
    # log.info(server_status)
    for i in server_ip:
        log.info(f"serverIp :{i}")
        '''
        if i in server_status:
            retdata = {"gamestatus": "TRUE",
                                   "gameIP": i, "PID": server_status[i]}
            return jsonify(retdata)
        '''
        result = gameserver_CMD(i).APICTL(**startapi)
        log.debug(result)
        # server_status[i] = result["PID"]
        return jsonify(result)


@app.route('/End', methods=['GET'])
def endGame():
    global server_status
    exmode = request.args.get("excuteMode", type=str)
    ip = request.args.get("serverIp", type=str)
    pid = request.args.get("pid", type=str)
    remote_status = remote_control.remote(ip).taskkill(exmode, pid)
    result = gameserver_CMD(ip).refresh()

    if remote_status == 0 or "IDLE" in result:
        server_status[ip] = ""
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
    for i in server_ip:
        A = gameserver_CMD(i).APICTL(**CONFIG)
        filetransfer = remote_control.SftpClient(i)
        filetransfer.upload(filename=Zip.filename, name=File)
        filetransfer.close()
        B = gameserver_CMD(i).APICTL(**Finish)
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
        for i in server_ip:
            result = gameserver_CMD(i).APICTL(**BODY)
            if "false" in result.items():
                log.waring(f"wrong info: {result}")
                return {"status": "Edit failed"}
            
        return {"status": "Edit success"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
