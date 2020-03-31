@echo on
rem chcp 65001
echo aaaaaaaa
del %TEMP%\burn_esp8266.bat
cd "C:\Program Files (x86)\s3-extend-tool\firmware\esp8266"
copy "c:\Program Files (x86)\s3-extend-tool\firmware\esp8266\burn_esp8266.bat" %TEMP%\burn_esp8266.bat
%TEMP%\burn_esp8266.bat %1
	