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

### 目前

- app
- remote_control
- server
  - server_monitor
  - SQL_connect
  - config_editor

### 待開發
- vm_placement_agr

## Portal API 呼叫參數

:::spoiler {state="open"} **start game /IP**
* gameID
* excutemode
* configfile
* **return**
    * gamestatus
    * IP
    * PID
::: 

:::spoiler {state="open"} **end game /End**
* excuteMode
* serverip
* pid
* **return**
    * gamestatus
:::

:::spoiler {state="open"} **add game /Add**
* gamename
* file zip type
:::

:::spoiler {state="open"} **add conf /Conf**
* gamename
* config 
  * [{ dictionary: null, gaColumn: "abc", value: true}, { dictionary: null, gaColumn: "134", value: "apple" }]
:::

## 啟動service 
1. 在VSCODE 啟動 `app.py` 檔，顯示0.0.0.0:5000即為運行中
or in CMD : `set FLASK_APP=main.py`，
`flask run --reload --debugger --host 0.0.0.0 --port 80`
2. 在runtime server端啟動`server_monitor.py`檔，以監控game server 

