from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import QDialog, QFileDialog
from modules.misc_web3 import *
from pathlib import Path

import uic.settingsinfo_ui as settingsinfo_ui


class SettingsWindow(QtGui.QWidget):
	walletSignal = pyqtSignal(str)
	fileSignal = pyqtSignal(str)
	passSignal = pyqtSignal(str)

	def __init__(self, parent=None):

		self.walletAddr=""
		self.walletUTC=""
		QtGui.QWidget.__init__(self, parent)
		self.ui = settingsinfo_ui.Ui_SettingsInfo()
		self.ui.setupUi(self)
		self.connect(self.ui.btn_OPenWallet, SIGNAL("clicked()"), self.handleBtnOpenWallet)
#		self.connect(self.ui.btn_CreateWallet, SIGNAL("clicked()"), self.handleBtnCreateWallet)

	def sendWallet(self):
#		print("sending addr:" + self.walletAddr)
		self.walletSignal.emit(self.walletAddr)

	def sendFname(self):
		self.fileSignal.emit(self.walletUTC)

	def sendPass(self):
		self.passSignal.emit(self.walletPass)


	def handleBtnOpenWallet(self):
		home = str(Path.home())
		fname = QFileDialog.getOpenFileName(self, 'Open file',
				home,"*.*")
		if len(fname) != 0 :

			#Enter password to verify wallet
			input, ok = QtGui.QInputDialog.getText(None, 'Password',
                                                   'Enter password:', QtGui.QLineEdit.Password)

			print(fname)

			print(input, ok)
			self.walletPass=input
			ret = verifyWallet(fname, input)
			print (ret)
			if ret == False:
				msg = QtGui.QMessageBox()
				msg.setIcon(QtGui.QMessageBox.Information)

				msg.setText("Invalid Password ")
				msg.setInformativeText("This file cannot be used")
				msg.setStandardButtons(QtGui.QMessageBox.Ok)
				msg.exec_()
			else:
				self.walletUTC = fname
				#get the wallet address from file
				addr=getAddrfromFile(fname)
				self.walletAddr=addr
				#print(addr)
				#send Fname to MainWindow
				self.sendFname()

				#send wallet addr to main window
				self.sendWallet()

				#send the password for use in send window
				self.sendPass()
