from PyQt6.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt
import csv

from programs.programs_page_design import Ui_MainWindow as ProgramsPageUI

from utils.reset_sorting_state import ResetSortingState
from utils.get_information_codes import GetInformationCodes

from programs.add_program import AddProgramDialog

from helper_dialogs.input_prerequisite.input_prerequisite import InputPrerequisiteDialog


class ProgramsPage(QMainWindow, ProgramsPageUI):
    def __init__(self, main_screen):
        super().__init__()

        self.setupUi(self)
        self.load_programs_from_database()

        self.main_screen = main_screen

        self.college_codes = GetInformationCodes.for_colleges()

        self.add_program_button.clicked.connect(self.open_add_program_dialog)
        self.back_to_main_button.clicked.connect(self.return_to_main_screen)

        self.reset_sorting_state_helper = ResetSortingState(self.programs_table, Qt.SortOrder.AscendingOrder)

        self.programs_table.horizontalHeader().sectionClicked.connect(
            self.reset_sorting_state_helper.reset_sorting_state)

    def open_add_program_dialog(self):
        if not self.college_codes:
            self.input_college_dialog = InputPrerequisiteDialog("college")
            self.input_college_dialog.show()
        else:
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

                program_name = QTableWidgetItem(row[1].replace("_", ","))
                program_name.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                college_code = QTableWidgetItem(row[2])
                college_code.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                self.programs_table.setItem(rowPosition, 0, order_id)
                self.programs_table.setItem(rowPosition, 1, program_code)
                self.programs_table.setItem(rowPosition, 2, program_name)
                self.programs_table.setItem(rowPosition, 3, college_code)

            self.programs_table.setSortingEnabled(True)
            self.adjust_horizontal_header()

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


