#/bin/bash
cp /opt/s3-extend-tool/firmware/FirmataCPx.uf2 /media/$USER/CPLAYBOOT
if [ "$?" == "0" ] ; then
	zenity --info --width=200 --text="cpx firmware copy complete. cpx 韌體燒錄完成"
else
	zenity --info --width=200 --text="cpx firmware copy false. cpx 韌體燒錄失敗"
fi

