# Form implementation generated from reading ui file 'success_add_item.ui'
#
# Created by: PyQt6 UI code generator 6.8.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(450, 103)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(450, 103))
        Dialog.setMaximumSize(QtCore.QSize(450, 103))
        Dialog.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 2)
        self.proceed_button = QtWidgets.QPushButton(parent=Dialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.proceed_button.setFont(font)
        self.proceed_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.proceed_button.setObjectName("proceed_button")
        self.gridLayout.addWidget(self.proceed_button, 2, 0, 1, 2)
        self.message_label = QtWidgets.QLabel(parent=Dialog)
        self.message_label.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.message_label.setFont(font)
        self.message_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.message_label.setObjectName("message_label")
        self.gridLayout.addWidget(self.message_label, 0, 0, 1, 2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Success!"))
        self.proceed_button.setText(_translate("Dialog", "Click here to proceed"))
        self.message_label.setText(_translate("Dialog", ""))
