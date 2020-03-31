# -*- coding: utf-8 -*-
import sys
import os
import glob
import serial
import subprocess
from PyQt5 import QtCore ,QtWidgets
from PIL import Image, ImageDraw, ImageFilter
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListView, QVBoxLayout, QMessageBox, QGridLayout 
from PyQt5.QtCore import QStringListModel, pyqtSlot
from PyQt5.QtGui import QIcon, QPixmap
  
#path_dir = '/home/teacher/Documents/s3-extend-tool' def_browser='firefox' def_offline ='onegpio_scratch3'
#目前位置
now_path = os.path.abspath(os.getcwd())

global def_url 
def_url = 'https://jycs.page.link/osep-editor'
def_classurl = 'https://jycs.page.link/osep-course'
def_abouturl = 'https://jycs.page.link/osep-about'
#def_url = 'https://mryslab.github.io/s3onegpio/'
global def_offline 
##全域變數連接port
global def_port
#//版本號
version = '1.0.1'

def_port = ''
def_disk = ''
##目前位置
now_path = os.path.abspath(os.getcwd())

if serial.sys.platform.startswith('win'):
    os_name = 'win'
    path_dir = 'C:\Program Files (x86)\osep-s3-extend'
    cpx_sh_name = 'cpx_firmata.bat'
    def_browser = 'start'
    exe_s3a = 'start s3a'
    exe_s3c = 'start s3c'
    exe_s3e = 'start s3e'
    exe_s3p = 'start s3p'
    exe_s3r = 'start s3r'
    exe_b_uno = '"'+path_dir+'\\uno_firmata.bat" '
    exe_b_esp8266 = '"'+path_dir+'\\chk_burn_esp8266.bat" '
    exe_b_cpx = '"'+path_dir+'\\cpx_firmata.bat" '
    exe_clear = 'taskkill /f /im python.exe'
    def_offline = '"C:\Program Files (x86)\osep_scratch3\osep_scratch3.exe"'
elif serial.sys.platform.startswith('linux'):
    os_name = 'linux'
    path_dir = '/opt/osep-s3-extend'
    cpx_sh_name = 'cpx_firmata.sh'
    def_browser = 'browse'
    exe_s3a ='gnome-terminal -- s3a '
    exe_s3c = 'gnome-terminal -- s3c'
    exe_s3e = 'gnome-terminal -- s3e'
    exe_s3p = 'gnome-terminal -- s3p'
    exe_s3r = 'gnome-terminal -- s3r'
    exe_b_uno = path_dir+'/uno_firmata.sh '
    exe_b_esp8266 =path_dir+'/firmware/esp8266/burn_esp8266.sh '
    exe_b_cpx = path_dir+'/cpx_firmata.sh'
    exe_clear = 'killall python'
    def_offline = path_dir+'/../osep_scratch3/scratch3'
elif serial.sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
    os_name = 'cygwin'
    path_dir = '/opt/osep-s3-extend'
    def_browser = 'browse'
    exe_s3a = 'gnome-terminal -- s3a '
    exe_s3c = 'gnome-terminal -- s3c'
    exe_s3e = 'gnome-terminal -- s3e'
    exe_s3p = 'gnome-terminal -- s3p'
    exe_s3r = 'gnome-terminal -- s3r'
    exe_b_uno = path_dir+'/uno_firmata.sh '
    #exe_b_esp8266 ='gnome-terminal -- /opt/s3-extend-tool/firmware/esp8266/burn_esp8266.sh '
    exe_b_esp8266 =path_dir+'/firmware/esp8266/burn_esp8266.sh '
    exe_b_cpx = path_dir+'/cpx_firmata.sh '
    def_offline = path_dir+'/../osep_scratch3/scratch3'
