@ECHO OFF
%~d0
cd %~dp0
SET RUNCMD="%~dp0execute.bat"
SET RUN_USER=%USERNAME%
schtasks /Create /SC DAILY /MO 1 /ST 09:00 /TR "%RUNCMD%" /TN "Health" /F /RU "%RUN_USER%"
PAUSE
## 程序设置每天早上9点执行任务，你可根据自己的情况修改。请确保打卡时，网络畅通。
## 修改时间请修改/ST 后的值，格式为"HH:MM"