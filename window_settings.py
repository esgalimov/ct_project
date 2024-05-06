from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget

from window_error import ErrorWidget
from constants import *


class Ui_Settings(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 151)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.line_n = QtWidgets.QLineEdit(self.widget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.line_n.setFont(font)
        self.line_n.setObjectName("line_n")
        self.horizontalLayout.addWidget(self.line_n)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.line_dt = QtWidgets.QLineEdit(self.widget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.line_dt.setFont(font)
        self.line_dt.setObjectName("line_dt")
        self.horizontalLayout_2.addWidget(self.line_dt)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_3.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_3.addWidget(self.pushButton_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Настройки"))
        self.label.setText(_translate("Form", "N:"))
        self.label_2.setText(_translate("Form", "dt"))
        self.pushButton.setText(_translate("Form", "Применить"))
        self.pushButton_2.setText(_translate("Form", "Отменить"))


# window to change N and DT
class SettingsWindow(QWidget, Ui_Settings):
    def __init__(self):
        global N, DT
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.new_settings)
        self.pushButton_2.clicked.connect(self.close)
        self.error = ErrorWidget()
        self.line_n.setText(str(N))
        self.line_dt.setText(str(DT))

    def new_settings(self):
        global N, DT
        try:
            N = int(self.line_n.text())
            DT = int(self.line_dt.text())
        except ValueError:
            self.error.show()