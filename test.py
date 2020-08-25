import os
import socket
import sys
import MySQLdb
import cofig_editor

cmd = "C:\\gamefile\\FPS_Game\\FPS_Game\\FPS_Game.exe"
exIP = "8.8.8.8"
configpath = "C:\\gaminganywhere-0.8.0\\bin\\config\\server.neverball.conf"

# os.system()

d = os.popen(cmd)
print(d.read())
os.getcwd()
A = os.getcwd()
'''
# os.chdir("C:\\")
os.system(cmd)
A = os.getcwd()
os.chdir(configpath)

B = os.listdir("./")

print(A)
print(B[0])
print(type(B), len(B))

for i in range(len(B)):
    C = os.path.splitext(B[i])[0]
    print(C, type(C))
'''
# print(sys.path)
'''
gamedb = MySQLdb.connect(host="compalgame.cvtg5m1xenqd.us-east-1.rds.amazonaws.com",
                       user="applecatcar", 
                       passwd="redorange",
                       db="gamedb"
                       )
cursor = gamedb.cursor()
'''
A = '*'
B = "config_fix"
C = "name"
D = ()
# "select * from config_fix"
# cursor.execute("use gamedb") 
print(f"select {A} from {B}" + f" where {C} = {D}")
# cursor.execute(f"select {A} from {B}") 
'''
r = open(configpath,'r')
j = 0
for i in r:
    j += 1
    print(j)
    A = i.split("=",1)
    print(A[0].rstrip())
# x = open(configpath,'x')
'''


'''
cursor.execute("SELECT VERSION()") 

B = cursor.fetchone()
for i in range(len(B)):
    if B[i] == None:
        B = B[:i]
        break

print(type(B))
print( f"{B}")

'''

 # SQL = SQL_connect()

