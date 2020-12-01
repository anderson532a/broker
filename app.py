from flask import Flask, jsonify, request
from flask_cors import CORS
import os, json
import remote_control

UPLOAD_FOLDER = os.getcwd()
ALLOWED_EXTENSIONS = set(['zip'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)
server_ip = ("192.168.43.196", )
server_status = {server_ip[0]: ""}
log = app.logger

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
    for i in server_ip:
        # if server_status[i] == "":
        game = remote_control.client_socket(i)
        result = game.control(**startapi)
        server_status[i] = conip
        return jsonify(result)
        '''
        else:
            log.warning("server is full !!!")
            return jsonify({"gamestatus": "FULL", "gameIP": "", "PID": ""})
'''

@app.route('/End', methods=['GET'])
def endGame():
    global server_status
    exmode = request.args.get("excuteMode", type=str)
    ip = request.args.get("serverIp", type=str)
    pid = request.args.get("pid", type=str)
    remote_status = remote_control.remote(ip).taskkill(exmode, pid)

    if remote_status == 0:
        server_status[ip] = ""
        return jsonify(gamestatus="end game sucessful")
    else:
        return jsonify(gamestatus="failed")


@app.route('/Add', methods=['POST'])
def addgame():
    gname = request.args.get('gamename', type=str)
    CONFIG = dict(request.form)
    CONFIG['gamename'] = gname
   # if 'file' not in request.files:
        #log.error("request with no file")
       # return "no file, please try again"
    #else:
    Zip = request.files['zip']
    Zip.save((os.path.join(app.config['UPLOAD_FOLDER'], Zip.filename)))
    log.info(f"API get zip : {Zip.filename}")
    File = f"{gname}.zip"
    CONFIG['file'] = File
    result = {}
    for i in server_ip:
        Upload = remote_control.client_socket(i)
        result.update(Upload.control(**CONFIG))
        filetransfer = SftpClient(i)
        filetransfer.upload(filename=Zip.filename, name=File)
        filetransfer.close()
        Upload.client.send("file_finish")
    
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
            config = remote_control.client_socket(i)
            result = config.control(**BODY)
            if "false" in result.items():
                log.waring(f"wrong info: {result}")
                return {"status": "Edit failed"}
            
        return {"status": "Edit success"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)