from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import QDialog, QFileDialog
import uic.sendWindow_ui as sendWindow_ui
from modules.misc_web3 import *

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
		toAddr = w3.toChecksumAddress(self.ui.lineEdit_to.text())
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

		except ValueError as v:
			print("ValueError Exception occurred" )
			print (v)
		except :
			print ("Unknown exception occurred on signTransaction")
			print (sys.exc_info()[0])


		try:
			transaction_id = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)
		except TypeError as err:
			print("Exception occurred" )
			print (err)

		except ValueError as v:
			print("ValueError Exception occurred" )
			print (v)
		except :
			print ("Unknown exception occurred on signTransaction")
			print (sys.exc_info()[0])


		txHashHex=transaction_id.hex()
		msg = QtGui.QMessageBox()
		msg.setIcon(QtGui.QMessageBox.Information)
		msg.setText(txHashHex)
		msg.setInformativeText("This is your Transaction Id")
		msg.setStandardButtons(QtGui.QMessageBox.Ok)
		msg.exec_()


	@pyqtSlot(str)
	def sendWindowStorePass(self, str):
		#print("SendWin incoming pass:" + str)
		self.myPass=str

	@pyqtSlot(str)
	def sendWindowStoreFile(self, str):
		print("SendWin incoming file:" + str)
		self.myUTCFile=str

	@pyqtSlot(str)
	def sendWindowStoreWallet(self, str):
		print("SendWin incoming wallet:" + str)
		# run thru checksum to fix lowercase addr otheriwse GetBalance error
		wallet = toChecksumAddr(str)
		self.myWallet=wallet
		self.WalletInit=True



	def validateForm(self):
		#  wallet initial
		if self.WalletInit == False :
			msg = QtGui.QMessageBox()
			msg.setIcon(QtGui.QMessageBox.Information)
			msg.setText("No Wallet selected ")
			msg.setInformativeText("Please select a wallet from Settings window")
			msg.setStandardButtons(QtGui.QMessageBox.Ok)
			msg.exec_()
			return False


		#TODO need more rigorous validation
		if self.ui.lineEdit_to.text() == "":
			msg = QtGui.QMessageBox()
			msg.setIcon(QtGui.QMessageBox.Information)
			msg.setText("Invalid To Addr ")
			msg.setInformativeText("Please enter a valid address")
			msg.setStandardButtons(QtGui.QMessageBox.Ok)
			msg.exec_()
			return False

		if self.ui.lineEdit_amt.text() == "":
			msg = QtGui.QMessageBox()
			msg.setIcon(QtGui.QMessageBox.Information)
			msg.setText("Invalid Amt ")
			msg.setInformativeText("Please enter a valid Amt")
			msg.setStandardButtons(QtGui.QMessageBox.Ok)
			msg.exec_()
			return False

		if self.ui.lineEdit_gas.text() == "":
			msg = QtGui.QMessageBox()
			msg.setIcon(QtGui.QMessageBox.Information)
			msg.setText("Invalid Gas")
			msg.setInformativeText("Please enter atleast 21000")
			msg.setStandardButtons(QtGui.QMessageBox.Ok)
			msg.exec_()
			return False

		return True
