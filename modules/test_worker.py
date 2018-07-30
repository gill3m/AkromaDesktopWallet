from PyQt4 import QtGui, QtCore
from wallet_worker import *

searchWallet="0x11082c348fab0c5877ac2a345a3e76b18fe0ae5c"

def printTx(txn):
	print(txn)

def printBlock(block):
	print("GUI:" + str(block))

def threadFinished():
	print("thread finished......")

def startThread():
	app = QtCore.QCoreApplication([])

	thread = Worker(searchWallet)
	thread.transaction.connect(printTx)
	thread.currentBlock.connect(printBlock)
	#thread.finished.connect(app.exit)
	thread.finished.connect(threadFinished)
	thread.start()
	sys.exit(app.exec_())


if __name__ == "__main__":
    startThread()


