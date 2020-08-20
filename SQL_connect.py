import MySQLdb

gamedb = MySQLdb.connect(host="compalgame.cvtg5m1xenqd.us-east-1.rds.amazonaws.com",
                       user="applecatcar", 
                       passwd="redorange",
                       db="gamedb"
                       )

cur = gamedb.cursor()

_table = "config_fix","config_mapping","config_changable"


## read config info from MySQL

class SQL_CMD():
    def __init__(self,CMD):
        self.CMD = CMD
    def get(self):
        return cur.execute(self.CMD)



class readSQL:
    def __init__(self):
        self.CMD1 = f"select {self.item} from {self.Table}"
        self.CMD2 = f""

    def excute(self, item, num, where = None):
        self.item = item
        self.num = num
        self.where = where
        if self.where != None:






# create config for new game

'''

'''

# user edit config option

'''
cur.close()
gamedb.commit()
gamedb.close()
'''

# default local setting to SQL 



# check SQL & local data metch 

