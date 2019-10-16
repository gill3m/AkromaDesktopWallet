import sys
import os
from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import QDialog, QFileDialog

import uic.mainwindow_ui as mainwindow_ui
from modules.misc_web3 import *
from modules.table_model import *
from modules.wallet_worker import *
from modules.send_window import *
from modules.settings_window import *
from modules.fileops import *


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
		#User chosen a new wallet
		settings.walletSignal.connect(self.sayWallet)
		settings.walletSignal.connect(send.sendWindowStoreWallet)

		#UTC file associated with this wallet, this is chosen by User
		# in the Settings window.
		settings.fileSignal.connect(self.sayFile)
		settings.fileSignal.connect(send.sendWindowStoreFile)
		settings.passSignal.connect(send.sendWindowStorePass)

		self.connect(self.ui.btn_Home, SIGNAL("clicked()"), self.handleBtnWHome)
		self.connect(self.ui.btn_Send, SIGNAL("clicked()"), self.handleBtnWSend)
		self.connect(self.ui.btn_Settings, SIGNAL("clicked()"), self.handleBtnWSettings)
		self.walletUpdated=False

		#this will store txns as they arrive for saving to to file
		#together with the current blockheight
		self.myWalletData={}
		#setup tableData
		#TODO - initial load from wallet file
		self.tableData=[]
		#self.txnTest()
		self.setTableDefaults()
		#lets wait for user to select wallet

		#setup setIcons
		self.setBtnIcons()


	def setBtnIcons(self):
		#TODO use resource file
		homeIcon=QtGui.QIcon("assets/icons/home1.svg")
		self.ui.btn_Home.setIcon(homeIcon)

		sendIcon=QtGui.QIcon("assets/icons/arrowx2.png")
		self.ui.btn_Send.setIcon(sendIcon)

		settingsIcon=QtGui.QIcon("assets/icons/settings.png")
		self.ui.btn_Settings.setIcon(settingsIcon)


	def closeEvent(self, e):
	# Write window size and position to config file
		if self.walletUpdated == True:
			print("Window about to close..writing wallet data")
			self.dumpCurrWalletJson()
			print("Done")
		#for some reason terminal window is left in unknown state, make sane again
		os.system('stty sane')
		e.accept()




	def startLookingforTxn(self):
		self.thread=Worker(self.myWallet, self.blockHeight)
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

		#Append this txn to walletdict
		self.myWalletData['txns'].append({
		'direction': x[0],
		'addr': x[1],
		'amt' : x[2],
		'date' : x[3],
		'txn' : x[4]
		})
		self.tableData.insert(0, x)

		self.ui.tableView_txn.model().layoutChanged.emit()
		#Update the balance
		self.set_balance(self.myWallet)
		#TODO add txn to datastore

	def readWalletStore(self):
		#check file exists, otherwise make new wallet
		pathtoFile=buildFullPath(self.myWalletUC);
		ret = checkFileExists(pathtoFile)
		if ret == False:
			data={}
			data['blockHeight'] = 0
			data['txns']=[]
			with open(pathtoFile, 'w') as outfile:
				json.dump(data, outfile, indent=4)
			print("Info: wallet file does not exist - will create new one")

		#read blockheight from file
		blockHeight, ok = getTxnHeight(self.myWalletUC)
		if ok==True:
			self.blockHeight= blockHeight
			wallet=buildFullPath(self.myWalletUC)
			#get the txns
			try:
				with open(wallet, 'r') as fp:
					obj = json.load(fp)
					self.myWalletData=obj

			except ValueError:
				print ("readWalletStore::error loading JSON")

			print ("Wallet is at height:" + str(blockHeight))
			#make list to append into datastore


			for tx in obj['txns']:
				'''
				print('Direction: ' + tx['direction'])
				print('addr: ' + tx['addr'])
				print('amt: ' + tx['amt'])
				print('date: ' + tx['date'])
				print('txn: ' + tx['txn'])
				'''
				data=[tx['direction'],tx['addr'],tx['amt'],tx['date'],tx['txn']]

				# put these txns on main display
				self.tableData.insert(0, data)

				self.ui.tableView_txn.model().layoutChanged.emit()


	@pyqtSlot(str)
	def sayWallet(self, str):
		''' print Wallet name  '''
		print("New incoming wallet:" + str)

		#switching wallet dump the old one to disk
		if self.walletUpdated == True:
			self.dumpCurrWalletJson()
			#stop current thread
			self.thread.stop()
			self.myWalletData={}
			#reset display data data aswell
			del self.tableData[:]
			self.ui.tableView_txn.model().layoutChanged.emit()



		self.myWalletOrig=str
		# run thru checksum to fix lowercase addr otheriwse GetBalance error
		wallet = w3.toChecksumAddress(str)
		self.myWallet=wallet
		self.myWalletUC=wallet.upper()
		self.walletUpdated=True

		# TODO stop looking on old thread
		self.set_wallet(wallet)				#set wallet on screen
		self.set_balance(wallet)            #set balance on screen
		self.readWalletStore()

		self.startLookingforTxn()

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

	def dumpCurrWalletJson(self):
		pathtoFile=buildFullPath(self.myWalletUC)
		self.myWalletData['blockHeight'] = getCurrBlockNo()
		with open(pathtoFile, 'w') as outfile:
			json.dump(self.myWalletData, outfile, indent=4)


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

#def myExitHandler():
	#pass

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)

	#app.aboutToQuit.connect(myExitHandler) # myExitHandler is a callable
	#check geth connection
	if not checkGethRunning():
		print('Please start geth....with --rpc  --rpcaddr 127.0.0.1 --rpcport 8545 --rpcapi web3,admin,personal,db,eth,net --rpccorsdomain "*"')
		exit(1)

	akromaMain = ControlMainWindow()
	akromaMain.show()
	sys.exit(app.exec_())
