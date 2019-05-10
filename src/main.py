import time
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QListWidgetItem
from UI.main import Ui_Library
from UI.add import Ui_addReadingRoom
from PyQt5 import QtWidgets,QtGui,QtCore
from UI.vip import Ui_vip
import sys

class mainWindow(QtWidgets.QMainWindow, Ui_Library):
    def __init__(self):
        super(mainWindow, self).__init__()
        self.setupUi(self)
        self.pushButton_2.clicked.connect(self.addRead)
        self.listWidget.itemClicked.connect(self.showRoom)
        self.pushButton.clicked.connect(self.find)

    def find(self):
        print(self.dateTimeEdit.text())
        print(self.listWidget.currentItem().text())

    def load_data(self, sp):
        for i in range(1, 100):  # 模拟主程序加载过程
            time.sleep(0.04)  # 加载数据
            sp.showMessage("加载... {0}%".format(i), QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.white)
            QtWidgets.qApp.processEvents()  # 允许主进程处理事件

    def addRead(self):
        add.show()

    # def showEvent(self, *args, **kwargs):
    #     self.listWidget.clear()
    #     f = open('ReadingRoom.txt', 'r')
    #     name = f.readline()
    #     while name != "":
    #         newItem = QListWidgetItem(name)
    #         self.listWidget.addItem(newItem)
    #         name = f.readline()
    #     f.close()

    def showRoom(self):
        self.tableWidget.clear()
        row=self.listWidget.currentRow()
        fname='ReadingRoom/'+self.listWidget.item(row).text().strip('\n')+'.txt'
        fobj=open(fname,'r')
        name = fobj.readline()
        while name != "":
            line=name.strip('\n')
            num=0
            for i in line:
                num=num*10+int(i)
            newItem=QTableWidgetItem()
            newItem.setBackground(QtCore.Qt.gray)
            self.tableWidget.setItem(num/10,num%10,newItem)
            name=fobj.readline()



class addWimdow(QtWidgets.QMainWindow,Ui_addReadingRoom):
    def __init__(self):
        super(addWimdow, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.add)
        self.tableWidget.cellClicked.connect(self.block)

        # self.tableWidget.doubleClicked.connect(self.clear)

    def block(self):
        row=self.tableWidget.currentRow()
        cou=self.tableWidget.currentColumn()
        if row*10+cou in x:
            x.remove(row*10+cou)
            newItem = QTableWidgetItem("")
            self.tableWidget.setItem(row, cou, newItem)
        else:
            addVip.show()


    def add(self):
        if self.lineEdit.text()=="":
            self.label_2.setText("名称不能为空")
        elif len(x)==0:
            self.label_2.setText( "座位不能为空")
        else:
            f=open('ReadingRoom.txt','r+')
            if f.readline()==(self.lineEdit.text()+"\n"):
                self.label_2.setText("名称重复")
            else:
                fname='ReadingRoom/'+self.lineEdit.text()+'.txt'
                # if os.path.exists(fname):
                #     self.label_2.setText("阅览室已存在")
                # else:
                f.write(self.lineEdit.text() + "\n")
                fobj=open(fname,'w')
                for num in x:
                    fobj.write(str(num)+"\n")
                fobj.close()
                reply=QMessageBox.information(self,"Tips","添加成功")
                if reply==QMessageBox.Ok:
                    self.close()
                f.close()

    def closeEvent(self, *args, **kwargs):
        x.clear()
        self.tableWidget.clear()
        self.lineEdit.clear()


class addVip(QtWidgets.QMainWindow,Ui_vip):
    def __init__(self):
        super(addVip, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.click)
        self.comboBox.addItem('C')

    def showEvent(self, *args, **kwargs):
        self.lineEdit.setText("未设置")
        self.comboBox.setCurrentText("空")

    def click(self):
        row=add.tableWidget.currentRow()
        cou=add.tableWidget.currentColumn()
        x.add(row * 10 + cou)
        newItem = QTableWidgetItem(self.lineEdit.text() + " " + self.comboBox.currentText())
        newItem.setBackground(QtCore.Qt.gray)
        add.tableWidget.setItem(row, cou, newItem)
        self.close()

if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    add=addWimdow()
    addVip=addVip()
    splash = QtWidgets.QSplashScreen(QtGui.QPixmap('img.png'))
    splash.showMessage("加载... 0%", QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.white)
    splash.show()  # 显示启动界面
    QtWidgets.qApp.processEvents()  # 处理主进程事/件
    app.processEvents()
    window = mainWindow()
    window.load_data(splash)  # 加载数据
    window.show()
    splash.finish(window)
    x = set()
    sys.exit(app.exec_())