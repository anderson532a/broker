
from flask import Flask, jsonify, request
from flas_cors import CORS
import os
import excute_game

app = Flask(__name__)
CORS(app)
IPadr = ""

@app.route("/")
def home():
    return "broker for gaminganywhere"


@app.route('/IP', methods=['GET'])
def selectGame():
    gameID = request.args.get("gameId", type=str)
    proID = request.args.get("providerId", type=str)
    selectconfig = request.args.get("configfile", type=str)
    game = excute_game.IP_config()
    game.set_config(selectconfig)
    IPadr = game.get_IP()
    if IPadr == "":
        return jsonify(gamestatus="FALSE", gameIP=IPadr)
    else:
        return jsonify(gamestatus="TRUE", gameIP=IPadr)


@app.route('/Login', methods=['POST'])
def userlogin_info():
    user = request.values.get('username')
    pwd = request.values.get('password')


if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)