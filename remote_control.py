import winrm
import socket
import time
import json
import logging
# import SQL_connect
FORMAT = "%(asctime)s %(levelname)s:%(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

_account = {"192.168.43.196":"RD"}
_pwd = {'RD':'Aa123456'}

exepath = "C:\\gaminganywhere-0.8.0\\bin\\"
configpath = "C:\\gaminganywhere-0.8.0\\bin\\config\\"
gamepath = "C:\\gamefile\\"

S_EVD = "start ga-server-event-driven config//"
S_PD = "start ga-server-periodic config//"
TER = "taskkill /F /IM "
class remote:
    def __init__(self, ip):
      self.ip = ip
      self.session = winrm.Session(f"{self.ip}",auth=(_account[self.ip] , _pwd[_account[self.ip]] ))
    def taskkill(self, exmode, pid):
      self.exmode = exmode
      self.killpid = pid
      self.cmd = self.session.run_cmd(f"taskkill /F /PID {self.killpid}" )
      if exmode == "periodic":
        self.session.run_cmd(f"taskkill /F /IM ga-server-periodic.exe" )
      
      return self.cmd.status_code

class client_socket:
  def __init__(self, hostip):
    PORT = 8000
    self.host = hostip
    try:
      self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.client.connect((self.host, PORT))
    except socket.gaierror:
      logging.error("socket error", exc_info=True)
      

  def control(self, **cmd):

    jsonobj = json.dumps(cmd)
    self.client.sendall(jsonobj.encode('utf-8'))
    logging.info("client send = ", jsonobj)
    msg = self.client.recv(1024).decode('utf-8')
    logging.info("client receive = ", msg)
    return json.loads(msg)
  
  def sendfile(self, filename):

    try:
      with open (filename, 'rb')as rb:
        logging.info("file opened")

        data = rb.read(1024)
        while (data):
          self.client.send(data)
          logging.info("client sending file ....")
          data = rb.read(1024)
        logging.info("send file done")
        self.client.send("done".encode('utf-8'))

      msg = self.client.recv(1024).decode('utf-8')
      logging.info("client receive = ", msg)
      return json.loads(msg)

    except:
      logging.error("file error", exc_info=True)




if __name__ == "__main__":

  A = client_socket("AndersonCJ_Chen")
  #A.client.send("done".encode('utf-8'))
  #api = {"gameId":123, "excutemode":"periodic"}
  #B = A.control(**api)
    
    
  C = A.sendfile("ABC.zip")

