import os
import logging
from pathlib import Path
import SQL_connect

c = ".config"

configpath = "C:\\gaminganywhere-0.8.0\\bin\\config\\"

class read_in:
# read config file  
    def __init__(self, name):
        os.chdir(configpath)
        logging.debug(f"now path : {Path.cwd()}")
        self.name = f"server.{name}.conf"
        try:
            with open(self.name,'r') as fr:
                self.list = fr.readlines()
                logging.info("read in success")
                # logging.debug(self.list)

        except FileNotFoundError:
            logging.error("can't find", exc_info=True)


# write config data 
class edit_config(read_in):
    def __init__(self, name):
        super().__init__(name)

    def match_modify(self, **change):
        k = change["GAcolumn"]
        if "newValue" in change:
            v = str(change["newValue"])
        else:
            v = str(change["value"])
        newlist = []
        logging.info(f"write key : {k}; value : {v}")
        A = True
        for line in self.list:
            if k in line: # find match
                if "=" in k:
                    logging.info("- config comment -")
                    if v == "False":
                        line = "# "+line
                    else:
                        line = line.strip("#")
                        line = line.strip()
                elif '#' in v:
                    # commet something
                    logging.info("- config comment -")
                    pass 
                else:
                    logging.info("- config modify -")
                    edit = line.split()
                    logging.debug(edit)
                    edit[2] = v
                    line = ' '.join(edit) + '\n'
                A = False
            newlist.append(line)

        if A == True:
            logging.info("- config append -")
            other = " = ".join([k, v])
            newlist.append(other)
        
           
        writein = "".join(newlist)
        # logging.debug("write in :" + f"{writein}")
        try:
            with open(self.name, 'w+') as fw:
                logging.debug("write mode w+, edit " + f"{self.name}")
                fw.seek(0, 0)
                fw.write(writein)
                logging.info("write in success")
                return True
        except:
            logging.error("something wrong in write in", exc_info=True)
            return False




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
    A = {"GAcolumn": "include = common/server-common.conf", "value": 'True'}
    B = {"GAcolumn": "enable-audio", "value": 'false'}
    C = {"GAcolumn": "video-fps", "value": 50}
    test = edit_config("test")
    test.match_modify(**C)
'''

