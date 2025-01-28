# Form implementation generated from reading ui file 'add_student.ui'
#
# Created by: PyQt6 UI code generator 6.8.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(350, 400)
        Dialog.setMinimumSize(QtCore.QSize(350, 400))
        Dialog.setMaximumSize(QtCore.QSize(350, 400))
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.add_student_button = QtWidgets.QPushButton(parent=Dialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.add_student_button.setFont(font)
        self.add_student_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.add_student_button.setObjectName("add_student_button")
        self.gridLayout.addWidget(self.add_student_button, 4, 0, 1, 1)
        self.header_label = QtWidgets.QLabel(parent=Dialog)
        self.header_label.setMinimumSize(QtCore.QSize(0, 50))
        self.header_label.setMaximumSize(QtCore.QSize(400, 50))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.header_label.setFont(font)
        self.header_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.header_label.setObjectName("header_label")
        self.gridLayout.addWidget(self.header_label, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout.addItem(spacerItem, 5, 0, 1, 1)
        self.frame = QtWidgets.QFrame(parent=Dialog)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gender_label = QtWidgets.QLabel(parent=self.frame)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.gender_label.setFont(font)
        self.gender_label.setObjectName("gender_label")
        self.gridLayout_2.addWidget(self.gender_label, 5, 1, 1, 1)
        self.program_code_lineedit = QtWidgets.QLineEdit(parent=self.frame)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.program_code_lineedit.setFont(font)
        self.program_code_lineedit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.program_code_lineedit.setObjectName("program_code_lineedit")
        self.gridLayout_2.addWidget(self.program_code_lineedit, 6, 3, 1, 1)
        self.gender_combobox = QtWidgets.QComboBox(parent=self.frame)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.gender_combobox.setFont(font)
        self.gender_combobox.setObjectName("gender_combobox")
        self.gender_combobox.addItem("")
        self.gender_combobox.addItem("")
        self.gender_combobox.addItem("")
        self.gender_combobox.addItem("")
        self.gridLayout_2.addWidget(self.gender_combobox, 5, 3, 1, 1)
        self.first_name_label = QtWidgets.QLabel(parent=self.frame)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.first_name_label.setFont(font)
        self.first_name_label.setObjectName("first_name_label")
        self.gridLayout_2.addWidget(self.first_name_label, 2, 1, 1, 1)
        self.id_number_label = QtWidgets.QLabel(parent=self.frame)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.id_number_label.setFont(font)
        self.id_number_label.setObjectName("id_number_label")
        self.gridLayout_2.addWidget(self.id_number_label, 1, 1, 1, 1)
        self.year_level_label = QtWidgets.QLabel(parent=self.frame)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.year_level_label.setFont(font)
        self.year_level_label.setObjectName("year_level_label")
        self.gridLayout_2.addWidget(self.year_level_label, 4, 1, 1, 1)
        self.last_name_lineedit = QtWidgets.QLineEdit(parent=self.frame)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.last_name_lineedit.setFont(font)
        self.last_name_lineedit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.last_name_lineedit.setObjectName("last_name_lineedit")
        self.gridLayout_2.addWidget(self.last_name_lineedit, 3, 3, 1, 1)
        self.first_name_lineedit = QtWidgets.QLineEdit(parent=self.frame)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.first_name_lineedit.setFont(font)
        self.first_name_lineedit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.first_name_lineedit.setObjectName("first_name_lineedit")
        self.gridLayout_2.addWidget(self.first_name_lineedit, 2, 3, 1, 1)
        self.id_number_lineedit = QtWidgets.QLineEdit(parent=self.frame)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.id_number_lineedit.setFont(font)
        self.id_number_lineedit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.id_number_lineedit.setObjectName("id_number_lineedit")
        self.gridLayout_2.addWidget(self.id_number_lineedit, 1, 3, 1, 1)
        self.last_name_label = QtWidgets.QLabel(parent=self.frame)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.last_name_label.setFont(font)
        self.last_name_label.setObjectName("last_name_label")
        self.gridLayout_2.addWidget(self.last_name_label, 3, 1, 1, 1)
        self.program_code_label = QtWidgets.QLabel(parent=self.frame)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.program_code_label.setFont(font)
        self.program_code_label.setObjectName("program_code_label")
        self.gridLayout_2.addWidget(self.program_code_label, 6, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(15, 15, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 1, 0, 6, 1)
        spacerItem2 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 1, 4, 6, 1)
        spacerItem3 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_2.addItem(spacerItem3, 1, 2, 6, 1)
        self.year_level_combobox = QtWidgets.QComboBox(parent=self.frame)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.year_level_combobox.setFont(font)
        self.year_level_combobox.setObjectName("year_level_combobox")
        self.year_level_combobox.addItem("")
        self.year_level_combobox.addItem("")
        self.year_level_combobox.addItem("")
        self.year_level_combobox.addItem("")
        self.year_level_combobox.addItem("")
        self.gridLayout_2.addWidget(self.year_level_combobox, 4, 3, 1, 1)
        self.gridLayout.addWidget(self.frame, 2, 0, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout.addItem(spacerItem4, 3, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Add student"))
        self.add_student_button.setText(_translate("Dialog", "Add student"))
        self.header_label.setText(_translate("Dialog", "Input information"))
        self.gender_label.setText(_translate("Dialog", "Gender"))
        self.gender_combobox.setItemText(0, _translate("Dialog", "Male"))
        self.gender_combobox.setItemText(1, _translate("Dialog", "Female"))
        self.gender_combobox.setItemText(2, _translate("Dialog", "Others"))
        self.gender_combobox.setItemText(3, _translate("Dialog", "Prefer not to say"))
        self.first_name_label.setText(_translate("Dialog", "First Name"))
        self.id_number_label.setText(_translate("Dialog", "ID Number"))
        self.year_level_label.setText(_translate("Dialog", "Year Level"))
        self.last_name_label.setText(_translate("Dialog", "Last Name"))
        self.program_code_label.setText(_translate("Dialog", "Program Code"))
        self.year_level_combobox.setItemText(0, _translate("Dialog", "1st"))
        self.year_level_combobox.setItemText(1, _translate("Dialog", "2nd"))
        self.year_level_combobox.setItemText(2, _translate("Dialog", "3rd"))
        self.year_level_combobox.setItemText(3, _translate("Dialog", "4th"))
        self.year_level_combobox.setItemText(4, _translate("Dialog", ">4th"))
