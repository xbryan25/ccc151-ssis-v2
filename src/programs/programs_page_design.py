# Form implementation generated from reading ui file 'programs_page.ui'
#
# Created by: PyQt6 UI code generator 6.8.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(700, 580)
        MainWindow.setMinimumSize(QtCore.QSize(700, 580))
        MainWindow.setMaximumSize(QtCore.QSize(700, 580))
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(180, 10, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout.addItem(spacerItem, 7, 5, 1, 1)
        self.edit_program_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.edit_program_button.setMinimumSize(QtCore.QSize(150, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.edit_program_button.setFont(font)
        self.edit_program_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.edit_program_button.setObjectName("edit_program_button")
        self.gridLayout.addWidget(self.edit_program_button, 5, 3, 1, 2)
        self.back_to_main_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.back_to_main_button.setMinimumSize(QtCore.QSize(180, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.back_to_main_button.setFont(font)
        self.back_to_main_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.back_to_main_button.setObjectName("back_to_main_button")
        self.gridLayout.addWidget(self.back_to_main_button, 1, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout.addItem(spacerItem1, 2, 4, 1, 1)
        self.search_input_lineedit = QtWidgets.QLineEdit(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.search_input_lineedit.sizePolicy().hasHeightForWidth())
        self.search_input_lineedit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.search_input_lineedit.setFont(font)
        self.search_input_lineedit.setObjectName("search_input_lineedit")
        self.gridLayout.addWidget(self.search_input_lineedit, 1, 4, 1, 2)
        self.search_type_combobox = QtWidgets.QComboBox(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.search_type_combobox.setFont(font)
        self.search_type_combobox.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.search_type_combobox.setEditable(False)
        self.search_type_combobox.setObjectName("search_type_combobox")
        self.search_type_combobox.addItem("")
        self.search_type_combobox.addItem("")
        self.search_type_combobox.addItem("")
        self.gridLayout.addWidget(self.search_type_combobox, 1, 3, 1, 1)
        self.delete_program_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.delete_program_button.setMinimumSize(QtCore.QSize(150, 30))
        self.delete_program_button.setMaximumSize(QtCore.QSize(150, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.delete_program_button.setFont(font)
        self.delete_program_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.delete_program_button.setObjectName("delete_program_button")
        self.gridLayout.addWidget(self.delete_program_button, 6, 2, 1, 2)
        self.add_program_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.add_program_button.setMinimumSize(QtCore.QSize(150, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.add_program_button.setFont(font)
        self.add_program_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.add_program_button.setObjectName("add_program_button")
        self.gridLayout.addWidget(self.add_program_button, 5, 1, 1, 2)
        self.serach_label = QtWidgets.QLabel(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.serach_label.setFont(font)
        self.serach_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.serach_label.setObjectName("serach_label")
        self.gridLayout.addWidget(self.serach_label, 1, 2, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout.addItem(spacerItem2, 0, 4, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(180, 10, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout.addItem(spacerItem3, 4, 0, 1, 1)
        self.programs_table_view = QtWidgets.QTableView(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.programs_table_view.setFont(font)
        self.programs_table_view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.programs_table_view.setObjectName("programs_table_view")
        self.programs_table_view.horizontalHeader().setMinimumSectionSize(100)
        self.programs_table_view.verticalHeader().setVisible(False)
        self.gridLayout.addWidget(self.programs_table_view, 3, 0, 1, 6)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.search_type_combobox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.edit_program_button.setText(_translate("MainWindow", "Edit program"))
        self.back_to_main_button.setText(_translate("MainWindow", "Go back to main screen"))
        self.search_input_lineedit.setPlaceholderText(_translate("MainWindow", "Input Program Code"))
        self.search_type_combobox.setItemText(0, _translate("MainWindow", "Program Code"))
        self.search_type_combobox.setItemText(1, _translate("MainWindow", "Program Name"))
        self.search_type_combobox.setItemText(2, _translate("MainWindow", "College Code"))
        self.delete_program_button.setText(_translate("MainWindow", "Delete program"))
        self.add_program_button.setText(_translate("MainWindow", "Add program"))
        self.serach_label.setText(_translate("MainWindow", "Search by"))
