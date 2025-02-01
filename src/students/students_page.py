from PyQt6.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt, QSortFilterProxyModel
import csv

from PyQt6.uic.Compiler.qtproxies import QtCore
from students.students_page_design import Ui_MainWindow as StudentsPageUI

from utils.reset_sorting_state import ResetSortingState
from utils.get_information_codes import GetInformationCodes

from students.add_student import AddStudentDialog

from helper_dialogs.input_prerequisite.input_prerequisite import InputPrerequisiteDialog


class StudentsPage(QMainWindow, StudentsPageUI):
    def __init__(self, main_screen):
        super().__init__()

        self.setupUi(self)
        self.load_students_from_database()

        self.main_screen = main_screen

        self.program_codes = GetInformationCodes.for_programs()

        self.add_student_button.clicked.connect(self.open_add_student_dialog)
        self.back_to_main_button.clicked.connect(self.return_to_main_screen)

        self.adjust_horizontal_header()

        self.columns = [0, 0, 0, 0, 0, 0]

        self.reset_sorting_state_helper = ResetSortingState(self.students_table, Qt.SortOrder.AscendingOrder)

        self.students_table.horizontalHeader().sectionClicked.connect(
            self.reset_sorting_state_helper.reset_sorting_state)

    def open_add_student_dialog(self):
        if not self.program_codes:
            self.input_programs_dialog = InputPrerequisiteDialog("programs")
            self.input_programs_dialog.exec()
        else:
            self.add_student_dialog = AddStudentDialog(self.students_table)
            self.add_student_dialog.exec()

    def load_students_from_database(self):
        with open("databases/students.csv", 'r') as from_students_csv:
            reader = csv.reader(from_students_csv)

            for index, row in enumerate(reader):
                rowPosition = self.students_table.rowCount()
                self.students_table.insertRow(rowPosition)

                order_id = QTableWidgetItem()
                order_id.setData(Qt.ItemDataRole.DisplayRole, index + 1)
                order_id.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

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

                self.students_table.setItem(rowPosition, 0, order_id)
                self.students_table.setItem(rowPosition, 1, id_number)
                self.students_table.setItem(rowPosition, 2, first_name)
                self.students_table.setItem(rowPosition, 3, last_name)
                self.students_table.setItem(rowPosition, 4, year_level)
                self.students_table.setItem(rowPosition, 5, gender)
                self.students_table.setItem(rowPosition, 6, program_code)

            # self.tableWidget.sortItems(0, Qt.SortOrder.DescendingOrder)
            self.students_table.setSortingEnabled(True)
            # self.students_table.hideColumn(0)

    def adjust_horizontal_header(self):
        h_header = self.students_table.horizontalHeader()

        # Hide 'Order ID' column
        h_header.resizeSection(0, 0)
        h_header.resizeSection(1, 90)
        h_header.resizeSection(2, 220)
        h_header.resizeSection(3, 220)
        h_header.resizeSection(4, 90)
        h_header.resizeSection(5, 120)
        h_header.resizeSection(6, 100)

    def return_to_main_screen(self):
        self.main_screen.show()

        self.close()
