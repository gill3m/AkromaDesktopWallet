import sys

from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import QDialog, QFileDialog

import uic.mainwindow_ui as mainwindow_ui
from modules.misc_web3 import *
from modules.table_model import *
from modules.wallet_worker import *
from modules.send_window import *
from modules.settings_window import *


class ControlMainWindow(QtGui.QMainWindow):

	def __init__(self, parent=None):
		super(ControlMainWindow, self).__init__(parent)
		self.ui = mainwindow_ui.Ui_MainWindow()
		self.ui.setupUi(self)
		# Add the send window
		send = SendWindow()
		self.ui.stackedWidget.addWidget(send)

		#Add the settings window
		settings = SettingsWindow()
		self.ui.stackedWidget.addWidget(settings)

		#Setup slots connections here
		settings.walletSignal.connect(self.sayWallet)
		settings.walletSignal.connect(send.sendWindowStoreWallet)
		settings.fileSignal.connect(self.sayFile)
		settings.fileSignal.connect(send.sendWindowStoreFile)
		settings.passSignal.connect(send.sendWindowStorePass)



		self.connect(self.ui.btn_Home, SIGNAL("clicked()"), self.handleBtnWHome)
		self.connect(self.ui.btn_Send, SIGNAL("clicked()"), self.handleBtnWSend)
		self.connect(self.ui.btn_Settings, SIGNAL("clicked()"), self.handleBtnWSettings)
		self.walletUpdated=False

		#setup tableData
		#TODO - initial load from wallet file
		self.tableData=[]
		#self.txnTest()
		self.setTableDefaults()
		#lets wait for user to select wallet


	def startLookingforTxn(self, searchWallet):
		self.thread=Worker(searchWallet)
		self.thread.transaction.connect(self.TxnArrive)
		self.thread.currentBlock.connect(self.blockArrive)
		self.thread.finished.connect(self.threadFin)
		#self.connect(self.thread, self.thread.transaction, self.TxnArrive)
		self.thread.start()

	@pyqtSlot()
	def threadFin(self):
		print ("Thread finished......")

	@pyqtSlot(int)
	def blockArrive(self, blockNo):
		print ("GUI:" + str(blockNo))
		self.statusBar().showMessage("Processed block:" + str(blockNo), 2000)

	@pyqtSlot(str)
	def TxnArrive(self, txnStr):
		print ("GUI:" + txnStr)
		#add to table
#		self.tableData.append(['y',1,1,1,1])

		x=txnStr.split(',')
		self.tableData.insert(0, x)

		self.ui.tableView_txn.model().layoutChanged.emit()
		#Update the
		self.set_balance(self.myWallet)


	@pyqtSlot(str)
	def sayWallet(self, str):
		''' Give wallet name  '''
		print("New incoming wallet:" + str)
		# run thru checksum to fix lowercase addr otheriwse GetBalance error
		wallet = w3.toChecksumAddress(str)
		self.myWallet=wallet
		self.set_wallet(wallet)				#send Fname to MainWindow
		self.set_balance(wallet)
		self.walletUpdated=True
		# TODO raise signal to save old wallet info to file
		# TODO reset tableData if new wallet

		#start background thread.....
		self.startLookingforTxn(wallet)

	@pyqtSlot(str)
	def sayFile(self, str):
		print("New incoming file:" + str)
		self.myUTCFile=str



	def set_wallet(self, wallet):
		self.ui.lineEdit_wallet.setText(wallet)

	def set_balance(self, wallet):
		bal=getBal(wallet)
		self.ui.lineedit_balance.setText(str(bal))

	def handleBtnWSettings(self):
		self.ui.stackedWidget.setCurrentIndex(2)



	def handleBtnWSend(self):
		self.ui.stackedWidget.setCurrentIndex(1)
		'''
		msg = QtGui.QMessageBox()
		msg.setIcon(QtGui.QMessageBox.Information)

		msg.setText("This is a send message box")
		msg.setInformativeText("This is additional information")
		msg.setStandardButtons(QtGui.QMessageBox.Ok)
		msg.exec_()
		'''

	def handleBtnWHome(self):
		self.ui.stackedWidget.setCurrentIndex(0)

	def setTableDefaults(self):
		header=['', 'From/To', 'Amt', 'Date', 'Txn']

		tableModel=TxnTableModel(self.tableData,header, self)

		self.ui.tableView_txn.setModel(tableModel)

        # hide grid
		self.ui.tableView_txn.setShowGrid(False)
        # hide vertical header
		vh = self.ui.tableView_txn.verticalHeader()
		vh.setVisible(False)

        # set horizontal header properties
		hh = self.ui.tableView_txn.horizontalHeader()
		hh.setStretchLastSection(True)

        # set column width to fit contents
		self.ui.tableView_txn.resizeColumnsToContents()

        # set row height
		self.ui.tableView_txn.resizeRowsToContents()

        # enable sorting
		self.ui.tableView_txn.setSortingEnabled(False)
		self.ui.tableView_txn.model().layoutChanged.emit()

	def txnTest(self):
		#tableData=[[1,322222222222,4444444444444444,5444444444444,6444444444444444444],
		#[5,6,7,8,9]]


		header=['', 'From/To', 'Amt', 'Date', 'Txn']
		tableModel=TxnTableModel(self.tableData,header, self)

		self.ui.tableView_txn.setModel(tableModel)

        # hide grid
		self.ui.tableView_txn.setShowGrid(False)
        # hide vertical header
		vh = self.ui.tableView_txn.verticalHeader()
		vh.setVisible(False)

        # set horizontal header properties
		hh = self.ui.tableView_txn.horizontalHeader()
		hh.setStretchLastSection(True)

        # set column width to fit contents
		self.ui.tableView_txn.resizeColumnsToContents()

        # set row height
		self.ui.tableView_txn.resizeRowsToContents()

        # enable sorting
		self.ui.tableView_txn.setSortingEnabled(False)
		for y in range (100):
			self.tableData.append([y,1,1,1,1])

		self.ui.tableView_txn.model().layoutChanged.emit()



if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)

	#check geth connection
	if not checkGethRunning():
		print("Please start geth....with --rpcport 8545 --rpcapi personal,eth,web3,admin,net,db --rpccorsdomain *")
		exit(1)

	akromaMain = ControlMainWindow()
	akromaMain.show()
	sys.exit(app.exec_())
