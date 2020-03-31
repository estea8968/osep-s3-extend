@echo off
chcp 65001
cd "c:\Program Files (x86)\s3-extend-tool"
wmic logicaldisk get caption
set /p cpx_disk="input cpx disk(輸入cpx的磁碟機代號例如E:):"
copy firmware\FirmataCPx.uf2 %cpx_disk%
echo cpx firmware burn complete 韌體燒錄完成