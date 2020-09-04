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
default = {"config_fix", "config_mapping",
           "config_changable", "gamelist", " gaconnection"}


class SQL_CMD:
    def __init__(self, CMD, table=default):
        self.CMD = CMD
        self.table = table

    def Tables(self):
        if self.table == {}:
            print("empty talbe")
        else:
            print(f"show table = {self.table}")
        return self.table

    def execute(self):
        cur.execute(self.CMD)
        gamedb.commit()

    def close(self):
        cur.close()
        gamedb.close()


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
        super().close()


'''
    def join(self):

'''


class writeSQL(SQL_CMD):
    def __init__(self):
        self.CMD1 = f"insert into {self.Table}"
        self.CMD2 = f"values {self.item}"

        self.CMD3 = f"update {self.Table} set {self.column}={self.item} where {self.w1}={self.w2}"

    def insert(self, num=0, w1=None, w2=None, **new,):
        self.Table = self.table[num]
        self.item = item
        self.column = column
        if self.column != ():
            self.CMD = self.CMD1 + f"{self.column}" + self.CMD2
        else:
            self.CMD = self.CMD1 + self.CMD2
        super().execute()
        super().close()

    def update(self, item=(), column=(), num=1, w1=None, w2=None):
        self.item = item
        self.column = column
        self.Table = self.table[num]
        self.w1 = w1
        self.w2 = w2


#
'''
if __name__ == "__main__":
'''
