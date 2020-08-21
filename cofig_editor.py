import os

c = ".config"

configpath = "C:\\gaminganywhere-0.8.0\\bin\\config\\"
'''
class read_config:
    def __init__(self,name):
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
    def __init__(self,name):
        os.chdir(configpath)
        self.name = name
        f = open(self.name,'r')
    def scan_line(self,word):
        self.word = word
        line = 0
        for i in f:
            line +=1

    def scan_head(self,word):
        self.word = word
        line = 0
        for i in f:
            line +=1
            A = i.split("=",1)
            B = self.word.split("=",1)
            if A[0].rstrip() == B[0].rstrip():
                return line
            else:
                return 0


# write config data to local
class edit_config(find_match):
    def __init__(self,name):
        super().__init__
        f = open(self.name,'a')

# create new config file
class create_new:
    def __init__(self,name):
        f = open(self.name,'x')
    





 






# check match config
'''
os.chdir(configpath)
configfile = os.listdir("./")
for i in range(len(configfile)):
    if selectconfig == configfile[i]
    break

'''