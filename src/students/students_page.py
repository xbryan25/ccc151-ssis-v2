from PyQt6.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt
import csv

from students.students_page_design import Ui_MainWindow as StudentsPageUI

from students.add_student import AddStudentDialog


class StudentsPage(QMainWindow, StudentsPageUI):
    def __init__(self, main_screen):
        super().__init__()

        self.setupUi(self)
        self.add_from_database()

        self.main_screen = main_screen

        self.add_student_button.clicked.connect(self.open_add_student_dialog)
        self.back_to_main_button.clicked.connect(self.return_to_main_screen)

    def open_add_student_dialog(self):
        self.add_student_dialog = AddStudentDialog()
        self.add_student_dialog.show()

    def add_from_database(self):
        with open("databases/students.csv", 'r') as from_students_csv:
            reader = csv.reader(from_students_csv)

            for row in reader:
                rowPosition = self.students_table.rowCount()
                self.students_table.insertRow(rowPosition)

                # item = QTableWidgetItem()
                # item.setData(Qt.ItemDataRole.DisplayRole, row[0])

                self.students_table.setItem(rowPosition, 0, QTableWidgetItem(row[0]))
                self.students_table.setItem(rowPosition, 1, QTableWidgetItem(row[1]))
                self.students_table.setItem(rowPosition, 2, QTableWidgetItem(row[2]))
                self.students_table.setItem(rowPosition, 3, QTableWidgetItem(row[3]))
                self.students_table.setItem(rowPosition, 4, QTableWidgetItem(row[4]))
                self.students_table.setItem(rowPosition, 5, QTableWidgetItem(row[5]))

            # self.tableWidget.sortItems(0, Qt.SortOrder.DescendingOrder)
            self.students_table.setSortingEnabled(True)

    def return_to_main_screen(self):
        self.main_screen.show()

        self.close()


