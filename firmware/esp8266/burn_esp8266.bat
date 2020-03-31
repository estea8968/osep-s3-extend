@echo off
chcp 65001
cd "C:\Program Files (x86)\s3-extend-tool\firmware\esp8266"

:start
rem ##set /p echo u_choice="choice (1:burn firmware 2:set wifi ssid password): "

choice /d 2 /t 100 /c 123 /m "choice選擇 1.burn firmware燒錄韌體 2.set wifi ssid password設定無線網路. 3. end離開 "
if errorlevel 3 goto end
if errorlevel 2 goto ssid
if errorlevel 1 goto burn

:burn
 	esptool.py --port %1 --baud 460800 write_flash --flash_size=detect -fm dio 0 esp8266-20191220-v1.12.bin
	ampy --port %1 put main.py
	ampy --port %1 put esp_8266_min.py 
	echo "esp8266 firmware burn complete韌體燒錄完成"
	echo "input any key to continue.按任意鍵繼續"
	pause
	goto start
:ssid
	set /p ssid="input wifi ssid輸入wifi ssid:"
	set /p password="input wifi password輸入wifi密碼:"
	echo #import esp >%USERPROFILE%\boot.py
	echo import uos, machine, time, network, gc >>%USERPROFILE%\boot.py
	echo gc.collect() >>%USERPROFILE%\boot.py
	echo sta_if = network.WLAN(network.STA_IF) >>%USERPROFILE%\boot.py
	echo sta_if.active(True) >>%USERPROFILE%\boot.py
	echo sta_if.connect('%ssid%', '%password%') >>%USERPROFILE%\boot.py
	echo while not sta_if.isconnected(): >>%USERPROFILE%\boot.py
	echo     time.sleep(1) >>%USERPROFILE%\boot.py
	echo     pass >>%USERPROFILE%\boot.py
	echo print('network config:', sta_if.ifconfig()) >>%USERPROFILE%\boot.py
	ampy --port %1 put %USERPROFILE%\boot.py
	echo "wifi ssid password set complete 無線網路設定完"
	echo "input any key to continue.按任意鍵繼續"
	pause
	goto start
:end
    echo "tks bye bye!"

