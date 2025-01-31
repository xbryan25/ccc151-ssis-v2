from PyQt6.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt
import csv

from programs.programs_page_design import Ui_MainWindow as ProgramsPageUI

from utils.reset_sorting_state import ResetSortingState

# from programs.add_student import AddStudentDialog


class ProgramsPage(QMainWindow, ProgramsPageUI):
    def __init__(self, main_screen):
        super().__init__()

        self.setupUi(self)
        self.load_programs_from_database()

        self.main_screen = main_screen

        self.add_program_button.clicked.connect(self.open_add_program_dialog)
        self.back_to_main_button.clicked.connect(self.return_to_main_screen)

        self.reset_sorting_state_helper = ResetSortingState(self.programs_table, Qt.SortOrder.AscendingOrder)

        self.programs_table.horizontalHeader().sectionClicked.connect(
            self.reset_sorting_state_helper.reset_sorting_state)

    def open_add_program_dialog(self):
        self.add_program_dialog = AddProgramDialog(self.programs_table)
        self.add_program_dialog.show()

    def load_programs_from_database(self):
        with open("databases/programs.csv", 'r') as from_programs_csv:
            reader = csv.reader(from_programs_csv)

            for index, row in enumerate(reader):
                rowPosition = self.programs_table.rowCount()
                self.programs_table.insertRow(rowPosition)

                order_id = QTableWidgetItem()
                order_id.setData(Qt.ItemDataRole.DisplayRole, index + 1)
                order_id.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                program_code = QTableWidgetItem(row[0])
                program_code.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                program_name = QTableWidgetItem(row[1])
                program_name.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                college_code = QTableWidgetItem(row[2])
                college_code.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                self.programs_table.setItem(rowPosition, 0, order_id)
                self.programs_table.setItem(rowPosition, 1, program_code)
                self.programs_table.setItem(rowPosition, 2, program_name)
                self.programs_table.setItem(rowPosition, 3, college_code)

            self.programs_table.setSortingEnabled(True)
            self.adjust_horizontal_header()

    # def reset_sorting_state(self, column_number):
    #     # This function determines if a column header has been clicked 3 times consecutively
    #     # If so, then the sort order for that particular column will be removed
    #     # Under the hood, the 'Order ID' column, which is hidden, will just be sorted
    #     # in ascending order
    #
    #     column_header = self.programs_table.horizontalHeaderItem(column_number)
    #
    #     if not self.prev_clicked[0] and not self.prev_clicked[1]:
    #         self.prev_clicked[0] = column_header
    #
    #     elif column_header != self.prev_clicked[0]:
    #         self.prev_clicked[0] = column_header
    #         self.prev_clicked[1] = None
    #
    #     elif column_header == self.prev_clicked[0] and not self.prev_clicked[1]:
    #         self.prev_clicked[1] = column_header
    #
    #     elif column_header == self.prev_clicked[1]:
    #         self.programs_table.sortItems(0, Qt.SortOrder.AscendingOrder)
    #         self.prev_clicked = [None, None]
    #
    #     print(self.prev_clicked)

    def adjust_horizontal_header(self):
        h_header = self.programs_table.horizontalHeader()

        # Hide 'Order ID' column
        h_header.resizeSection(0, 0)

        h_header.resizeSection(1, 100)
        h_header.resizeSection(2, 460)
        h_header.resizeSection(3, 100)

    def return_to_main_screen(self):
        self.main_screen.show()

        self.close()


