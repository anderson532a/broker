import MySQLdb

gamedb = MySQLdb.connect(host="compal.cvtg5m1xenqd.us-east-1.rds.amazonaws.com",
                       user="admin", 
                       passwd="applebanana",
                       db="game"
                       )

cursor = gamedb.cursor()
cursor.execute("SELECT VERSION()") 
'''
print("Database version : %s " % cursor.fetchone())
'''

# write config name to "gamelist"

# write config data to "CONFIG"

# read config to excute game