elif sys.platform.startswith('darwin'):
    os_name = 'mac'
    path_dir = '/User'
    def_browser = 'open'
    exe_s3a = 's3a'
    exe_s3c = 's3c'
    exe_s3e = 's3e'
    exe_s3p = 's3p'
    exe_s3r = 's3r'
    exe_b_uno = path_dir+'uno_firmata_mac.sh'
    exe_b_esp8266 =path_dir+'burn_esp8266_mac.sh'
    exe_b_cpx = path_dir+'cpx_firmata_mac.sh'
    def_offline = 'osep_scratch3'
else:
    os_name = 'other'
    path_dir = ''
    def_browser = ''
    exe_s3a = 's3a '
    exe_s3c = 's3c'
    exe_s3e = 's3e'
    exe_s3p = 's3p'
    exe_s3r = 's3r'
    exe_b_uno = ''
    exe_b_esp8266 =''
    exe_b_cpx = ''
    def_offline = ''

###偵測連接設備port
def serial_ports():
    """ Lists serial port names
  
        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if serial.sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif serial.sys.platform.startswith('linux') or serial.sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except  serial.SerialException :
            pass
    return result




#class App(QWidget):
class ComboWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.title = os_name+":OSEP控制台 v:"+version
        #背景圖
        self.pixmap = QPixmap('images/osep.png')

        self.left = 100
        self.top = 100
        self.width = 800 
        self.height = 360
        self.setMaximumSize(800,360)
        self.initUI()
    
    def initUI(self):
        
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        #a_combobox = QWidgets.QComboBox()
        comboA = QtWidgets.QComboBox(self)
        comboB = QtWidgets.QComboBox(self)
        #comboA.setGeometry(QtCore.QRect(400, 180, 200, 50))
        comboA.setGeometry(400, 200, 150, 80)
        comboB.setGeometry(20, 300, 220, 40)
        layoutA = QtWidgets.QVBoxLayout(comboA)
        layoutB = QtWidgets.QVBoxLayout(comboB)

        comboA.setStyleSheet("font: 20px; border-style: outset; border-width:0px ; border-color: rbg(128,128,128); color:rgb(0,0,0); background-color: rgb(255,255,255);");
        comboB.setStyleSheet("font: 20px; border-style: outset; border-width:0px ; border-color: rbg(128,128,128); color:rgb(0,0,0); background-color: rgb(255,255,255);");
        comboA.addItem("選擇連線硬體")
        comboA.addItem("Arduino")
        comboA.addItem("Circuit")
        comboA.addItem("ESP-8266")
        comboA.addItem("Picoboard")
        comboA.addItem("Raspberry Pi")
        comboB.addItem("選擇燒錄硬體")
        comboB.addItem("Arduino Uno")
        comboB.addItem("ESP-8266")
        comboB.addItem("Circuit")
        ##預設值
        #comboA.setCurrentIndex(0)
         
        #print (comboA.currentText())
        comboA.activated.connect(self.comboA_selectionchange)
        comboB.activated.connect(self.comboB_selectionchange)
        layoutA.addWidget(comboA)
        layoutB.addWidget(comboB)

        #label
        l_v = QLabel('v:'+version,self) #//版本號
        l_v.resize(80,25)
        l_v.setStyleSheet("font: 12px; border-style: outset; color:rgb(255,0,255);");
        l_v.move(20,20)

        l_A = QLabel("連接硬體功能",self)
        l_A.setAlignment(QtCore.Qt.AlignCenter)
        l_A.resize(150,35)
        l_A.setStyleSheet("font: 20px;text-align:center; color:rgb(255,255,255); background-color: rgb(233,0,125);");
        l_A.move(400,300)
        l_B = QLabel('',self)
        l_B.setPixmap(self.pixmap)
        l_B.resize(300,160)
        l_B.move(350,10)

        l_C =QLabel('燒錄韌體',self)
        l_C.move(250,300)
        l_C.setAlignment(QtCore.Qt.AlignCenter) #//*置中*/
        l_C.resize(120,35)
        l_C.setStyleSheet("font: 20px;text-align:center; color:rgb(255,255,255); background-color: rgb(233,0,125);");

        l_D =QLabel('開始創作',self)
        l_D.setAlignment(QtCore.Qt.AlignLeft)
        l_D.resize(120,35)
        l_D.setStyleSheet("font: 16px; border-style: outset; border-width:0px ; border-color: rbg(128,128,128); color:rgb(174, 182, 191); ");
        l_D.move(600,175)

        l_E =QLabel('選擇硬體',self)
        l_E.setAlignment(QtCore.Qt.AlignLeft)
        l_E.resize(120,35)
        l_E.setStyleSheet("font: 16px; border-style: outset; border-width:0px ; border-color: rbg(128,128,128); color:rgb(174, 182, 191); ");
        l_E.move(400,175)

        l_F =QLabel('確認硬體',self)
        l_F.setAlignment(QtCore.Qt.AlignLeft)
        l_F.resize(120,35)
        l_F.setStyleSheet("font: 16px; border-style: outset; border-width:0px ; border-color: rbg(128,128,128); color:rgb(174, 182, 191); ");
        l_F.move(20,175)


        b_port = QPushButton("連接埠",self)
        b_port.resize(120,35)
        b_port.setStyleSheet("font: 20px;text-align:center; color:rgb(255,255,255); background-color: rgb(233,0,125);");
        b_port.setToolTip("偵測設備port")
        b_port.move(250,200)
        b_port.clicked.connect(self.b_port_clicked)

        
        #l_B = QLabel("設備port",self)
        #l_B.move(164,10)
        #https://blog.csdn.net/jia666666/article/details/81624550
        listviewA = QListView(self)
        listviewA.setStyleSheet("font: 20px;  background-color: rgb(255,255,255);");
        listviewA.resize(220,80)
        listviewA.move(20,200)
        slm=QStringListModel()

        ##port
        self.qList=serial_ports()
        ##listviewA.qList=['aaaa','bbbb','cccc']
        slm.setStringList(self.qList)
        listviewA.setModel(slm)
        listviewA.clicked.connect(self.listviewA_clicked)

        b_class = QPushButton("OSEP課程資源",self)
        b_class.setStyleSheet("font: 20px;text-align:center; color:rgb(255,255,255); background-color: rgb(233,0,125);");
        b_class.setToolTip("瀏覽器開啟OSEP課程資源")
        b_class.resize(150,35)
        b_class.move(600,200)
        b_class.clicked.connect(self.b_class_clicked)

        b_url = QPushButton("OSEP線上操作",self)
        b_url.setStyleSheet("font: 20px;text-align:center; color:rgb(255,255,255); background-color: rgb(233,0,125);");
        b_url.setToolTip("瀏覽器開啟OSEP線上操作網站")
        b_url.resize(150,35)
        b_url.move(600,250)
        b_url.clicked.connect(self.b_url_clicked)

        b_offline = QPushButton("OSEP離線操作",self)
        b_offline.resize(150,35)
        b_offline.setStyleSheet("font: 20px;text-align:center; color:rgb(128,128,128); background-color: rgb(255,255,255);");
        b_offline.setToolTip("OSEP離線操作")
        b_offline.move(600,300)
        b_offline.clicked.connect(self.b_offline_clicked)

        b_clear = QPushButton("重置OSEP",self)
        b_clear.setToolTip("clear python.exe")
        b_clear.resize(150,35)
        b_clear.setStyleSheet("font: 20px;text-align:center; color:rgb(128,128,128); background-color: rgb(255,255,255);");
        b_clear.move(600,65)
        b_clear.clicked.connect(self.b_clear_clicked)

        b_about = QPushButton("關於OSEP",self)
        b_about.setToolTip("關於OSEP")
        b_about.resize(150,35)
        b_about.setStyleSheet("font: 20px; color: rgb(128,128,128);  text-align::center; ");
        b_about.move(600,20)
        b_about.clicked.connect(self.b_about_clicked)
        
        self.show()

    # 定義 被觸發時要執行
    @pyqtSlot()
    def b_port_clicked(self):
        global listviewA
        listviewA = QListView(self)
        listviewA.setStyleSheet("font: 20px;  background-color: rgb(255,255,255);");
        listviewA.resize(220,80)
        listviewA.move(20,200)
        slm=QStringListModel()

        self.qList=serial_ports()
        slm.setStringList(self.qList)
        listviewA.setModel(slm)
        listviewA.clicked.connect(self.listviewA_clicked)
        listviewA.show()  #self.show()

    ##//下拉式選單
    def comboA_selectionchange(self,text):
        #print(self.comboA.currentText())
        if text == 0:
            print('') #//choice
        elif text == 1 :
            if os_name == 'win' :
                os.system(exe_clear)

            if def_port  == '' :
                os.system(exe_s3a)
            else :
                subprocess.call( exe_s3a +' -c '+ def_port,shell = True)

        elif text == 2 :  #//circuit
            if os_name == 'win' :
                os.system(exe_clear)

            os.system(exe_s3c)

        elif text == 3 : #//ESP-8266
            if def_port  == '' :
                QMessageBox.information(self,'Error錯誤','Please choice content port必需選port')
            else :
                if os_name == 'win' :
                    os.system(exe_clear)
                    os.system ('"'+path_dir+'\putty.exe" -serial')
                else :
                    os.system ('echo "Ctrl+c then Ctrl+d copy IP .Ctrl+a then Ctrl+q Exit";picocom -b 115200 -l '+def_port)
                os.system(exe_s3e)

        elif text == 4 : #//picoboard
            if os_name == 'win' :
                os.system(exe_clear)

            if def_port  == '' :
                os.system(exe_s3p)
            else :
                subprocess.call( exe_s3p +' -c ' + def_port,shell = True)
                #os.system('s3p -c '+def_port)

        elif text == 5 : #//s3r
            os.system(exe_s3r)

        #print(text)
  
    def comboB_selectionchange(self,text):
        #print(self.comboB.currentText())
        if text == 0:
            print('')
        elif text == 1: #arduino uno burn
            if def_port  == '' :
                QMessageBox.information(self,'Error錯誤','no content port沒有連接port')
            else :
                subprocess.call(exe_b_uno +' '+ def_port,shell = True)
                
        elif text == 2: #circuit
            subprocess.call(exe_b_cpx ,shell = True)

        elif text == 2: #esp-8266
            if def_port  == '' :
                QMessageBox.information(self,'Error錯誤','Please choice  content port必需選port')
            else :
                #print(exe_b_esp8266)
                subprocess.call(exe_b_esp8266 + def_port ,shell = True)

    # 定義 browser onegpio scratch3 被觸發時要執行的
    def b_url_clicked(self):
        os.system(def_browser+' '+def_url)

    #osep課程資源
    def b_class_clicked(self):
        os.system(def_browser+' '+def_classurl)

    # 定義 offline onegpio scratch3 被觸發時要執行的
    def b_offline_clicked(self):
        os.system(def_offline)


    #def listviewA_clicked(listviewA,qModelIndex):
    def listviewA_clicked(self,qModelIndex):
        #提示信息窗，你選擇的訊息
        global def_port
        def_port = self.qList[qModelIndex.row()]
        
    def b_clear_clicked(self):
        os.system(exe_clear)


    def b_about_clicked(self):
        os.system(def_browser+' '+def_abouturl)
        ##QMessageBox.information(self,'About','Name: Chen estea \n Email:estea8968@gmail.com \n url:https://github.com/estea8968/osep-s3-extend/blob/master/LICENSE')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    #ex = App()
    ex = ComboWidget()
    sys.exit(app.exec_())
