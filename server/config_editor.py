import os
import logging
from pathlib import Path
FORMAT = "%(asctime)s %(levelname)s:%(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

c = ".config"
configpath = "C:\\gaminganywhere-0.8.0\\bin\\config\\"

class read_in:
# read config file  
    def __init__(self, name, dir):
        if dir == 'C':
            os.chdir(configpath)
            logging.debug(f"{Path.cwd()}")
        else:
            logging.debug(f"{Path.cwd()}")
        self.name = name
        try:
            with open(self.name,'r') as fr:
                self.list = fr.readlines()
                logging.debug(f"{self.list}")

        except FileNotFoundError:
            logging.error("can't find", exc_info=True)


# write config data 
class edit_config(read_in):
    def __init__(self):
        super().__init__

    def find_match(self, **change):
        self.change = change
        # can be opt algorithm
        for line in self.list:
            for item in self.change:
                if "=" in line:
                    check = line.strip().split(" = ")
                    if check[0] == 'include':
                        pass
                    else:
                        pass

    def comment_out(self):
        pass

# create new config file
class create_new(read_in):
    def __init__(self, N = 0):
        super().__init__
        etype = ("periodic", "event-driven")
        self.type = etype[N]
    def new(self):
        template = Path.cwd() / f"server/server.{self.type}.conf"
        self.confname = f"server.{self.name}.conf"
        newpath = configpath + self.confname
        with open(newpath, 'w+') as fw:
            logging.debug("write mode w+")





# fw.write(f"# configuration for {self.name}"+"\n")

if __name__ == "__main__": # for testing
    test = create_new("ABC")
    test.new()







# check match config
'''
os.chdir(configpath)
configfile = os.listdir("./")
for i in range(len(configfile)):
    if selectconfig == configfile[i]
    break

'''