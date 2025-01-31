from PyQt6.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt
import csv

from students.students_page_design import Ui_MainWindow as StudentsPageUI

from students.add_student import AddStudentDialog


class StudentsPage(QMainWindow, StudentsPageUI):
    def __init__(self, main_screen):
        super().__init__()

        self.setupUi(self)
        self.load_students_from_database()

        self.main_screen = main_screen

        self.add_student_button.clicked.connect(self.open_add_student_dialog)
        self.back_to_main_button.clicked.connect(self.return_to_main_screen)

        self.adjust_horizontal_header()

        # h_header.horizontalHeaderItem(0).sectionClicked.connect(self.onHeaderClicked)

    def open_add_student_dialog(self):
        self.add_student_dialog = AddStudentDialog(self.students_table)
        self.add_student_dialog.show()

    def load_students_from_database(self):
        with open("databases/students.csv", 'r') as from_students_csv:
            reader = csv.reader(from_students_csv)

            for row in reader:
                rowPosition = self.students_table.rowCount()
                self.students_table.insertRow(rowPosition)

                id_number = QTableWidgetItem(row[0])
                id_number.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                first_name = QTableWidgetItem(row[1])
                first_name.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                last_name = QTableWidgetItem(row[2])
                last_name.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                year_level = QTableWidgetItem(row[3])
                year_level.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                gender = QTableWidgetItem(row[4])
                gender.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                program_code = QTableWidgetItem(row[5])
                program_code.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                self.students_table.setItem(rowPosition, 0, id_number)
                self.students_table.setItem(rowPosition, 1, first_name)
                self.students_table.setItem(rowPosition, 2, last_name)
                self.students_table.setItem(rowPosition, 3, year_level)
                self.students_table.setItem(rowPosition, 4, gender)
                self.students_table.setItem(rowPosition, 5, program_code)

            # self.tableWidget.sortItems(0, Qt.SortOrder.DescendingOrder)
            self.students_table.setSortingEnabled(True)

    def adjust_horizontal_header(self):
        h_header = self.students_table.horizontalHeader()
        h_header.resizeSection(0, 90)
        h_header.resizeSection(1, 220)
        h_header.resizeSection(2, 220)
        h_header.resizeSection(3, 90)
        h_header.resizeSection(4, 120)
        h_header.resizeSection(5, 100)

    def return_to_main_screen(self):
        self.main_screen.show()

        self.close()


