
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget

class Ui_Added(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(682, 379)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.textEdit = QtWidgets.QTextEdit(Form)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.textEdit.setFont(font)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.horizontalLayout.addWidget(self.textEdit)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Введенные значения"))

# window to show which parameters added to graph creation
class AddedWindow(QWidget, Ui_Added):
    def __init__(self):
        super(AddedWindow, self).__init__()
        self.setupUi(self)