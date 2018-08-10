# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../mainwindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(600, 400)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralWidget)
        self.gridLayout.setMargin(11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.btn_Settings = QtGui.QPushButton(self.centralWidget)
        self.btn_Settings.setObjectName(_fromUtf8("btn_Settings"))
        self.gridLayout.addWidget(self.btn_Settings, 0, 3, 1, 1)
        self.btn_Home = QtGui.QPushButton(self.centralWidget)
        self.btn_Home.setObjectName(_fromUtf8("btn_Home"))
        self.gridLayout.addWidget(self.btn_Home, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        self.btn_Send = QtGui.QPushButton(self.centralWidget)
        self.btn_Send.setObjectName(_fromUtf8("btn_Send"))
        self.gridLayout.addWidget(self.btn_Send, 0, 2, 1, 1)
        self.stackedWidget = QtGui.QStackedWidget(self.centralWidget)
        self.stackedWidget.setFrameShape(QtGui.QFrame.StyledPanel)
        self.stackedWidget.setObjectName(_fromUtf8("stackedWidget"))
        self.page = QtGui.QWidget()
        self.page.setObjectName(_fromUtf8("page"))
        self.gridLayout_2 = QtGui.QGridLayout(self.page)
        self.gridLayout_2.setMargin(11)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_2 = QtGui.QLabel(self.page)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 1, 2, 1, 1)
        self.lineedit_balance = QtGui.QLineEdit(self.page)
        self.lineedit_balance.setReadOnly(True)
        self.lineedit_balance.setObjectName(_fromUtf8("lineedit_balance"))
        self.gridLayout_2.addWidget(self.lineedit_balance, 1, 1, 1, 1)
        self.lineEdit_wallet = QtGui.QLineEdit(self.page)
        self.lineEdit_wallet.setReadOnly(True)
        self.lineEdit_wallet.setObjectName(_fromUtf8("lineEdit_wallet"))
        self.gridLayout_2.addWidget(self.lineEdit_wallet, 0, 1, 1, 1)
        self.label = QtGui.QLabel(self.page)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 2, 1, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setMargin(11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_wallet = QtGui.QLabel(self.page)
        self.label_wallet.setObjectName(_fromUtf8("label_wallet"))
        self.verticalLayout.addWidget(self.label_wallet)
        self.label_balance = QtGui.QLabel(self.page)
        self.label_balance.setObjectName(_fromUtf8("label_balance"))
        self.verticalLayout.addWidget(self.label_balance)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 2, 1)
        self.tableView_txn = QtGui.QTableView(self.page)
        self.tableView_txn.setObjectName(_fromUtf8("tableView_txn"))
        self.gridLayout_2.addWidget(self.tableView_txn, 3, 1, 1, 1)
        self.stackedWidget.addWidget(self.page)
        self.gridLayout.addWidget(self.stackedWidget, 1, 0, 1, 4)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 600, 22))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtGui.QToolBar(MainWindow)
        self.mainToolBar.setObjectName(_fromUtf8("mainToolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Akroma Desktop Wallet", None))
        self.btn_Settings.setText(_translate("MainWindow", "Settings", None))
        self.btn_Home.setText(_translate("MainWindow", "Home", None))
        self.btn_Send.setText(_translate("MainWindow", "Send", None))
        self.label_2.setText(_translate("MainWindow", "AKA", None))
        self.label.setText(_translate("MainWindow", "Recent Transactions", None))
        self.label_wallet.setText(_translate("MainWindow", "Wallet", None))
        self.label_balance.setText(_translate("MainWindow", "Balance", None))

