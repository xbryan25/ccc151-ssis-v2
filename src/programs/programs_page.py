from PyQt6.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt, QSortFilterProxyModel, QAbstractTableModel
import csv

from programs.programs_page_design import Ui_MainWindow as ProgramsPageUI

from utils.reset_sorting_state import ResetSortingState
from utils.get_information_codes import GetInformationCodes
from utils.custom_table_model import CustomTableModel
from utils.custom_sort_filter_proxy_model import CustomSortFilterProxyModel
from utils.load_information_from_database import LoadInformationFromDatabase

from programs.add_program import AddProgramDialog

from helper_dialogs.input_prerequisite.input_prerequisite import InputPrerequisiteDialog


class ProgramsPage(QMainWindow, ProgramsPageUI):
    def __init__(self, main_screen):
        super().__init__()

        self.setupUi(self)

        self.main_screen = main_screen

        self.college_codes = GetInformationCodes.for_colleges()

        self.programs_data = LoadInformationFromDatabase.get_programs()
        self.columns = ["Program Code", "Program Name", "College Code"]

        self.programs_table_model = CustomTableModel(self.programs_data, self.columns)
        self.sort_filter_proxy_model = CustomSortFilterProxyModel(self.programs_table_model)

        self.programs_table_view.setSortingEnabled(True)
        self.programs_table_view.setModel(self.sort_filter_proxy_model)

        self.reset_sorting_state = ResetSortingState(self.programs_table_model,
                                                     self.programs_table_view)

        self.add_program_button.clicked.connect(self.open_add_program_dialog)
        self.back_to_main_button.clicked.connect(self.return_to_main_screen)

        self.programs_table_view.horizontalHeader().sectionClicked.connect(
            self.reset_sorting_state.reset_sorting_state)

        self.adjust_horizontal_header()

    def open_add_program_dialog(self):
        if not self.college_codes:
            self.input_college_dialog = InputPrerequisiteDialog("college")
            self.input_college_dialog.exec()
        else:
            self.add_program_dialog = AddProgramDialog(self.programs_table_view, self.programs_table_model)
            self.add_program_dialog.exec()

    def adjust_horizontal_header(self):
        h_header = self.programs_table_view.horizontalHeader()

        h_header.resizeSection(0, 100)
        h_header.resizeSection(1, 460)
        h_header.resizeSection(2, 100)

    def return_to_main_screen(self):
        self.main_screen.show()

        self.close()

