
from flask import Flask, jsonify, request
from flask_cors import CORS
import SQL_connect
import server_monitor
import remote_control

app = Flask(__name__)
CORS(app)
IPadr = ""

@app.route("/")
def home():
    return "broker for gaminganywhere"

@app.route('/TEST', methods=['GET'])
def test():
    gameID = request.args.get("gameId", type=str)
    proID = request.args.get("providerId", type=str)
    selectconfig = request.args.get("configfile", type=str)
    ip = request.remote_addr
    IPadr = "123.123.123.123"
    return jsonify(gamestatus="TRUE", gameIP=IPadr, clientIP=ip)


# api excute game
@app.route('/IP', methods=['GET'])
def startGame():
    gameID = request.args.get("gameId", type=str)
    exmode = request.args.get("excutemode", type=str)
    config = request.args.get("configfile", type=str)
    game = server_monitor.excute_game()
    game.set_config(config, exmode)
    IPadr = game.get_IP()
    PID = game.get_PID()
    if IPadr == "" and PID == "":
        return jsonify(gamestatus="FALSE", gameIP=IPadr, PID=PID)
    else:
        print(f"{IPadr},{PID}")
        return jsonify(gamestatus="TRUE", gameIP=IPadr, PID=PID)


@app.route('/End', methods=['GET'])
def endGame(): 
    exmode = request.args.get("excutemode", type=str)
    serverip = request.args.get("serverip", type=str)
    pid = request.args.get("pid", type=str)
    remote_status = remote_control.remote(serverip).taskkill(exmode, pid)
    
    if remote_status == 0: 
        return jsonify(gamestatus="end game sucessful")
    else:
        return jsonify(gamestatus="failed")


@app.route('/add', methods=['POST'])
def install():
    pass

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
