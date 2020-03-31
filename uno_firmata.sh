#/bin/bash
cd /opt/s3-extend-tool/firmware
avrdude -v -patmega328p -carduino -P$1 -b115200 -D -Uflash:w:FirmataExpress.ino.hex:i
zenity --info --width=200 --text="uno firmware burn complete. 韌體燒錄完成"
