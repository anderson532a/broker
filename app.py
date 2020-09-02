
from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import winrm
import SQL_connect
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
def startGame():
    gameID = request.args.get("gameId", type=str)
    exmode = request.args.get("excutemode", type=str)
    selectconfig = request.args.get("configfile", type=str)
    game = excute_game.IP_config()
    game.set_config(selectconfig, exmode)
    IPadr = game.get_IP()
    if IPadr == "":
        return jsonify(gamestatus="FALSE", gameIP=IPadr)
    else:
        print(f"{IPadr}")
        return jsonify(gamestatus="TRUE", gameIP=IPadr)

@app.route('/Check', method=['GET'])
def checkstatus():

    ip = request.args.get("ip", type=str)

@app.route('/End', methods=['GET'])
def endGame():
    endname = request.args.get("gamename", type=str)
    serverip = request.args.get("serverip", type=str)
    session = winrm.Session(f"{serverip}",auth=( 'RD' , 'Aa123456' ))
    cmd = session.run_cmd(f"taskkill /F /IM {endname}.exe /IM ga-server-periodic.exe" )
    if cmd.status_code == 0: 
        return jsonify(gamestatus="end game sucessful", gamename=endname)
    else:
        return jsonify(gamestatus="failed", gamename=endname)



@app.route('/Login', methods=['POST'])
def userlogin_info():
    user = request.values.get('username')
    pwd = request.values.get('password')


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
