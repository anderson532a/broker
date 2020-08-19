import MySQLdb

gamedb = MySQLdb.connect(host="compalgame.cvtg5m1xenqd.us-east-1.rds.amazonaws.com",
                       user="applecatcar", 
                       passwd="redorange",
                       db="gamedb"
                       )

cursor = gamedb.cursor()

# write config name to "gamelist"

# write config data to "CONFIG"
class create_table():
    def __init__(self,table,):
        self.table = table

    def set_data(self,):

    def SQL_excute(self):


# read config to excute game

