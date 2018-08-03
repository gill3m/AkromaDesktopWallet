from PyQt4 import QtGui

from enum import Enum


class MessageType(Enum):
    Info = 1
    Warn = 2
    Error = 3
    Critical = 4


def displayMessage(type, text, informText):

    if type == MessageType.Warn:
        icon=QtGui.QMessageBox.Warning
    else : 
        icon=QtGui.QMessageBox.Information

    msg = QtGui.QMessageBox()
    msg.setIcon(icon)
    msg.setText(text)
    msg.setInformativeText(informText)
    msg.setStandardButtons(QtGui.QMessageBox.Ok)
    msg.exec_()
