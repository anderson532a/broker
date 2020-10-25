import MySQLdb
import logging

gamedb = MySQLdb.connect(host="localhost",
                         user="server",
                         passwd="jasmine",
                         db="gamedb"
                         )
gamedb.ping(True)
cur = gamedb.cursor()
default = ("gaconnection", "config_data", "gameslist")
FORMAT = "%(asctime)s -%(levelname)s : %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

class SQL_CMD:
    def __init__(self, CMD = "", table = default):
        self.CMD = CMD
        self.table = table

    def execute(self):
        cur.execute(self.CMD)
        
    def close(self):
        cur.close()
        gamedb.close()

# read info from MySQL

class readSQL(SQL_CMD):
    def __init__(self):
        super().__init__()

    def select(self, *Item, num=0, **condi):
        self.Item = ', '.join(i for i in Item)
        self.Table = self.table[num]
        self.condi = condi
        self.CMD1 = f"select {self.Item} from {self.Table}"
        try:
            if self.condi != {} :
                for k, v in self.condi.items():
                    self.CMD = self.CMD1 + f" where {k}=\"{v}\""
                    logging.debug(f"CMD : {self.CMD}")
            else:
                self.CMD = self.CMD1
                logging.debug(f"CMD : {self.CMD}")
            super().execute()
            read = cur.fetchall()
            # for i in read:
                # logging.debug(f"{i}")  # tuple with tuple
            return read
        except:
            super().close()

    def join(self):
        pass

class writeSQL(SQL_CMD):
    def __init__(self):
        super().__init__()
        
    def insert(self, num=0, **newitem):
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
            self.CMD1 = f"insert into {self.Table} ({self.columns})"
            self.CMD2 = f"values ({self.values})"
            self.CMD = self.CMD1  + self.CMD2
            super().execute()
            gamedb.commit()
        except:
            logging.error("something wrong", exc_info=True)
            # cur.execute("SET SQL_SAFE_UPDATES=0")
            super().close()

# newitem : set ; col、val :  where
    def update(self, num = 0, col = "", val = "", **newitem):
        self.new = newitem
        self.Table = self.table[num]
        self.col = col
        self.val = val
        try:
            self.items = self.new.items()
            CCMD = ""
            for key, val in self.items:
                if CCMD == "":
                    CCMD = f"{key}=\"{val}\""
                else:
                    ST = f", {key}=\"{val}\""
                    CCMD = CCMD + ST
            self.set = CCMD
            self.CMD = f"update {self.Table} set {self.set} where {self.col}=\"{self.val}\""
            logging.debug(f"CMD : {self.CMD}")
            super().execute()
            gamedb.commit()
            logging.info("update commit sucessful")
        except:
            logging.error("something wrong", exc_info=True)
            #cur.execute("SET SQL_SAFE_UPDATES=0")
            super().close()
            

    def delete(self):
        pass


if __name__ == "__main__":
    A = readSQL()
    B = writeSQL()
    results = A.select("gamename", "pid", "status", **{"serverIp":"192.168.43.196"})
    print(type(results), len(results))
    ppid = ''
    T = list(zip(*results))
    print(T[2])
    if 'TRUE' not in T[2]:
        print("FFF")


        
                

        
        