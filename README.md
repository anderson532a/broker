# broker

###### tags: `intern`

## python (env)環境安裝CMD

`pip install virtualenv` : 安裝virtualenv

`virtualenv env`  : 創建新環境

`activate` : 啟動安裝環境

`pip list` : 顯示 pip 安裝目錄

`pip freeze > requirements.txt` : 環境 site-pkg 輸出

`pip install -r requirements.txt` : 安裝 site-pkg

for powershell 系統管理員:` Set-ExecutionPolicy RemoteSigned` 改 Y

for mysql 套件 : [mysqlclient](https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient)

### runtime server開啟winrm (for windows)


### debug

`pip debug --verbose` : python 相關版本確認


## .py檔案
``` graphviz
graph broker{
          nodesep=1.0
          
          node [color=Blue,fontname=Courie]
          Broker[color=black, shape=box, fontsize=26]
          Runtime_Server[color=black, shape=box,fontsize=26]
          
          Broker--app[label="API for web", fontcolor=darkgreen,fontsize=22]
          Broker--remote_control
          server_monitor--{SQL_connect config_editor}
          Runtime_Server--server_monitor
          {rank=same;app Runtime_Server}
          {rank=same;remote_control server_monitor}
          remote_control--server_monitor [label="socket connect", fontcolor=darkgreen,fontsize=22, color=darkorchid4, penwidth=3.0]


}
```

### 目前
- app
- remote_control
- server_monitor
- SQL_connect

### 待開發
- config_editor
- vm_placement_agr



## Portal API 呼叫參數
### 已經有的API
:::spoiler {state="open"} **start game**
* gameID
* excutemode
* configfile
* **return**
    * gamestatus
    * IP
    * PID
::: 

:::spoiler {state="open"} **end game**
* filename
* serverip
* pid
* **return**
    * gamestatus
:::

### 開發中API
:::spoiler {state="open"} **add game**
* 
:::


## 啟動service 
1. 在VSCODE 啟動 `app.py` 檔，顯示0.0.0.0:5000即為運行中
2. 在runtime server端啟動`server_monitor.py`檔，以監控game server 


## Flow Chart
```sequence
Title: Gaminganywhere 遊戲啟動流程
Note left of client: user登入
client->web portal: 選擇啟動遊戲
web portal-->broker: call start game API
Note right of broker: 選擇server
broker-->>game server: 啟動遊戲
game server-->>broker: 回傳IP、PID
broker-->web portal: API get IP、PID
Note over web portal: 寫入database
web portal->client: 回傳啟動game IP
game server->>client: Streaming
```

```sequence
Title: Gaminganywhere 遊戲結束流程
Note left of client: provider登入
client->web portal: 選擇結束遊戲
Note over web portal: 搜尋database
web portal-->broker: call end game API
Note left of broker: serverip, pid 
broker-->>game server: 遠端IP結束遊戲
game server-->>broker: 回傳成功與否
broker-->web portal: API get
Note over web portal: 更新database
```

