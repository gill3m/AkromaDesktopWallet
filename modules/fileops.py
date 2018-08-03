## Copyright (c) 2018 - Akroma Project (www.akroma.io)
from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import QDialog, QFileDialog
from modules.misc_web3 import *
from pathlib import Path
import json
import os
import uic.settingsinfo_ui as settingsinfo_ui

def getTxnHeight(fname):

	walletStore=buildFullPath(fname)
	print("Get Txn height from " + walletStore)
	try:
		with open(walletStore, 'r') as fp:
			obj = json.load(fp)
	except ValueError:
		print ("getTxnHeight::error loading JSON")
		return 0, False;
	blockHeight = obj["blockHeight"]
	return blockHeight, True


def buildFullPath(fname):
	#	acctUC=fname.upper()
	acctUC=fname
	dataDir=getDataDir()
	walletDir=dataDir + "/keystore/"
	walletStore=walletDir + acctUC + ".dat"

	return walletStore


def checkFileExists(filepath):
	ret = os.path.isfile(filepath) 
	return ret
