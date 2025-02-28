# Form implementation generated from reading ui file 'add_program.ui'
#
# Created by: PyQt6 UI code generator 6.8.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(420, 250)
        Dialog.setMinimumSize(QtCore.QSize(420, 250))
        Dialog.setMaximumSize(QtCore.QSize(420, 250))
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.header_label = QtWidgets.QLabel(parent=Dialog)
        self.header_label.setMinimumSize(QtCore.QSize(200, 50))
        self.header_label.setMaximumSize(QtCore.QSize(400, 50))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.header_label.setFont(font)
        self.header_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.header_label.setObjectName("header_label")
        self.gridLayout.addWidget(self.header_label, 1, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout.addItem(spacerItem, 5, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout.addItem(spacerItem1, 3, 1, 1, 1)
        self.line_1 = QtWidgets.QFrame(parent=Dialog)
        self.line_1.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.line_1.setLineWidth(2)
        self.line_1.setMidLineWidth(2)
        self.line_1.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_1.setObjectName("line_1")
        self.gridLayout.addWidget(self.line_1, 1, 0, 1, 1)
        self.line_2 = QtWidgets.QFrame(parent=Dialog)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.line_2.setLineWidth(2)
        self.line_2.setMidLineWidth(2)
        self.line_2.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 1, 2, 1, 1)
        self.frame = QtWidgets.QFrame(parent=Dialog)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.program_code_lineedit = QtWidgets.QLineEdit(parent=self.frame)
        self.program_code_lineedit.setMinimumSize(QtCore.QSize(200, 23))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.program_code_lineedit.setFont(font)
        self.program_code_lineedit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.program_code_lineedit.setObjectName("program_code_lineedit")
        self.gridLayout_2.addWidget(self.program_code_lineedit, 1, 3, 1, 1)
        self.program_name_lineedit = QtWidgets.QLineEdit(parent=self.frame)
        self.program_name_lineedit.setMinimumSize(QtCore.QSize(200, 23))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.program_name_lineedit.setFont(font)
        self.program_name_lineedit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.program_name_lineedit.setObjectName("program_name_lineedit")
        self.gridLayout_2.addWidget(self.program_name_lineedit, 2, 3, 1, 1)
        self.college_code_label = QtWidgets.QLabel(parent=self.frame)
        self.college_code_label.setMinimumSize(QtCore.QSize(125, 0))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.college_code_label.setFont(font)
        self.college_code_label.setObjectName("college_code_label")
        self.gridLayout_2.addWidget(self.college_code_label, 3, 1, 1, 1)
        self.program_code_label = QtWidgets.QLabel(parent=self.frame)
        self.program_code_label.setMinimumSize(QtCore.QSize(125, 0))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.program_code_label.setFont(font)
        self.program_code_label.setObjectName("program_code_label")
        self.gridLayout_2.addWidget(self.program_code_label, 1, 1, 1, 1)
        self.program_name_label = QtWidgets.QLabel(parent=self.frame)
        self.program_name_label.setMinimumSize(QtCore.QSize(125, 0))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.program_name_label.setFont(font)
        self.program_name_label.setObjectName("program_name_label")
        self.gridLayout_2.addWidget(self.program_name_label, 2, 1, 1, 1)
        self.college_code_combobox = QtWidgets.QComboBox(parent=self.frame)
        self.college_code_combobox.setMinimumSize(QtCore.QSize(200, 23))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.college_code_combobox.setFont(font)
        self.college_code_combobox.setEditable(True)
        self.college_code_combobox.setObjectName("college_code_combobox")
        self.college_code_combobox.addItem("")
        self.gridLayout_2.addWidget(self.college_code_combobox, 3, 3, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(15, 15, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 1, 0, 3, 1)
        spacerItem3 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_2.addItem(spacerItem3, 1, 2, 3, 1)
        spacerItem4 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_2.addItem(spacerItem4, 1, 4, 3, 1)
        self.gridLayout.addWidget(self.frame, 2, 0, 1, 3)
        self.add_program_button = QtWidgets.QPushButton(parent=Dialog)
        self.add_program_button.setEnabled(False)
        self.add_program_button.setMinimumSize(QtCore.QSize(402, 35))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.add_program_button.setFont(font)
        self.add_program_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.add_program_button.setObjectName("add_program_button")
        self.gridLayout.addWidget(self.add_program_button, 4, 0, 1, 3)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Sequence | Add a program"))
        self.header_label.setText(_translate("Dialog", "Input information"))
        self.college_code_label.setText(_translate("Dialog", "College Code"))
        self.program_code_label.setText(_translate("Dialog", "Program Code"))
        self.program_name_label.setText(_translate("Dialog", "Program Name"))
        self.college_code_combobox.setItemText(0, _translate("Dialog", "--Select a college--"))
        self.add_program_button.setText(_translate("Dialog", "Add program"))
