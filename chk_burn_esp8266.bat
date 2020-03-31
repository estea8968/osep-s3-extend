@echo on
rem chcp 65001

del %TEMP%\burn_esp8266.bat
cd "C:\Program Files (x86)\osep-s3-extend\firmware\esp8266"
copy "c:\Program Files (x86)\osep-s3-extend\firmware\esp8266\burn_esp8266.bat" %TEMP%\burn_esp8266.bat
%TEMP%\burn_esp8266.bat %1
	