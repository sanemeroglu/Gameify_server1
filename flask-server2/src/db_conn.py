import sqlite3

class DbManager:

    def __init__(self,dbfile):
        self.dbfile = dbfile
        self.conn = sqlite3.connect(self.dbfile,check_same_thread=False)
        self.c = self.conn.cursor()

    def execute_query(self,query):
        self.c.execute(query)
        rows = self.c.fetchall()
        return rows
    def insert_data(self,query):
        self.c.execute(query)
        self.conn.commit()
        return self.c.lastrowid
    def get_username_password(self,username,password):
        query = "select * from users where username = '{}' and password='{}'".format(username, password)
        result = self.execute_query(query)
        return result

    def add_user(self,user_info):
        if all(key in user_info for key in ["name","surname","username","mail","age","password","game","level"]):
            query=f"INSERT INTO users(name,surname,username,mail,age,password) VALUES ('{user_info['name']}','{user_info['surname']}" \
                f"','{user_info['username']}','{user_info['mail']}',{user_info['age']},'{user_info['password']}');"
            print(query)
            print(user_info)
            query2=f"INSERT INTO usergamerel(username,game,level,user_score) VALUES ('{user_info['username']}','{user_info['game']}','{int(user_info['level'])}','{int(int(user_info['level'])/10+1)}');"
            print(query2)
            self.insert_data(query)
            self.insert_data(query2)
            return True
        else:
            return False

    def add_game(self,game_info):
        if all(key in game_info for key in ["game","game_type","game_score"]):
            query=f"INSERT INTO games(game,game_type,game_score) VALUES ('{game_info['game']}','{game_info['game_type']}',{game_info['game_score']});"
            print(query)
            return self.insert_data(query)
        else:
            return False

    def add_game_to_user(self,username,game_info):
        if all(key in game_info for key in ["game","level","user_score"]):
            query=f"INSERT INTO usergamerel(username,game,level,user_score) VALUES ('{username}','{game_info['game']}',{game_info['level']},{game_info['user_score']});"
            print(query)
            return self.insert_data(query)
        else:
            return False

    def get_user_info(self,username):

        query = "select * from users where username = '{}' ".format(username)
        result = self.execute_query(query)
        result = {"name":result[0][0],"surname":result[0][1],"username":result[0][2],"mail":result[0][3],"age":result[0][4]}
        return result

    def get_user_game_info(self, username):

        query = "select username,games.game,level,user_score,game_type from usergamerel,games where usergamerel.game=games.game and username = '{}' ".format(username)
        result = self.execute_query(query)

        result = {"username":result[0][0],"game":result[0][1],"level":result[0][2],"score":result[0][3],"gametype":result[0][4]}
        return result

    def get_user_game_interes(self):
        query="select usergamerel.username,games.game,usergamerel.level,usergamerel.user_score from games left join usergamerel on usergamerel.game=games.game;"
        result = self.execute_query(query)
        return result