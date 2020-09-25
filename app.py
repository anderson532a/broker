from flask import Flask, jsonify, request
from flask_cors import CORS
import SQL_connect
import logging
import remote_control

app = Flask(__name__)
CORS(app)
server_ip = ("192.168.43.196",)
server_status = {server_ip[0]:""}

@app.route("/")
def home():
    return "broker for gaminganywhere"

@app.route('/TEST', methods=['GET', 'POST'])
def test():
    if request.method == 'GET':
        A = dict(request.args)
        logging.debug(f"{A}, {type(A)}")
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
        if server_status[i] == "":
            game = remote_control.client_socket(i)
            result = game.control(**startapi)
            server_status[i] = conip
            return jsonify(result)
        else:
            logging.warning("server is full !!!")
            return jsonify({"gamestatus":"FULL", "gameIP":"", "PID":""})

@app.route('/End', methods=['GET'])
def endGame(): 
    global server_status
    exmode = request.args.get("excuteMode", type=str)
    serverip = request.args.get("serverip", type=str)
    pid = request.args.get("pid", type=str)
    remote_status = remote_control.remote(serverip).taskkill(exmode, pid)

    if remote_status == 0:
        server_status[serverip ] = ""
        return jsonify(gamestatus="end game sucessful")
    else:
        return jsonify(gamestatus="failed")


@app.route('/Add', methods=['GET'])
def newgame():
    gname = request.form.get('gamename', type=str)
    CREAT = dict(request.args)
    for i in server_ip:
        config = remote_control.client_socket(i)
        result = config.control(**CREAT)

    return f"{gname}" + "create sucess"
    

@app.route('/Conf', methods=['POST'])
def config():
    gname = request.form.get('gamename', type=str)
    EDIT = dict(request.form)
    del EDIT['gamename']
    para = dict(request.args)
    COMME = {}
    if 'include' in str(EDIT):
        for k, v in EDIT.items():
            if 'include' in str(k):
                COMME[k]=v
                EDIT.pop(k)
    if para != {}:
        pass
    else:
        for i in server_ip:
            config = remote_control.client_socket(i)
            result1 = config.control(**{"gamename":gname})
            if EDIT != {}:
                logging.debug("edit : " + f"{EDIT}")
                result2 =config.control(**EDIT)
            if COMME != {}:
                logging.debug("comment : " + f"{COMME}")
                result3 =config.control(**COMME)

    return "get form"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)