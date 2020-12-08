import winrm
import socket
from paramiko import Transport, SFTPClient
import logging, json, time
FORMAT = "%(asctime)s -%(levelname)s : %(message)s"
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
            self.session.run_cmd(TER + "ga-server-periodic.exe")
        return self.cmd.status_code

class client_socket:

    def __init__(self, hostip):
        self.connection(hostip)
    
    @classmethod
    def connection(cls, hostip):
        PORT = 8000
        cls.host = hostip
        try:
            cls.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cls.client.connect((cls.host, PORT))
        except socket.gaierror:
            logging.error("socket error", exc_info=True)

    @classmethod
    def jsncontrol(cls, **cmd):
        sndg = json.dumps(cmd)
        logging.info(f"client send = {sndg}")
        cls.client.sendall(sndg.encode('utf-8'))
        msg = cls.client.recv(2048).decode('utf-8')
        logging.info(f"client receive = {msg}")
        return json.loads(msg)
    
   
        



# 大檔案傳輸速度不佳
def sendfile(self, filename, newname):
    self.client.send("sendfile".encode('utf-8'))
    R = self.client.recv(2048).decode('utf-8')
    if R == "ready":
        self.client.send(f"{newname}".encode('utf-8'))
    time.sleep(2)
    try:
        with open (filename, 'rb')as rb:
            logging.info("file opened")
        while True:
            data = rb.readline(4096)
            if not data:
                break
            self.client.send(data)
            #logging.debug(f"data : {data}")
            logging.info("client sending file ....")
            
        self.client.send("done".encode('utf-8'))
        # self.client.shutdown(socket.SHUT_WR)
        logging.info("send file done")

        msg = self.client.recv(1024).decode('utf-8')
        logging.info(f"client receive : {msg}")
        return msg

    except:
        logging.error("file error", exc_info=True)


class SftpClient:
    _connection = None

    def __init__(self, ip):
        self.ip = ip
        self.port = 22
        self.username = _account[self.ip]
        self.password = _pwd[_account[self.ip]] 
        self.create_connection(self.ip, self.port,
                                self.username, self.password)

    @classmethod
    def create_connection(cls, host, port, username, password):
        transport = Transport(sock=(host, port))
        transport.connect(username=username, password=password)
        cls._connection = SFTPClient.from_transport(transport)

    @staticmethod
    def size_convert(byte):
        BB = float(byte)
        KB = float(1024)
        MB = float(KB ** 2)
        GB = float(KB ** 3)

        if KB <= BB < MB:
            return round(BB/KB, 2)
        elif MB <= BB < GB:
            return round(BB/MB, 2)
        elif GB <= BB:
            return round(BB/GB, 2)
        else:
            return BB

    @classmethod
    def uploading_info(cls, uploaded_file_size, total_file_size, UP_buffer = 0):
        UP = cls.size_convert(uploaded_file_size)
        TO = cls.size_convert(total_file_size)
        if UP_buffer < int(UP):
            UP_buffer = UP
            logging.info('uploaded_file_size : {} total_file_size : {}'.
                        format(UP, TO))

    def upload(self, filename, name):

        local_path = 'C:\\Users\\RD\\Desktop\\broker\\' + f"{filename}"
        remote_path = gamepath + f"{name}"
        self._connection.put(localpath=local_path,
                            remotepath=remote_path,
                            callback=self.uploading_info,
                            confirm=True)

    def close(self):
        logging.info("upload finish")
        self._connection.close()


'''
if __name__ == "__main__":


    # A = client_socket("AndersonCJ_Chen")
    # A.client.send("done".encode('utf-8'))
    #api = {"gameId":123, "excutemode":"periodic"}
    #B = A.control(**api)

    # C = A.sendfile("Screen Shot 2020-10-24 at 11.01.26 AM.zip")
    hostname = socket.gethostname()
    IPadrr = socket.gethostbyname(hostname)
    user = 'RD'
    password = 'Aa123456'
    sclient = SftpClient(IPadrr)
    sclient.upload('')
    sclient.close()
    '''