"""
This application make it easy to view certain tango attributes with TaurusTrend and its interlocked states.
It is a user GUI created to display device attributes for non-expert users.

* Author: Gabriel Calvo
* Co-author: Saida Humbert
"""

import csv
import sys
import click
import tango

from taurus.external.qt.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QScrollArea
from taurus.external.qt import Qt, QtGui, QtCore
from taurus.qt.qtgui.application import TaurusApplication

from buttons import AttrButtons, PLCWidget

__version__ = "1.0.0"


class MyGUI(Qt.QWidget):

    def __init__(self, parent=None):
        Qt.QWidget.__init__(self, parent)
        # uic.loadUi("./ui/MainWindow0.1.ui", self)

        self.fileCsv = "./resources/epstest16_GUI.csv"
        self.CSVData = self.readFileCsv(self.fileCsv)

        # TODO: to save file name in self.fileCsv / self.CSVData
        # Button upload CSV:
        # self.buttonCSV = QPushButton('Upload CSV', self)
        # self.buttonCSV.clicked.connect(self.uploadCsv)

        self.setWindowTitle(self.CSVData[0][0])
        self.testDevice = tango.DeviceProxy(self.CSVData[0][0])

        self.font = QtGui.QFont()
        self.font.setPointSize(10)
        self.namesList = []

        # window's size max:
        width, height = 500, 1000
        self.setMaximumSize(width, height)
        self.resize(width, height)

        self.scrollWidget = QWidget()
        self.addNamesColumns()

        # Widget AttrButtons:
        self.w = AttrButtons(self.namesList, self.CSVData, self.testDevice)
        # Widget PLCWidget:
        self.w2 = PLCWidget(self.CSVData)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.w2)
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.layout.addWidget(self.w)

        scroll = QScrollArea()
        self.scrollWidget.setLayout(self.layout)
        scroll.setWidget(self.scrollWidget)

        layoutHbox = QHBoxLayout()
        layoutHbox.addWidget(scroll)

        self.setLayout(layoutHbox)

    # TODO: Function for upload a file CSV
    # def uploadCsv(self):
    #     fname = QtGui.QFileDialog.getOpenFileName(self, "Open Data File", "", "CSV data files (*.csv)")
    #     self.fileCsv = fname

    def readFileCsv(self, fileCsv):
        with open(fileCsv) as file:
            reader = csv.reader(file)
            i = 0
            CSVData = []
            for row in reader:
                CSVData.append([])
                for column in row:
                    CSVData[i].append(column)
                i += 1

        return CSVData

    # Other examples CSV:
    # READER:
    # with open(fileCsv) as File:
    #     reader = csv.reader(File, delimiter=',', quotechar=',',
    #                         quoting=csv.QUOTE_MINIMAL)
    #     for row in reader:
    #         print(row)

    # DictReader:
    # CSVData = []
    # with open(fileCsv) as File:
    #     reader = csv.DictReader(File)
    #     for row in reader:
    #         CSVData.append(row)
    #         print(CSVData)

    def addNamesColumns(self):
        for column in range(len(self.CSVData[1])):
            if column % 3 == 0 and not column == 0:
                nameColumn = str(self.CSVData[1][column])
                self.namesList.append(nameColumn)


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
def cli():
    app = TaurusApplication(cmd_line_parser=None)
    gui = MyGUI()
    gui.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    cli()
