#!/bin/bash
#cd /opt/s3-extend-tool/firmware/esp8266
. /opt/s3-extend-tool/firmware/esp8266/config

u_choice=2
##echo "list ttyUSB port:"
###ls /dev/ttyUSB*
##read -e -i "$d_port" -p "Please input esp8266 port:" d_port 
##echo  " esp8266 port="$d_port 

read  -e -i "$u_choice" -p "choice (1:burn firmware 2:set wifi ssid password): " u_choice
if [ $u_choice -eq 1 ];then 
	esptool.py --port $1 --baud 460800 write_flash --flash_size=detect -fm dio 0 /opt/s3-extend-tool/firmware/esp8266/esp8266-20191220-v1.12.bin
	ampy --port $1 put /opt/s3-extend-tool/firmware/esp8266/main.py
	ampy --port $1 put /opt/s3-extend-tool/firmware/esp8266/esp_8266_min.py 
	echo "esp8266 firmware burn complete"
	read -n 1 -p "Press any key to continue..."
else
	read -e -i "$ssid" -p "Please input wifi ssid:" ssid
	read -e -i "$password" -p "Please input wifi password:" password
	echo "#import esp" >/tmp/boot.py
	echo "import uos, machine, time, network, gc" >>/tmp/boot.py
	echo "gc.collect()" >>/tmp/boot.py
	echo "sta_if = network.WLAN(network.STA_IF)" >>/tmp/boot.py
	echo "sta_if.active(True)" >>/tmp/boot.py
	echo "sta_if.connect('"$ssid"', '"$password"')" >>/tmp/boot.py
	echo "while not sta_if.isconnected():" >>/tmp/boot.py
	echo "    time.sleep(1)" >>/tmp/boot.py
	echo "    pass" >>/tmp/boot.py
	echo "print('network config:', sta_if.ifconfig())" >>/tmp/boot.py
	ampy --port $1 put /tmp/boot.py
	echo "wifi data reset complete"
	read -n 1 -p "Press any key to continue..."
fi

