@echo off

REM 起動パラメータ
REM -n 名前
REM -p ポート2009(COOL)、2010(HOT)
REM -h ホストのIP

REM IPアドレスの取得
for /f "tokens=*" %%i in ('ruby -r socket -e "UDPSocket.open {|s| s.connect(\"127.0.0.0\", 7); puts s.addr.last }"') do set MY_IP=%%i

set %MY_IP%=192.168.3.16

REM 引数に応じた動作を実行
if "%1" == "c" (
    echo COOL Run
    python KeyInputDo.py -n COOL -p 2009 -h %MY_IP%
) else if "%1" == "h" (
    echo HOT Run
    python KeyInputDo.py -n HOT -p 2010 -h %MY_IP%
) else (
    echo 引数が設定されていません: %1
    echo 実行方法: %0 {c|h}
    exit /b 1
)
