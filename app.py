
from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import excute_game

app = Flask(__name__)
CORS(app)
IPadr = ""
pre_game = ""


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
    return jsonify(gamestatus="TRUE", gameIP=IPadr)


# api excute game
@app.route('/IP', methods=['GET'])
def selectGame():
    gameID = request.args.get("gameId", type=str)
    extype = request.args.get("excutetype", type=str)
    selectconfig = request.args.get("configfile", type=str)

    # if pre_game != "":

    game = excute_game.IP_config()
    game.set_config(selectconfig, extype)
    IPadr = game.get_IP()
    if IPadr == "":
        return jsonify(gamestatus="FALSE", gameIP=IPadr)
    else:
        return jsonify(gamestatus="TRUE", gameIP=IPadr)
        print(f"{IPadr}")

    pre_game = selectconfig.split('.')[1]


'''
@app.route('/terminate', methods=['GET'])
def endgame():
    name = request.args.get("name", type=str)
    ip = request.args.get("ip", type=str)
    print()
'''


@app.route('/Login', methods=['POST'])
def userlogin_info():
    user = request.values.get('username')
    pwd = request.values.get('password')


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
