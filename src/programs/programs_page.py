from PyQt6.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt
import csv

from programs.programs_page_design import Ui_MainWindow as ProgramsPageUI

# from programs.add_student import AddStudentDialog


class ProgramsPage(QMainWindow, ProgramsPageUI):
    def __init__(self, main_screen):
        super().__init__()

        self.setupUi(self)
        self.load_programs_from_database()

        self.main_screen = main_screen

        self.add_program_button.clicked.connect(self.open_add_program_dialog)
        self.back_to_main_button.clicked.connect(self.return_to_main_screen)

    def open_add_program_dialog(self):
        self.add_program_dialog = AddProgramDialog(self.programs_table)
        self.add_program_dialog.show()

    def load_programs_from_database(self):
        with open("databases/programs.csv", 'r') as from_programs_csv:
            reader = csv.reader(from_programs_csv)

            for row in reader:
                rowPosition = self.programs_table.rowCount()
                self.programs_table.insertRow(rowPosition)

                program_code = QTableWidgetItem(row[0])
                program_code.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                program_name = QTableWidgetItem(row[1])
                program_name.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                college_code = QTableWidgetItem(row[2])
                college_code.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                self.programs_table.setItem(rowPosition, 0, program_code)
                self.programs_table.setItem(rowPosition, 1, program_name)
                self.programs_table.setItem(rowPosition, 2, college_code)

            # self.tableWidget.sortItems(0, Qt.SortOrder.DescendingOrder)
            self.programs_table.setSortingEnabled(True)
            # self.programs_table.resizeColumnsToContents()
            self.adjust_horizontal_header()

    def adjust_horizontal_header(self):
        h_header = self.programs_table.horizontalHeader()
        h_header.resizeSection(0, 100)
        h_header.resizeSection(1, 460)
        h_header.resizeSection(2, 100)

    def return_to_main_screen(self):
        self.main_screen.show()

        self.close()


