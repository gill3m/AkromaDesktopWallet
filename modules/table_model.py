import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class MakeTxnTableTest():
    def __init__(self):

        # create table
        self.get_table_data()
        self.table = self.createTable()


    def get_table_data(self):
        self.tabledata = [[1111111,2,3,4,5],
                          [6,7,8,9,10],
                          [11,12,13,14,15],
                          [16,17,18,19,20]]

    def createTable(self):
        # create the view
        tView = QTableView()

        # set the table model
        header = ['', 'From/To', 'Amt', 'Date', 'Txn']
        tablemodel = TxnTableModel(self.tabledata, header, self)
        tView.setModel(tablemodel)

        # set the minimum size
#        tv.setMinimumSize(400, 300)

        # hide grid
        tView.setShowGrid(False)

        # hide vertical header
        vh = tView.verticalHeader()
        vh.setVisible(False)

        # set horizontal header properties
        hh = tView.horizontalHeader()
        hh.setStretchLastSection(True)

        # set column width to fit contents
        tView.resizeColumnsToContents()

        # set row height
        tView.resizeRowsToContents()

        # enable sorting
        tView.setSortingEnabled(False)

        return tView


class TxnTableModel(QAbstractTableModel):
    def __init__(self, datain, headerdata, parent=None):
        """
        Args:
            datain: a list of lists\n
            headerdata: a list of strings
        """
        QAbstractTableModel.__init__(self, parent)
        self.arraydata = datain
        self.headerdata = headerdata

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        if len(self.arraydata) > 0:
            return len(self.arraydata[0])
        return 0

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        return self.arraydata[index.row()][index.column()]

    def setData(self, index, value, role):
        pass         # not sure what to put here

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headerdata[col]
        return None

    def sort(self, Ncol, order):
        """
        Sort table by given column number.
        """
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.arraydata = sorted(self.arraydata, key=operator.itemgetter(Ncol))
        if order == Qt.DescendingOrder:
            self.arraydata.reverse()
        self.emit(SIGNAL("layoutChanged()"))
'''
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MyWindow()
    w.show()
    sys.exit(app.exec_())
'''
