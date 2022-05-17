import itertools
import tango
import subprocess

from taurus.external.qt.QtWidgets import QVBoxLayout, QHBoxLayout, QCompleter, QScrollArea, QCheckBox, QGridLayout, \
    QMessageBox, QGroupBox, QLabel, QRadioButton
from taurus.external.qt import QtGui, QtCore
from taurus.qt.qtgui.base import TaurusBaseComponent
from taurus.qt.qtgui.display import TaurusLabel, TaurusLed
from taurus.external.qt import uic


class SecondaryWindow(QtGui.QDialog):

    def __init__(self, buttonName, column, CSVData, attrValid):
        QtGui.QDialog.__init__(self)

        uic.loadUi("./ui/Dialog0.1.ui", self)
        self.setWindowTitle(buttonName)
        TaurusBaseComponent.FORMAT = "{:6.4f}"
        TaurusLabel.FORMAT = "{:6.4f}"
        self.font = QtGui.QFont()
        self.font.setPointSize(10)

        # window's size max:
        width, height = 570, 790
        self.setMaximumSize(width, height)
        self.resize(width, height)

        self.column = column
        self.attrValid = attrValid

        self.device = CSVData[0][0]
        self.testDevice = tango.DeviceProxy(self.device)

        self.gridLayout = QGridLayout()
        self.groupBox = QtGui.QGroupBox("")

        self.firstVariableList = []
        self.secondVariableList = []
        self.thirdVariableList = []
        self.fourthVariableList = []

        self.widgetsList = []
        self.nameAttrList = []

        self.nameAttr = []
        self.nameModel = []
        self.secondHeight = 100
        self.containerLayout = QVBoxLayout()
        # self.hboxLayaoutBottom = QHBoxLayout()

        self.searchBar = None

        self.labelCheckBox = None
        self.labelB = None
        self.labelButtonOpen = None
        self.labelButtonClose = None

        self.allCheckBoxes = []
        self.horizontalGroupBox = None
        self.checkBoxInterlock = None
        self.cbSelectSomeAttr = None

        self.createSecondLayout(self.secondHeight, self.gridLayout, column, CSVData)
        self.toDoScroll(self.groupBox, self.gridLayout)

        self.buttonOpenTaurusTrend = None
        self.createButtonTaurusTrend()
        self.buttonOpenTaurusTrend.clicked.connect(self.onClickedButtonTaurusTrend)

        self.createCheckBoxInterlock()
        self.attrDict = self.createDictWidgets()

        self.createCbLogicBlocks()

    def createCbLogicBlocks(self):
        nameCheckbox = 0
        self.dictBlocks = {}
        indexList = []
        t = 1
        for i in self.nameAttrList:
            if i.isdigit():
                indexList.append(self.nameAttrList.index(i))
                nameCheckbox += 1
                self.cbSelectSomeAttr = QCheckBox(str(nameCheckbox), self)
                self.cbSelectSomeAttr.stateChanged.connect(self.onClickedCbSomeAttr)
                self.containerLayout.addWidget(self.cbSelectSomeAttr)

        if len(indexList) == 1:
            self.cbSelectSomeAttr.hide()

        for item in range(len(indexList)):
            index = self.nameAttrList[indexList[item]]
            if item == 0:
                self.dictBlocks[t] = self.nameAttrList[0:self.nameAttrList.index(index)]
            else:
                preIndex = self.nameAttrList[indexList[item - 1]]
                self.dictBlocks[t] = self.nameAttrList[
                                     self.nameAttrList.index(preIndex):self.nameAttrList.index(index)]
            t = t + 1

    def onClickedCbSomeAttr(self):
        senderCb = self.sender()
        w = self.dictBlocks[int(senderCb.text())]

        if senderCb.isChecked():
            for widget in self.attrDict.keys():
                if widget in w and not widget.isdigit():
                    # if not widget.isdigit():
                    print(widget)
                    for item in self.attrDict[widget]:
                        print(item)
                        item.show()
                else:
                    for item in self.attrDict[widget]:
                        item.hide()
        else:
            for widget in self.attrDict.keys():
                for item in self.attrDict[widget]:
                    item.show()

    def splitDict(self, d, num):

        n = len(d) // num  # length of smaller half
        i = iter(d.items())  # alternatively, i = d.iteritems() works in Python 2

        d1 = dict(itertools.islice(i, n))  # grab first n items
        d2 = dict(i)  # grab the rest

        for w in d:
            w.show(d1)
            w.hide(d2)

    def createCheckBoxInterlock(self):
        self.checkBoxInterlock = QCheckBox("Only Interlock", self)
        self.containerLayout.addWidget(self.checkBoxInterlock)
        self.checkBoxInterlock.stateChanged.connect(self.checkBoxChangedAction)

    def createListInterlocks(self):
        listInterlocks = []
        for attr in self.nameAttrList:
            if '_' in attr:
                data = self.testDevice[str(attr)]
                if str(data.quality) != "ATTR_VALID":
                    listInterlocks.append(attr)
        interlocksNotRepeats = list(set(listInterlocks))
        return sorted(interlocksNotRepeats)

    def checkBoxChangedAction(self):
        interlocksNotRepeats = self.createListInterlocks()
        if self.checkBoxInterlock.isChecked():
            pos = 0
            if not self.attrValid:
                for widget in sorted(self.attrDict.keys()):
                    if pos < len(interlocksNotRepeats):
                        if interlocksNotRepeats[pos] in widget:
                            for i in self.attrDict[widget]:
                                i.show()
                            pos += 1
                        else:
                            for i in self.attrDict[widget]:
                                i.hide()
                    else:
                        for i in self.attrDict[widget]:
                            i.hide()
            else:
                QMessageBox.warning(self, 'WARNING', 'There are not attributes in interlock')
                self.checkBoxInterlock.setChecked(False)
        else:
            for widget in self.attrDict.keys():
                for i in self.attrDict[widget]:
                    i.show()

    # Command format f.e.:  taurus trend 'sys/tg_test/1/double_scalar' 'sys/tg_test/1/long64_scalar'
    # This gets the text of the selected checks to open taurus trend
    def onClickedButtonTaurusTrend(self):
        listTaurusTrend = ['taurus', 'trend']
        for i, checkbox in enumerate(self.allCheckBoxes):
            if checkbox.isChecked():
                listTaurusTrend.append(self.device + "/" + checkbox.text())
        if len(listTaurusTrend) > 2:
            subprocess.Popen(listTaurusTrend)
        else:
            QMessageBox.warning(self, 'Selection empty', 'You must select at least one attribute to open TaurusTrend!')

    def configureWidgets(self, nameModel):
        self.labelB.setNoneValue("Not found")
        self.labelB.model = '{}{}'.format(nameModel, '#rvalue.magnitude')

    def openCloseClicked(self):
        sender = self.sender()
        print(sender.objectName())
        if "OPEN" in sender.text():
            self.testDevice.write_attribute(sender.objectName(), 1)
            print("1")
        elif "CLOSE" in sender.text():
            self.testDevice.write_attribute(sender.objectName(), 0)
            print("0")
        else:
            QMessageBox.critical(self, 'ERROR', 'This valve cannot be opened or closed')
            print("ERROR: This valve cannot be opened or closed")

    def createSecondLayout(self, height, gridLayout, column, CSVData):
        pos = 0
        for i in range(2, len(CSVData)):
            # len(CSVData(column)) -> get the row, not the column
            if CSVData[i][column]:
                pos = pos + 1
                self.horizontalGroupBox = QGroupBox()
                self.nameAttr = CSVData[i][column]
                self.nameAttrList.append(self.nameAttr)
                self.nameModel = CSVData[0][0] + '/' + self.nameAttr

                self.labelCheckBox = QCheckBox(self.nameAttr, self)
                self.allCheckBoxes.append(self.labelCheckBox)
                self.addLabel(self.labelCheckBox, self.firstVariableList, 50, height)
            elif CSVData[i][column] == '' \
                    and CSVData[i - 1][column] != '' \
                    and CSVData[i - 1][column] != CSVData[1][column]:
                pos = pos + 1
                self.nameAttrList.append(str(pos))
                self.labelCheckBox = QLabel(self)
                self.addLabel(self.labelCheckBox, self.firstVariableList, 150, height)

                self.labelB = QLabel(self)
                self.addLabel(self.labelB, self.secondVariableList, 300, height)

                self.labelButtonOpen = QLabel("")
                self.addLabel(self.labelButtonOpen, self.thirdVariableList, 350, height)

                self.labelButtonClose = QLabel("")
                self.addLabel(self.labelButtonClose, self.fourthVariableList, 355, height)

            try:
                if CSVData[i][column + 1] == "DI":
                    self.labelB = TaurusLed(self)
                    self.labelB.setFixedWidth(20)
                    self.labelB.setFixedHeight(20)
                    self.configureWidgets(self.nameModel)

                    self.addLabel(self.labelB, self.secondVariableList, 300, self.secondHeight)

                    self.labelButtonOpen = QLabel("")
                    self.addLabel(self.labelButtonOpen, self.thirdVariableList, 350, self.secondHeight)

                    self.labelButtonClose = QLabel("")
                    self.addLabel(self.labelButtonClose, self.fourthVariableList, 355, height)

                elif CSVData[i][column + 1] in ["VALVES"]:
                    self.labelB = TaurusLed(self)
                    self.labelB.setFixedWidth(20)
                    self.labelB.setFixedHeight(20)
                    self.configureWidgets(self.nameModel)
                    self.addLabel(self.labelB, self.secondVariableList, 300, self.secondHeight)

                    self.labelButtonOpen = QtGui.QPushButton("OPEN", self)
                    self.labelButtonOpen.setObjectName(CSVData[i][column])
                    self.addLabel(self.labelButtonOpen, self.thirdVariableList, 350, self.secondHeight)

                    self.labelButtonClose = QtGui.QPushButton("CLOSE", self)
                    self.labelButtonClose.setObjectName(CSVData[i][column])
                    self.addLabel(self.labelButtonClose, self.fourthVariableList, 350, height)

                    self.labelButtonOpen.clicked.connect(self.openCloseClicked)
                    self.labelButtonClose.clicked.connect(self.openCloseClicked)

                elif CSVData[i][column + 1] != "":
                    self.labelB = TaurusLabel(self)
                    self.configureWidgets(self.nameModel)
                    self.confLabel(self.labelB)
                    self.addLabel(self.labelB, self.secondVariableList, 205, height)

                    self.labelButtonOpen = QLabel("")
                    self.addLabel(self.labelButtonOpen, self.thirdVariableList, 350, self.secondHeight)

                    self.labelButtonClose = QLabel("")
                    self.addLabel(self.labelButtonClose, self.fourthVariableList, 350, height)

                # Add the labels in the list into the layout:
                gridLayout.addWidget(self.labelCheckBox, pos, 1)
                gridLayout.addWidget(self.labelB, pos, 2)
                gridLayout.addWidget(self.labelButtonOpen, pos, 3)
                gridLayout.addWidget(self.labelButtonClose, pos, 4)

                height += 25

            except IndexError:
                pass

        self.createSearchBar()

    def confLabel(self, nameLabel):
        nameLabel.setNoneValue("No units")
        nameLabel.setFont(self.font)
        nameLabel.setAutoTrim(False)

    def addLabel(self, nameLabel, variableList, pos, height):
        nameLabel.move(pos, height)
        variableList.append(nameLabel)

    def toDoScroll(self, groupBox, gridLayout):
        gridLayout.setAlignment(QtCore.Qt.AlignTop)
        groupBox.setLayout(gridLayout)
        scroll = QScrollArea()
        scroll.setWidget(groupBox)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(650)
        scroll.setFixedWidth(550)
        self.containerLayout.addWidget(scroll)
        self.setLayout(self.containerLayout)

    def createSearchBar(self):
        self.searchBar = QtGui.QLineEdit()
        self.searchBar.textChanged.connect(self.updateDisplay)
        completer = QCompleter(sorted(set(self.nameAttrList)))
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.searchBar.setCompleter(completer)
        self.containerLayout.addWidget(self.searchBar)

    def createButtonTaurusTrend(self):
        self.buttonOpenTaurusTrend = QtGui.QPushButton("Open Taurus Trend", self)
        self.buttonOpenTaurusTrend.setFixedWidth(160)
        self.containerLayout.addWidget(self.buttonOpenTaurusTrend)

    def updateDisplay(self, text):
        for widget in self.attrDict.keys():
            if text.upper() in widget.upper() and '.' not in widget:
                for i in self.attrDict[widget]:
                    i.show()
            else:
                for i in self.attrDict[widget]:
                    i.hide()

    def createDictWidgets(self):
        newDict = {}
        # f.e. dict = {nameAttribute: widget1, widget2, widget3, widget4}
        i = 1
        listWidgets = list(
            zip(self.nameAttrList,
                self.firstVariableList, self.secondVariableList, self.thirdVariableList, self.fourthVariableList))

        for item in listWidgets:
            keys = item[0]
            values = item[1], item[2], item[3], item[4]
            if keys not in newDict.keys():
                newDict[keys] = values
            else:
                new_key = "{}.{}".format(keys, i)
                i += 1
                newDict[new_key] = values

        return newDict
