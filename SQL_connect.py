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
        self.CMD1 = f"insert into {self.Table} ({self.columns})"
        self.CMD2 = f"values ({self.values})"

        self.CMD3 = f"update {self.Table} {self.set} where {self.w1}={self.w2}"

    def insert(self, num=0, *onval,**newitem):
        self.Table = self.table[num]
        self.new = newitem
        self.val = onval
        if self.new != {}:
            self.items = self.new.items()
            self.values = ""
            self.columns = ""
            for key, val in self.items:
                if self.values == "":
                    self.columns = f"{key}"
                    self.values = f"{val}"
                else:
                    K = f", {key}"
                    V = f", {val}"
                    self.values = self.values + V
                    self.columns = self.columns + K
            self.CMD = self.CMD1  + self.CMD2
        elif self.val != ():
            pass
        else: # error
            pass

        super().execute()
        super().close()

    def update(self, num=1, w1=None, w2=None, **newitem):
        self.new = newitem
        self.Table = self.table[num]
        self.w1 = w1
        self.w2 = w2
        if self.new != {}:
            self.items = self.new.items()
            CCMD = ""
            for key, val in self.items:
                if CCMD == "":
                    CCMD = f"{key}={val}"
                else:
                    ST = f", {key}={val}"
                    CCMD = CCMD + ST
            self.set = f"set {CCMD}"
            self.CMD = self.CMD3
        else:
            self.CMD =  self.CMD3

#
'''
if __name__ == "__main__":
'''
