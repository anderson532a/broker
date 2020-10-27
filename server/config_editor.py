import os
import logging
from pathlib import Path
import SQL_connect

c = ".config"
configpath = "C:\\gaminganywhere-0.8.0\\bin\\config\\"

class read_in:
# read config file  
    def __init__(self, name, *dir):
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
    def __init__(self, name, *dir):
        super().__init__(name, *dir)

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
        logging.debug("write in :" + f"{writein}")
        try:
            with open(self.name, 'w+') as fw:
                logging.debug("write mode w+, edit"+ f"{self.name}")
                fw.seek(0, 0)
                fw.write(writein)
                return True
        except:
            logging.error("something wrong")
            return False

    def comment_out(self):
        pass

# create new config file
class create_new:
    def __init__(self, name, mode = "periodic"):
        self.name = name
        self.mode = mode
        
    def create(self):
        template = Path.cwd() / f"server.{self.mode}.conf"
        confname = f"server.{self.name}.conf"
        newpath = configpath + confname
        try:
            with open(newpath, 'x') as fx:
                logging.debug("write mode x, create name :"+ f"{self.name}")
                fx.write(template.read_text())
                fx.seek(0,0)
                fx.write(f"# configuration for {self.name}" + "\n")
                logging.info("new create success")
                return "TRUE"
        except FileExistsError:
            logging.error("file already exist", exc_info=True)
            return "FALSE"


'''
if __name__ == "__main__": # for testing
    test = create_new("ABC")
    test.create()
'''
