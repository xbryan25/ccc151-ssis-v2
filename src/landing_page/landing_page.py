from PyQt6.QtWidgets import QMainWindow

from landing_page.landing_page_design import Ui_MainWindow as LandingPageUI
from students.students_page import StudentsPage


class LandingPage(QMainWindow, LandingPageUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.students_button.clicked.connect(self.open_students_page)

    def open_students_page(self):
        self.students_page = StudentsPage(self)

        self.students_page.show()

        self.hide()
