import threading

from taurus.external.qt.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QLabel, QPushButton
from taurus.qt.qtgui.display import QLed, TaurusLabel
from taurus.external.qt import QtCore
from secondaryWindows import SecondaryWindow


class AttrButtons(QWidget):

    def __init__(self, param, CSVData, device, parent=None):
        QWidget.__init__(self, parent)

        self.widget = None
        self.layout = None
        self.grid = QGridLayout(self)

        self.dictWindows = {}

        self.namesTitle = ["Subsystem", "Attr itlk", "Logic itlk"]
        self.param = param
        self.CSVData = CSVData
        self.device = device

        self._state_column = None
        self.lastState = None

        self.sendingButton = None
        self.buttonName = None
        self.window2 = None

        self.add_titles()
        self.add_elems()

        self.grid.setAlignment(QtCore.Qt.AlignTop)

    def add_titles(self):
        col = 0
        for i in self.namesTitle:
            w = QWidget()
            layout = QHBoxLayout()
            labelTitle = QLabel(i)

            if i == "Subsystem":
                labelTitle.setFixedWidth(250)
                labelTitle.setFixedHeight(30)
                layout.setAlignment(QtCore.Qt.AlignLeft)
            else:
                labelTitle.setFixedWidth(125)
                labelTitle.setFixedHeight(30)
                layout.setAlignment(QtCore.Qt.AlignHCenter)

            # Bold font text:
            # myFont = QtGui.QFont()
            # myFont.setBold(True)
            # labelTitle.setFont(myFont)

            layout.addWidget(labelTitle)

            w.setLayout(layout)
            self.grid.addWidget(w, 0, col, 1, 3)
            col += 1

    def add_elems(self):
        row = 1
        for item in self.param:
            self.widget = QWidget()
            self.layout = QHBoxLayout()

            self.createButtons(item)

            for i in range(len(self.CSVData[1])):
                if self.CSVData[1][i] == item:
                    column = i

            self._state_column = self.getAttrQuality(column)
            self.lastState = self.getLastAttrQuality(column)

            self.createLed(self._state_column, "Any attribute in interlock")

            label = QLabel("     ")
            label.resize(100, 20)
            self.layout.addWidget(label)

            self.createLed(self.lastState, "Logic interlock")

            self.layout.setSpacing(15)
            self.layout.setContentsMargins(0, 0, 0, 40)

            self.widget.setLayout(self.layout)
            self.grid.addWidget(self.widget, row, 0, 2, 3)
            row += 1
        # f.e. This code: "grid.addWidget(button, 2, 0, 1, 2)" adds the button to the gridLayout and places it in row2,
        # column 0, occupying 1 row and 2 columns

    def createLed(self, state, toolTip):
        led = QLed()
        led.setFixedWidth(20)
        led.setFixedHeight(20)
        led.setToolTip(toolTip)
        self.layout.addWidget(led)

        if state is False:
            led.setLedColor("RED")
        else:
            led.setLedColor("GREEN")

    def createButtons(self, item):
        self.buttonName = QPushButton(item)
        self.buttonName.setFixedWidth(125)
        self.buttonName.setFixedHeight(30)
        self.buttonName.clicked.connect(self.openWindow)
        self.layout.setAlignment(QtCore.Qt.AlignLeft)
        self.layout.addWidget(self.buttonName)

    def openWindow(self):
        sender = self.sender()
        column = self.findColumn(sender.text())
        sendState = self.getAttrQuality(column)

        win = SecondaryWindow(sender.text(), column, self.CSVData, sendState)
        self.dictWindows[sender.text()] = win
        win.show()

    # It find the column (and its position) in CSVData that match with the button's name
    def findColumn(self, subtitle):
        csvList = self.CSVData[1]
        for pos, item in enumerate(csvList):
            if item == subtitle:
                return pos

    def getLastAttrQuality(self, column):
        for i in range(2, len(self.CSVData)):
            # if there is an empty space and the previous space is not empty then, we save the previous value as
            # attribute name
            if self.CSVData[i][column] == '' \
                    and self.CSVData[i - 1][column] != '' \
                    and self.CSVData[i - 1][column] != self.CSVData[1][column]:

                attrName = self.CSVData[i - 1][column]
                data = self.device[str(attrName)]

                if str(data.quality) not in ["ATTR_VALID"]:
                    return False
                else:
                    return True

    def getAttrQuality(self, column):
        for i in range(2, len(self.CSVData)):
            if self.CSVData[i][column] != '':
                attrName = self.CSVData[i][column]
                data = self.device[str(attrName)]

                if str(data.quality) not in ["ATTR_VALID"]:
                    return False
                else:
                    return True


class PLCWidget(QWidget):

    def __init__(self, CSVData, parent=None):
        QWidget.__init__(self, parent)

        self.Vlayaout = QVBoxLayout()

        self.CSVData = CSVData
        self.attrNames = None
        self.taurusLabel = None
        self.model = None

        self.add_elems()

        self.Vlayaout.setAlignment(QtCore.Qt.AlignTop)
        self.Vlayaout.setSpacing(0)
        self.setLayout(self.Vlayaout)

    def add_elems(self):
        for i in range(2, len(self.CSVData[0])):
            w = QWidget()
            layout = QHBoxLayout()

            if self.CSVData[i][0] != "":
                self.model = self.CSVData[0][0] + '/' + self.CSVData[i][0]
                self.attrNames = QLabel(self.CSVData[i][0], self)
                layout.addWidget(self.attrNames)

                self.createTaurusLabel(self.model, layout)

                layout.setSpacing(0)
                layout.setContentsMargins(0, 0, 0, 4)
                w.setLayout(layout)

                self.Vlayaout.addWidget(w)

    def createTaurusLabel(self, model, layout):
        self.taurusLabel = TaurusLabel(self)
        self.taurusLabel.model = model
        self.taurusLabel.setNoneValue("Not found")
        self.taurusLabel.setFixedWidth(100)
        self.taurusLabel.setFixedHeight(25)
        layout.addWidget(self.taurusLabel)





