## Copyright (c) 2018 - Akroma Project (www.akroma.io)

from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import QDialog, QFileDialog
from modules.misc_web3 import *
from modules.misc_shared import *
from pathlib import Path
import json
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
		self.connect(self.ui.btn_CreateWallet, SIGNAL("clicked()"), self.handleBtnCreateWallet)
		self.connect(self.ui.btn_PrivateKey, SIGNAL("clicked()"), self.handleBtnPrivateKey)


	def sendWallet(self):
#		print("sending addr:" + self.walletAddr)
		self.walletSignal.emit(self.walletAddr)

	def sendFname(self):
		self.fileSignal.emit(self.walletUTC)

	def sendPass(self):
		self.passSignal.emit(self.walletPass)

	def handleBtnPrivateKey(self):
		home = str(Path.home())
		fname = QFileDialog.getOpenFileName(self, 'Open file',
				home,"*.*")
		if len(fname) != 0 :
			#Enter password to verify wallet
			input, ok = QtGui.QInputDialog.getText(None, 'Password',
                                                   'Enter password:', QtGui.QLineEdit.Password)

			if ok == True:
				privKey = getPrivKey(fname, input)
				if privKey == "ERROR":
					displayMessage(MessageType.Info, "Invalid Password ", "Please enter a valid password for this wallet.")

				else :
					keyHex = privKey.hex()
					displayMessage(MessageType.Info, keyHex, "This your private key for this wallet. Keep this safe and do not disclose to anyone. You can recover you wallet with this key")


	def handleBtnCreateWallet(self):
		#Enter password to verify wallet
		input, ok = QtGui.QInputDialog.getText(None, 'Password',
                                               'Enter password:', QtGui.QLineEdit.Password)
		#if ok == True
		if ok == True:
			if len(input) == 0:
				displayMessage(MessageType.Info, "Please enter a password", "Password cannot be empty!")
				return

			print("About to make file")
			acct = w3.personal.newAccount('password')
			displayMessage(MessageType.Info, acct, "This is your wallet address. Your wallet file has been created in your keystore directory. Now select Private Key button to discover your private key")

			#write this file to config
			#create wallet file in Akroma
			acctUC=acct.upper()
			dataDir=getDataDir()
			walletDir=dataDir + "/keystore/"
			walletStore=walletDir + acctUC + ".dat"
			print(walletStore)

			#make dict for new wallet,set txnHeight to curr block no
			#we will store txns as they arrive
			data={}
			data['blockHeight'] = getCurrBlockNo()
			data['txns']=[]
			with open(walletStore, 'w') as outfile:
				json.dump(data, outfile, indent=4)


	def handleBtnOpenWallet(self):
		home = str(Path.home())
		fname = QFileDialog.getOpenFileName(self, 'Open file',
				home,"*.*")
		if len(fname) != 0 :

			#Enter password to verify wallet
			input, ok = QtGui.QInputDialog.getText(None, 'Password',
                                                   'Enter password:', QtGui.QLineEdit.Password)

			#print(fname)

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
