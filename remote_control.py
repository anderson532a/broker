import winrm
import socket
import time

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
      session = winrm.Session(f"{self.ip}",auth=(_account[self.ip] , _pwd[_account[self.ip]] ))

class client_socket:
  def __init__(self, hostname):
    PORT = 8000
    self.host = hostname
    try:
      self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.client.connect((self.host, PORT))
    except socket.gaierror:
      print()

  def repeat(self, msg):
    self.msg = msg
    CLMES = f"{self.msg}"
    self.client.sendall(CLMES.encode('utf-8'))
    rece = self.client.recv(1024)
    print(str(rece, encoding='utf-8'))    


if __name__ == "__main__":
    A = client_socket("AndersonCJ_Chen")
    for i in range(20):
      A.repeat(i)
      time.sleep(1)
      i += 1
