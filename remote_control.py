import winrm
import socket

account = {"192.168.43.196":"RD"}
pwd = {'RD':'Aa123456'}
class remote:
    def __init__(self, ip):
      self.ip = ip
      session = winrm.Session(f"{self.ip}",auth=(account[self.ip] , pwd[account[self.ip]] ))



'''
class client_socket:
  client = 

'''

