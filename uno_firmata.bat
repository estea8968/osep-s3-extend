@echo on
set PATH=%path%;C:\Program Files (x86)\Arduino\hardware\tools\avr\bin;C:\Program Files (x86)\Arduino\hardware\tools\avr\utils\bin;C:\Program Files (x86)\Arduino\hardware\tools\avr\etc
cd "C:\Program Files (x86)\osep-s3-extend\firmware"
"C:\Program Files (x86)\Arduino\hardware\tools\avr\bin\avrdude.exe" -v -p atmega328p -carduino -P %1 -b 115200 -D -Uflash:w:FirmataExpress.ino.hex:i
