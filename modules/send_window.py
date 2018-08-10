from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import QDialog, QFileDialog
import uic.sendWindow_ui as sendWindow_ui
from modules.misc_web3 import *
from modules.misc_shared import *
import sys

class SendWindow(QtGui.QWidget):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.ui = sendWindow_ui.Ui_Send()
		self.ui.setupUi(self)

		self.connect(self.ui.btn_Send, SIGNAL("clicked()"), self.handleBtnSend)
		#Uno wallet selected
		self.WalletInit=False


	def handleBtnSend(self):
		ret = self.validateForm()
		if ret == False:
			return

		ret = self.prepareAndSend()

	def prepareAndSend(self):
		try:
			toAddr = w3.toChecksumAddress(self.ui.lineEdit_to.text())
		except TypeError as err:
			print("Exception occurred" )
			print (err)
			displayMessage(MessageType.Warn, str(err), "Error on validating Address, exception occurred")
			return

		except ValueError as v:
			print("ValueError Exception occurred" )
			print (v)
			displayMessage(MessageType.Warn, str(v), "Error on validating Address, exception occurred")
			return

		except :
			print ("Unknown exception occurred on signTransaction")
			print (sys.exc_info()[0])
			return

		fromAddr = self.myWallet
		gasGiven = int(self.ui.lineEdit_gas.text())
		value= getAmtInWei(float(self.ui.lineEdit_amt.text()))
		nonce = getTransactionCount(self.myWallet)
		gasPrice=getGasPrice()

		transaction = {
    		'to': toAddr,
    		'from': fromAddr,
    		'value': value,
    		'gas':gasGiven,
    		'nonce':nonce,
    		'gasPrice':gasPrice
		}

		print (transaction)

		privKey=getPrivKey(self.myUTCFile, self.myPass)

		try:
			signed_transaction = w3.eth.account.signTransaction(transaction, privKey)
		except TypeError as err:
			print("Exception occurred" )
			print (err)
			displayMessage(MessageType.Warn, str(err), "Error on validating Address, exception occurred")


		except ValueError as v:
			print("ValueError Exception occurred" )
			print (v)
			displayMessage(MessageType.Warn, str(v), "Error on signTxn, exception occurred")

		except :
			print ("Unknown exception occurred on signTransaction")
			print (sys.exc_info()[0])


		try:
			transaction_id = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)
		except TypeError as err:
			print("Exception occurred" )
			print (err)
			return

		except ValueError as v:
			print("ValueError Exception occurred" )
			print (v)
			displayMessage(MessageType.Warn, str(v), "Error on send, exception occurred")
			return

		except :
			print ("Unknown exception occurred on signTransaction")
			print (sys.exc_info()[0])
			return



		txHashHex=transaction_id.hex()
		displayMessage(MessageType.Info, txHashHex, "This is your Transaction Id")


	@pyqtSlot(str)
	def sendWindowStorePass(self, str):
		#print("SendWin incoming pass:" + str)
		self.myPass=str

	@pyqtSlot(str)
	def sendWindowStoreFile(self, str):
		print("SendWin incoming file:" + str)
		self.myUTCFile=str

	@pyqtSlot(str)
	def sendWindowStoreWallet(self, inWallet):
		print("SendWin incoming wallet:" + inWallet)
		# run thru checksum to fix lowercase addr otheriwse GetBalance error
		wallet = toChecksumAddr(inWallet)
		self.myWallet=wallet
		self.WalletInit=True

		#set the Balance
		balance = getBal(wallet)
		self.ui.lineEdit_Balance.setText(str(balance))



	def validateForm(self):
		#  wallet initial
		if self.WalletInit == False :
			displayMessage(MessageType.Info, "No Wallet selected ", "Please select a wallet from Settings window")
			return False


		#TODO need more rigorous validation
		if self.ui.lineEdit_to.text() == "":
			displayMessage(MessageType.Info, "Invalid To Addr ", "Please enter a valid address")
			return False

		if self.ui.lineEdit_amt.text() == "":
			displayMessage(MessageType.Info, "Invalid Amt ", "Please enter a valid Amt")
			return False

		if self.ui.lineEdit_gas.text() == "":
			displayMessage(MessageType.Info, "Invalid Gas", "Please enter atleast 21000")
			return False

		return True
