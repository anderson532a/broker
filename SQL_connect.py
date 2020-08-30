import MySQLdb
'''old data
gamedb = MySQLdb.connect(host="compalgame.cvtg5m1xenqd.us-east-1.rds.amazonaws.com",
                       user="applecatcar", 
                       passwd="redorange",
                       db="gamedb"
                       )
'''
gamedb = MySQLdb.connect(host="localhost",
                         user="root",
                         passwd="Aa123456",
                         db="gamedb"
                         )

cur = gamedb.cursor()
default = {"config_fix", "config_mapping", "config_changable", "gamelist"}
class SQL_CMD:
    def __init__(self, CMD, table = default):
        self.CMD = CMD
        self.table = table

    def Tables(self):
        if self.table == {}:
            print("empty talbe")
        else:
            print(f"show table = {self.table}")
        return self.table

    def execute(self):
        return cur.execute(self.CMD)

# read info from MySQL

class readSQL(SQL_CMD):
    def __init__(self):
        self.CMD1 = f"select {self.item} from {self.Table}"

    def select(self, item, num=0, w1=None, w2=None):
        self.item = item
        self.Table = self.table[num]
        self.w1 = w1
        self.w2 = w2
        if self.w1 != None & self.w2 != None:
            self.CMD = self.CMD1 + f" where {self.w1}={self.w2}"
        else:
            self.CMD = self.CMD1
        super().execute()


'''
    def join(self):

'''

class writeSQL(SQL_CMD):
    def __init__(self):
        self.CMD1 = f"insert into {self.Table}"
        self.CMD2 = f"values {self.item}"

        self.CMD3 = f"update {self.Table} set{self.column}={self.item} where {self.w1}={self.w2}"

    def insert(self, item=(), column=(), num=0):
        self.Table = self.table[num]
        self.item = item
        self.column = column
        if self.column != ():
            self.CCMD = f"{self.column}"
            self.CMD = self.CMD1 + self.CCMD + self.CMD2
        else:
            self.CMD = self.CMD1 + self.CMD2
        super().execute()

    def update(self, item=(), column=(), num=1, w1=None, w2=None):
        self.item = item
        self.column = column
        self.Table = self.table[num]
        self.w1 = w1
        self.w2 = w2


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
