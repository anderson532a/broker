import os
import SQL_connect
import logging
from pathlib import Path
import shutil

c = ".config"

configpath = "C:\\gaminganywhere-0.8.0\\bin\\config\\"

'''
class read_config:
    def __init__(self, name):
        os.chdir(configpath)
        self.name = name
        f = open(self.name,'r')
    def read(self,num = None):
        self.num = num
        if nself.num != None:
            conf = f.read(self.num)
        else:
            conf = f.readlines()
        return conf
    def close(self):
        f.close()
'''
class find_match:
# read config file  
    def __init__(self, name):
        os.chdir(configpath)
        self.name = name
        self.f = open(self.name,'r')

    def scan_line(self, word):
        self.word = word
        line = 0
        for i in self.f:
            line +=1
            if i == self.word:
                return line    
        return 0

    def scan_head(self, word):
        self.word = word
        line = 0
        for i in self.f:
            line +=1
            A = i.split("=",1)
            B = self.word.split("=",1)
            if A[0].rstrip() == B[0].rstrip():
                return line
            else:
                return 0
    def close(self):
        self.f.close()

# write config data to local
class edit_config(find_match):
    def __init__(self, name):
        super().__init__
        self.f = open(self.name,'a+')

# create new config file
class create_new:
    def __init__(self, name, N = 0):
        etype = ("periodic", "event-driven")
        self.name = name
        self.type = etype[N]
    def new(self):
        periotem = Path.cwd() / f"server.{self.type}.conf"
        self.confname = f"server.{self.name}.conf"
        shutil.copyfile(periotem, configpath + self.confname)
        if self.type == "event-driven":
            pass
        else:
            pass


    



if __name__ == "__main__": # for testing
    pass








# check match config
'''
os.chdir(configpath)
configfile = os.listdir("./")
for i in range(len(configfile)):
    if selectconfig == configfile[i]
    break

'''