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
        newlist = []
        # can be opt algorithm
        for line in self.list:
            for k, v in self.change.items:
                if "=" in line:
                    check = line.strip().split(" = ")
                    if 'include' in check[0]:
                        pass
                    elif check[0] == k:
                        check[1] = v
                        line = " = ".join(check) + "\n"
                        logging.debug("editing : "+ f"{line}")

            newlist.append(line)
        writein = "".join(newlist)
        with open(self.name, 'w+') as fw:
            logging.debug("write mode w+, edit"+ f"{self.name}")
            fw.seek(0, 0)
            fw.write(writein)

    def comment_out(self):
        pass

# create new config file
class create_new(read_in):
    def __init__(self, N = 0):
        super().__init__
        etype = ("periodic", "event-driven")
        self.type = etype[N]
    def create(self):
        template = Path.cwd() / f"server/server.{self.type}.conf"
        self.confname = f"server.{self.name}.conf"
        newpath = configpath + self.confname
        try:
            with open(newpath, 'x') as fw:
                logging.debug("write mode x, create new"+ f"{self.name}")

        except FileExistsError:
            logging.error("file already exist!! try edit", exc_info=True)
    def add(self):
        pass



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