import MySQLdb

gamedb = MySQLdb.connect(host="compalgame.cvtg5m1xenqd.us-east-1.rds.amazonaws.com",
                       user="applecatcar", 
                       passwd="redorange",
                       db="gamedb"
                       )

cur = gamedb.cursor()

_table = "config_fix","config_mapping","config_changable"

class SQL_CMD:
    def __init__(self,CMD):
        self.CMD = CMD
    def execute(self):
        return cur.execute(self.CMD)

# read config info from MySQL
class readSQL(SQL_CMD):
    def __init__(self):
        self.CMD1 = f"select {self.item} from {self.Table}"
        self.CMD2 = f""

    def select(self, item, num = 1, w1 = None, w2 = None):
        self.item = item
        self.Table = _table[num]
        self.w1 = w1
        self.w2 = w2
        if self.w1 != None & self.w2 != None:
            self.CMD = self.CMD1 + f" where {self.w1}={self.w2}"
        else:
            self.CMD = self.CMD1
        super().execute()

    # def join(self):

class writeSQL(SQL_CMD):
    def __init__(self):
        self.CMD1 = f"insert into {self.Table}"
        self.CMD2 = f"values {self.item}"

        self.CMD3 = f"update {self.Table} set{self.colomn}={self.item} where {self.w1}={self.w2}"
    
    def insert(self, item = (), colomn = (), num = 1):
        self.Table = _table[num] 
        self.item = item
        self.colomn = colomn
        if self.colomn != ():
            self.CCMD = f"{self.colomn}"
            self.CMD = self.CMD1 + self.CCMD + self.CMD2
        else:
            self.CMD = self.CMD1 + self.CMD2
        super().execute()
    
   # def update(self):









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

