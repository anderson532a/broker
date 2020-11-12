import os
import logging
from pathlib import Path
import SQL_connect

c = ".config"

configpath = "C:\\gaminganywhere-0.8.0\\bin\\config\\"
diclist = ['[core]\n', '[video]\n', '[audio]\n', '[filter]\n',  '[ga-server-event-driven]\n', '[ga-server-periodic]\n']
class read_in:
# read config file  
    def __init__(self, name, path=0):
        if path == 0:
            os.chdir(configpath)
        logging.debug(f"now path : {Path.cwd()}")
        self.name = f"server.{name}.conf"
        try:
            with open(self.name,'r') as fr:
                self.list = fr.readlines()
                logging.info("read in success")
                logging.debug(self.list)

        except FileNotFoundError:
            logging.error("can't find", exc_info=True)


# write config data 
class edit_config(read_in):
    def __init__(self, name):
        super().__init__(name)

    def match_modify(self, **change):
        d = change['dictionary']
        k = change["gaColumn"]
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
            newlist = self.list
            logging.info("- config append -")
            dstr = d + "\n"
            other = " = ".join([k, v]) + "\n"
            if dstr in self.list:
                logging.info("have dictionary")
                num1 = diclist.index(dstr) + 1
                logging.info(f"diclist {d} next number:{num1}")
                locate = self.list.index(diclist[num1]) - 2
                newlist.insert(locate, other)

            else:
                logging.info("miss dictionary")
                num1 = diclist.index(dstr) + 1
                logging.info(f"diclist {d} next number:{num1}")
                for i in range(num1, 6):
                    if diclist[i] in self.list:
                        num2 = i
                        break
                locate = self.list.index(diclist[num2]) - 1
                newlist.insert(locate, "\n")
                newlist.insert(locate + 1, dstr)
                newlist.insert(locate + 2, other)
           
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
class create_new(read_in):
    def __init__(self, name, mode = "periodic"):
        self.name = name
        self.mode = mode
        
    def create(self):
        template = Path.cwd() / f"server.{self.mode}.conf"
        confname = f"server.{self.name}.conf"
        newpath = configpath + confname
        super().__init__(self.mode, path=1)
        try:
            with open(newpath, 'x') as fx:
                logging.debug("write mode x, create name :"+ f"{self.name}")
                self.list[1] = '# configuration for' + f"{self.name}" + '\n'
                logging.debug(f'new create: {self.list}')
                writein = "".join(self.list)
                fx.seek(0, 0)
                fx.write(writein)
                logging.info("new create success")
                return "TRUE"
        except FileExistsError:
            logging.error("file already exist", exc_info=True)
            return "FALSE"


'''
if __name__ == "__main__": # for testing
    
    A = {'dictionary':"[core]", "gaColumn": "include = common/server-common.conf", "value": 'True'}
    B = {'dictionary':"[ga-server-periodic]", "gaColumn": "enable-audio", "value": 'false'}
    C = {'dictionary':"[video]", "gaColumn": "video-fps", "value": 50}
    test = edit_config("tttttt")
    test.match_modify(**C)
    
    create_new('ABC').create()
    
'''