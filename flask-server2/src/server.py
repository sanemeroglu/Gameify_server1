import flask
import sqlite3

from flask import request

from src.db_conn import DbManager
from src import EuclideanDistanceScore as euc
app = flask.Flask(__name__)
app.config["DEBUG"] = True
db = DbManager("db_file/mydb")



@app.route('/', methods=['GET'])
def home():
    return "Selam Sanem"

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            print({"Login":"Successful","user":db.get_user_info(request.form['username']),"gameinfo":db.get_user_game_info(request.form['username'])})
            return {"Login":"Successful","user":db.get_user_info(request.form['username']),"gameinfo":db.get_user_game_info(request.form['username'])}
        else:
            return {"Login":"Failed"}

@app.route('/getuserinfo/<username>', methods=['POST', 'GET'])
def getuserinfo(username):
    return db.get_user_info(username)

@app.route('/gettestusers', methods=['POST', 'GET'])
def gettestusers():
    return {"Users":["umit","gizem","sanem"]}

@app.route('/getfriendsuggestion/<username>', methods=['POST', 'GET'])
def getfriendsuggestion(username):
    user_data = db.get_user_game_interes()
    gamedatas = {}
    result=[]
    for data in user_data:
        if (data[0] is not None and data[1] is not None and data[2] is not None and data[3] is not None):
            user_score = int(data[3])
            user_name = data[0]
            user_level = int(data[2])
            game = data[1]
            gamedata = {
                user_name: {game: user_level, "game": int(game.replace("-", "").replace(" ", "").replace("'", ""), 36)}}
            gamedatas.update(gamedata)
    friendlist = euc.topMatches(gamedatas,username, n=5)
    for friend in friendlist:
        user_info=db.get_user_game_info(str(friend[1]))
        result.append("Username:"+user_info["username"]+"  Game:"+user_info["game"]+"  Game Type:"+user_info["gametype"]+"  Game Level:" +str(user_info["level"]) )
    return {"Users":result}


@app.route('/getusers', methods=['GET'])
def get_users():
    query= "select * from users"
    db.execute_query(query)
    return "success"

@app.route('/adduser', methods=['GET', 'POST'])
def add_user():
    content = request.form
    if(db.add_user(content)):
        return "Success"
    else:
        return "Failed, check if all fields exist"
@app.route('/addgame', methods=['GET', 'POST'])
def add_game():
    content = request.json
    if(db.add_game(content)):
        return  {"Result":"Success"}
    else:
        return  {"Result":"Fail"}


@app.route('/addgametouser/<username>', methods=['GET', 'POST'])
def addgametouser(username):
    content = request.json
    if (db.add_game_to_user(username,content)):
        return "Success"
    else:
        return "Failed, check if all fields exist"

@app.route('/getusergameinfo/<username>', methods=['GET', 'POST'])
def getusergameinfo(username):
    if (db.get_user_game_info(username)):
        return db.get_user_game_info(username)
    else:
        return {"Result":"Failed"}


def valid_login(username,password):
    result=db.get_username_password(username,password)
    if len(result)>0:
        return True
    else:
        return False

if __name__ == "__main__":
    app.run(host= '0.0.0.0')