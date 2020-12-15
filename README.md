# Broker

###### tags: `intern`

## broker 環境設定
* **python CMD (env)安裝**

`pip install virtualenv` : 安裝virtualenv

`virtualenv env`  : 創建新環境

`activate` : 啟動安裝環境 *(至activate檔所在file)*

`pip list` : 顯示 pip 安裝目錄

`pip freeze > requirements.txt` : 環境 site-pkg 輸出成requirements.txt

`pip install -r requirements.txt` : 從requirements.txt安裝 site-pkg

for powershell 系統管理員:` Set-ExecutionPolicy RemoteSigned` 改 Y

for python mysql 套件 : [mysqlclient](https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient)
找對應版本安裝
* **python debug**

`pip debug --verbose` : python 相關版本確認

### Runtime Server開啟winrm (for upload game function)

[windows SSH 設定](https://medium.com/@fortunatemaker2603/ssh-%E9%81%A0%E7%AB%AF%E9%80%A3%E7%B7%9A%E5%9B%9E%E5%AE%B6%E4%B8%AD%E7%9A%84-windows-%E9%9B%BB%E8%85%A6-7e5267ae1e93)
#### winrm CMD
`winrm enumerate winrm/config/listener` : 確認是否開啟winrm
```cmd
設定winrm
winrm quickconfig
winrm set winrm/config/service/auth '@{Basic="true"}'
winrm set winrm/config/service '@{AllowUnencrypted="true"}'
```
參考來源[python winrm 連接windows](https://www.itread01.com/content/1531822819.html)

### win系統其他issue
* port 占用
1. `netstat -a -b` : 檢視port的使用情況
2. `netstat -ano | findstr 0.0:3000` : 查port 號 3000 的pid 
3. `taskkill /f /PID 7216` : 刪除pid 7216

參考來源 
[Windows 如何找到佔用 port 的程式?](https://blog.qoding.us/2011/07/windows-how-to-find-out-which-application-is-using-what-port/)


* 固定路徑

**遊戲檔案** : C:\\gamefile\\  
**gaminganywhere** : C:\\gaminganywhere-0.8.0\\bin\\  
**config file** : C:\\gaminganywhere-0.8.0\\bin\\config\\

:::spoiler PC 固定IP設定
1. 連線wifi
2. ipconfig 確認IP位址是否正確
![](https://i.imgur.com/gQmDEAB.png)
3. 若不是192.168.43.196 先打開"更改IP.BAT"修改gateway 與dns
![](https://i.imgur.com/oKsQNs0.png)
![](https://i.imgur.com/RgyIgAN.png)

4. 最後右鍵"以系統管理員執行"
![](https://i.imgur.com/5WUMKoy.png)
5. 需要回復IP則一樣右鍵"回復.bat"
6. *bat檔在notebook 
:::

## .py檔案
### Component Diagram
```plantuml
package "broker" {
  [app.py] as AP
  [remote_control.py] as RC
}

package "server" {
  [config_editor.py] as CE
  [server_monitor.py] as SM
  [SQL_connect.py] as SC
}

database "MySQL"  {
    frame "table"{
        [gaconnection] as DB
    }

}
node "WEB" as WB
interface "HTTP" as N1
interface "socket" as N3
interface "SFTP" as N2
interface "winrm" as N4
node "gaminganywhere server" as GA
 
 
WB . N1
N1 .. AP

SM .. DB : SQL CMD
AP --> N2
N2 --> SM
RC <. AP
SC <. SM
CE <.left. SM
AP -- N3
N3 -- SM 
AP --> N4
N4 --> SM
SM ..> GA : WIN CMD
note right of N2 
    upload game gateway
    *add game
    end note
note right of N3 
    API data
    (json type)
    *start game
    *edit config
    end note

note right of N4 
    Command control server
    *end game
    end note

```

### 已完成
- `app.py` 處理接收 web 端http request 
- `remote_control.py` : 遠端game server & 對server_monitor建立各種連線
- `server_monitor.py` : 啟動遊戲 & 結束遊戲 & 接收上傳遊戲
- `SQL_connect.py` : 連接資料庫
- `config_editor.py` : 創立 & 更改config檔

### 待開發
- `selectserver_algorithm.py` : 以統計數據選擇最好game server
- `server_monitor.py` : 監控系統資源(cpu、stdout...等)

### Class Diagram
#### broker
```plantuml

package remote_control.py{

class remote
class client_socket
class SftpClient

}

package app.py{

class gameserver_CMD
class route_IP
class route_End
class route_Add
class route_Conf
gameserver_CMD <|.. client_socket
route_Add <|.. SftpClient
route_End <|.. remote
}
```
#### server
```plantuml
package config_editor.py{
class read_in
class edit_config
class create_new
read_in <|-- edit_config
read_in <|-- create_new
}

package SQL_connect.py{
class SQL_CMD
class readSQL
class writeSQL
SQL_CMD <|-- readSQL
SQL_CMD <|-- writeSQL
}

package server_monitor.py{
class game_status
class excute_game
class sync_DB
class Handler
interface BaseRequestHandler
BaseRequestHandler <|-- Handler
sync_DB <|. readSQL
sync_DB <|. writeSQL
Handler <|.. edit_config
Handler <|.. create_new
}



```
### 元件情境描述(broker 端)
:::spoiler 開啟遊戲 & 觀看遊戲
```plantuml
start 
:route(/IP);
note right :API get method
:gameserver_CMD;
note right :socket client send "start game"
:Handler;
note right :socket server received
:excute_game;
:route(/IP);
note right :return game info
stop
```
:::

:::spoiler 結束遊戲
```plantuml
start 
:route(/End);
note right :API get method
:remote;
note right :remote server kill game
:gameserver_CMD;
note right :socket client send "clean server status"
:Handler;
note right :socket server idle
:route(/End);
note right :return end message
stop
```
:::

:::spoiler 新增遊戲
```plantuml
start 
:route(/Add);
note right :API post method
:gameserver_CMD;
note right :socket client send "new game config"
:Handler;
note right :socket server create new config file
:SftpClient;
note right :upload zip file
:gameserver_CMD;
note right :socket client send "finish upload"
:Handler;
note right :socket server unzip file
:route(/Add);
note right :return status message
stop
```
:::

:::spoiler 更改conf檔
```plantuml
start 
:route(/Conf);
note right :API post method
:gameserver_CMD;
note right :socket client send "edit config file"
:Handler;
note right :socket server received
:edit_config;
note right :find column to edit
:route(/Conf);
note right :return status message
stop
```
:::

## 由 Portal 呼叫API參數
API文件 : [Postman API document](https://speeding-trinity-458849.postman.co/collections/12905825-e66ea83a-d7b1-49a4-a208-982e5a3ab819?version=latest&workspace=728006cb-e97c-49e7-8b0e-7b17a245c54c#4bf22223-79bb-4a85-84b8-8032aa59d86f)
:::spoiler {state="open"} **start game** (get)
* **parameter**
    * gameId
    * excuteMode
    * configfile
* **return**
    * gamestatus
    * IP
    * PID
::: 

:::spoiler {state="open"} **end game** (get)
* **parameter**
    * excuteMode
    * serverip
    * pid
* **return**
    * gamestatus
:::

:::spoiler {state="open"} **add game** (post)
* **parameter**
    * gamename
* **body**
    * zip file
* **return**
    * status
:::

:::spoiler {state="open"} **config file** (post)
* **body**
    * gamename
    * **config** (主要會用到)
        * dictionary
        * gaColumn
        * value or newValue
* **return**
    * status

:::
## 啟動程式 service 
一. VSCODE(for測試)
1. 在VSCODE 啟動 `app.py` 檔，顯示0.0.0.0:5000即為運行中
2. 在runtime server端啟動`python server_monitor.py`檔，以監控game server 

二. win terminal

在broker 目錄下
```CMD
set FLASK_APP=app.py
set FLASK_DEBUG=true
flask run --reload --debugger --host 0.0.0.0
```
## 注意事項
* git : https://github.com/anderson532a/broker
* 目前最後版本已合併master，dev1 為測試功能用途分支
* 固定位置、路徑、IP 在程式裡以 #%# 標記
* server game 狀態以DB為準，若開啟遊戲後未馬上寫入DB則會被關閉(時間差有機會)

## 其他資料

### [觀看模式demo](https://drive.google.com/file/d/1YzknRzJSwJtoqhu5RMYQPSjuPr1rR0IL/view?usp=sharing)


### [GA server](hackmd.io/aJ1q1xhvRGyZmkAZ1c0M5A?view)
<iframe width="100%" height="300" src="https://hackmd.io/aJ1q1xhvRGyZmkAZ1c0M5A?view"  frameborder="0"></iframe>


