import json
import web3
from web3 import Web3
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

def checkGethRunning():
	#check geth connection
	if(not w3.isConnected()):
		return False
	else:
		return True


def verifyWallet(fname, pwd):

	with open(fname, 'r') as keyfile:
 		encrypted_key = keyfile.read()
 		try:
 			private_key = w3.eth.account.decrypt(encrypted_key, pwd)
 		except :
 			print ("Incorrect password")
 			return False

	return True

def getPrivKey(UtcFile, passwd):
	with open(UtcFile, 'r') as keyfile:
		encrypted_key = keyfile.read()
		try:
			private_key = w3.eth.account.decrypt(encrypted_key, passwd)
		except:
			print ("Incorrect password")
			return "ERROR"

	return private_key


def getTransactionCount(walletAddr):
	txn=w3.eth.getTransactionCount(walletAddr)
	return txn

def getAmtInWei(amtInt):
	value=w3.toWei(amtInt, 'ether')
	return value

def getGasPrice():
	gp=w3.eth.gasPrice
	return gp

def toChecksumAddr(inWallet):

	wallet=w3.toChecksumAddress(inWallet)
	return wallet

def getBal(inWallet):

	# run thru checksum to fix lowercase addr otheriwse GetBalance error
	wallet = w3.toChecksumAddress(inWallet)
	bal=w3.fromWei(w3.eth.getBalance(wallet), 'ether')

	return bal


def getAddrfromFile(fname):
	try:
		with open(fname, 'r') as fp:
			obj = json.load(fp)

	except ValueError:
		print ("getAddrFromFile::error loading JSON")

	addr = obj["address"]


	return addr
