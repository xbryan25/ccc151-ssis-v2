from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

from application.application_window import ApplicationWindow

import ctypes


def main():
    # To show icon in Windows taskbar
    # https://stackoverflow.com/questions/1551605/how-to-set-applications-taskbar-icon-in-windows-7/1552105#1552105
    # @zeroalpha's answer
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('ccc151.ssis.v1')

    app = QApplication([])
    app.setWindowIcon(QIcon("../assets/images/sequence_icon.ico"))

    application_window = ApplicationWindow()

    application_window.show()
    app.exec()

if __name__ == "__main__":
    main()
