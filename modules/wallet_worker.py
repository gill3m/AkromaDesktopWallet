from web3 import Web3
import binascii
import datetime

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

from PyQt4 import QtCore, QtGui
import sys, time

#TODO this should be loaded from DB or 0 for new wallet
startBlock=0


class Worker(QtCore.QThread):
    transaction = QtCore.pyqtSignal(str)
    currentBlock=QtCore.pyqtSignal(int)

    def __init__(self, str, parent=None):
        super(Worker, self).__init__()
    #
    #    super(Worker, self).__init__(parent)
        self.runThread=True
        self.wallet=str;
        self.startBlock=startBlock
        self.endBlock=w3.eth.blockNumber

    def stop(self):
        self.runThread = False

    def run(self):
        counter=0

        print ("Finding Txn for: " + self.wallet)
        searchWalletUC=self.wallet.upper()

        while self.runThread:

            self.endBlock=w3.eth.blockNumber
            print ("Looking for blocks in range:" + str(self.startBlock) + " to " + str(self.endBlock))

            for blockNo in range(self.startBlock, self.endBlock):

                #send out current block for every xx blocksd
                if counter==500:
                    #TODO emit the current blockNo
                    #print(blockNo)
                    self.currentBlock.emit(blockNo)
                    counter=0
                else:
                    counter = counter + 1

            #   print("------Get BlockNo:" + str(blockNo))
                x=w3.eth.getBlock(blockNo)
                timestamp = x['timestamp']
                # get the timestamp and convert it to useful format
                dateISO=datetime.datetime.fromtimestamp(timestamp).isoformat()
                #print(dateISO)

                for txHash in x['transactions']:

                    txn = w3.eth.getTransaction(txHash)

                    if (txn['from'] != None and txn['from'].upper() == searchWalletUC):
                        txnHashHex = txHash.hex()
                        txnAmt=w3.fromWei(txn['value'], 'ether')
                        txnData=("{},{},{},{},{}".format('To', txn['to'], txnAmt, dateISO, txnHashHex))
                        self.transaction.emit(txnData)
                        #print(txnData)
                    if (txn['to'] != None and txn['to'].upper() == searchWalletUC):
                        txnHashHex = txHash.hex()
                        txnAmt=w3.fromWei(txn['value'], 'ether')
                        txnData=("{},{},{},{},{}".format('From', txn['from'], txnAmt, dateISO, txnHashHex))
                        #print(txnData)
                        self.transaction.emit(txnData)

            # end for loop
            self.startBlock = self.endBlock
             #sleep for xx secs
            time.sleep(60)
        # end while loop
