
from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import winrm
import excute_game

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
def selectGame():
    gameID = request.args.get("gameId", type=str)
    extype = request.args.get("excutetype", type=str)
    selectconfig = request.args.get("configfile", type=str)
    game = excute_game.IP_config()
    game.set_config(selectconfig, extype)
    IPadr = game.get_IP()
    if IPadr == "":
        return jsonify(gamestatus="FALSE", gameIP=IPadr)
    else:
        return jsonify(gamestatus="TRUE", gameIP=IPadr)
        print(f"{IPadr}")


@app.route('/End', methods=['GET'])
def endgame():
    endconfigfile = request.args.get("configfile", type=str)
    ip = request.args.get("ip", type=str)
    name = endconfigfile.split('.')[1]
    session = winrm.Session(f"{ip}",auth=( 'RD' , 'Aa123456' ))
    cmd = session.run_cmd(f"taskkill /F /IM {name}.exe /IM ga-server-periodic.exe" )
    if cmd.status_code == 0: 
        return jsonify(gamestatus="end game sucessful", gamename=name)
    else:
        return jsonify(gamestatus="failed", gamename=name)



@app.route('/Login', methods=['POST'])
def userlogin_info():
    user = request.values.get('username')
    pwd = request.values.get('password')


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
