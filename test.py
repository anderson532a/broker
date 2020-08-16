import os
import socket


cmd = "ipconfig"
exIP = "8.8.8.8"
configpath = "C:\\gaminganywhere-0.8.0\\bin\\config"

'''

os.system()

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
