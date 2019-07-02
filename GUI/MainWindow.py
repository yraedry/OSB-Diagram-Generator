from PyQt5 import QtCore, QtGui, QtWidgets
import utils.FilesOperations

import os


class Ui_MainWindow(object):
    service_dir = os.path.normpath(os.getcwd() + os.sep + os.pardir + "/Files")


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(828, 513)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 30, 241, 441))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.listWidget = QtWidgets.QListWidget(self.tab)
        self.listWidget.setGeometry(QtCore.QRect(0, 0, 235, 415))
        self.listWidget.setObjectName("listWidget")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.listWidget_2 = QtWidgets.QListWidget(self.tab_2)
        self.listWidget_2.setGeometry(QtCore.QRect(0, 0, 235, 415))
        self.listWidget_2.setObjectName("listWidget_2")
        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 828, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        items_list = utils.FilesOperations.read_files(self.service_dir, "services.txt")
        service_line = items_list.readlines()

        # Ahora mismo esta con valores absolutos, aqui deberemos leer de una BBDD
        exclude_services = ["Cibt-OSB-common", "Cibt-OSB-templates", "Cibt-SOA-common", "Cibt-SOA-mds"]
        available_services = []
        for x in service_line:
            for y in exclude_services:
                if x.rstrip('\n') == y:
                    service_line.remove(x)
                else:
                    available_services.append(x.rstrip('\n'))
        # #revisar
        # for z in available_services:
        #     if "OSB" in z:
        #         self.listWidget.addItem(z)
        #     elif "SOA" in z:
        #         self.listWidget_2.addItem(z)

        # for y in exclude_services:
        #     for x in service_line:
        #         if y == x.rstrip('\n'):
        #             service_line.remove(x)
        for x in service_line:
            if "OSB" in x:
                self.listWidget.addItem(x.rstrip('\n'))
            elif "SOA" in x:
                self.listWidget_2.addItem(x.rstrip('\n'))


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Tab 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Tab 2"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

