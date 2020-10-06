import MySQLdb

gamedb = MySQLdb.connect(host="localhost",
                         user="server",
                         passwd="jasmine",
                         db="gamedb"
                         )

cur = gamedb.cursor()
default = ("gaconnection", "config_data", "gameslist")


class _SQL_CMD:
    def __init__(self, CMD, table = default):
        self.CMD = CMD
        self.table = table

    def execute(self):
        cur.execute(self.CMD)
        
    def close(self):
        cur.close()
        gamedb.close()

# read info from MySQL

class readSQL(_SQL_CMD):
    def __init__(self):
        self.CMD1 = f"select {', '.join(i for i in self.item)} from {self.Table}"

    def select(self, num=0, *item, **condi):
        self.item = item
        self.Table = self.table[num]
        self.condi = condi
        try:
            if self.condi != {} :
                for k, v in self.condi.items():
                    self.CMD = self.CMD1 + f" where {k}={v}"
            else:
                self.CMD = self.CMD1
            super().execute()
            read = cur.fetchall()
            return read
        except:
            pass
        finally:
            super().close()

'''
    def join(self):

'''

class writeSQL(_SQL_CMD):
    def __init__(self):
        self.CMD1 = f"insert into {self.Table} ({self.columns})"
        self.CMD2 = f"values ({self.values})"

        self.CMD3 = f"update {self.Table} set {self.set} where {self.col}={self.val}"

    def insert(self, num=0,  **newitem):
        self.Table = self.table[num]
        self.new = newitem
        try:
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
            super().execute()
            gamedb.commit()
        except:
            pass
        finally:
            super().close()

    def update(self, num=1, col="", val="", **newitem):
        self.new = newitem
        self.Table = self.table[num]
        try:
            self.items = self.new.items()
            CCMD = ""
            for key, val in self.items:
                if CCMD == "":
                    CCMD = f"{key}={val}"
                else:
                    ST = f", {key}={val}"
                    CCMD = CCMD + ST
            self.set = CCMD
            self.CMD = self.CMD3
            super().execute()
            gamedb.commit()
        except:
            pass
        finally:
            super().close()



if __name__ == "__main__":
    cur.execute("SELECT * FROM gaconnection")
    results = cur.fetchall()
    print(type(results))
    for i in results:
        print(i[4])
