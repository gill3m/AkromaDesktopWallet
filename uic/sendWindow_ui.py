# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../sendWindow.ui'
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

class Ui_Send(object):
    def setupUi(self, Send):
        Send.setObjectName(_fromUtf8("Send"))
        Send.resize(600, 300)
        Send.setStyleSheet(_fromUtf8(""))
        self.formLayout = QtGui.QFormLayout(Send)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.lbl_to = QtGui.QLabel(Send)
        self.lbl_to.setObjectName(_fromUtf8("lbl_to"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.lbl_to)
        self.lineEdit_to = QtGui.QLineEdit(Send)
        self.lineEdit_to.setObjectName(_fromUtf8("lineEdit_to"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEdit_to)
        self.lbl_amt = QtGui.QLabel(Send)
        self.lbl_amt.setObjectName(_fromUtf8("lbl_amt"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.lbl_amt)
        self.lineEdit_amt = QtGui.QLineEdit(Send)
        self.lineEdit_amt.setObjectName(_fromUtf8("lineEdit_amt"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEdit_amt)
        self.lbl_gas = QtGui.QLabel(Send)
        self.lbl_gas.setObjectName(_fromUtf8("lbl_gas"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.lbl_gas)
        self.lineEdit_gas = QtGui.QLineEdit(Send)
        self.lineEdit_gas.setObjectName(_fromUtf8("lineEdit_gas"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.lineEdit_gas)
        spacerItem = QtGui.QSpacerItem(20, 150, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.formLayout.setItem(4, QtGui.QFormLayout.FieldRole, spacerItem)
        self.btn_Send = QtGui.QPushButton(Send)
        self.btn_Send.setObjectName(_fromUtf8("btn_Send"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.btn_Send)
        self.lineEdit_Balance = QtGui.QLineEdit(Send)
        self.lineEdit_Balance.setEnabled(False)
        self.lineEdit_Balance.setAutoFillBackground(False)
        self.lineEdit_Balance.setReadOnly(True)
        self.lineEdit_Balance.setObjectName(_fromUtf8("lineEdit_Balance"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.lineEdit_Balance)
        self.lbl_Balance = QtGui.QLabel(Send)
        self.lbl_Balance.setObjectName(_fromUtf8("lbl_Balance"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.lbl_Balance)

        self.retranslateUi(Send)
        QtCore.QMetaObject.connectSlotsByName(Send)

    def retranslateUi(self, Send):
        Send.setWindowTitle(_translate("Send", "Form", None))
        self.lbl_to.setText(_translate("Send", "To", None))
        self.lbl_amt.setText(_translate("Send", "Amt", None))
        self.lbl_gas.setText(_translate("Send", "Gas", None))
        self.btn_Send.setText(_translate("Send", "Send", None))
        self.lbl_Balance.setText(_translate("Send", "Balance", None))

