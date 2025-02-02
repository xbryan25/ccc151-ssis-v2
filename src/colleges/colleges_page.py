from PyQt6.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt
import csv

from colleges.colleges_page_design import Ui_MainWindow as CollegesPageUI

from utils.reset_sorting_state import ResetSortingState
from utils.custom_table_model import CustomTableModel
from utils.custom_sort_filter_proxy_model import CustomSortFilterProxyModel
from utils.load_information_from_database import LoadInformationFromDatabase

from colleges.add_college import AddCollegeDialog

from utils.reset_sorting_state import ResetSortingState


class CollegesPage(QMainWindow, CollegesPageUI):
    def __init__(self, main_screen):
        super().__init__()

        self.setupUi(self)

        self.main_screen = main_screen

        self.colleges_data = LoadInformationFromDatabase.get_colleges()
        self.columns = ["College Code", "College Name"]

        self.colleges_table_model = CustomTableModel(self.colleges_data, self.columns)
        self.sort_filter_proxy_model = CustomSortFilterProxyModel(self.colleges_table_model)

        self.colleges_table_view.setSortingEnabled(True)
        self.colleges_table_view.setModel(self.sort_filter_proxy_model)

        self.reset_sorting_state = ResetSortingState(self.colleges_table_model,
                                                     self.colleges_table_view)

        self.add_college_button.clicked.connect(self.open_add_college_dialog)
        self.back_to_main_button.clicked.connect(self.return_to_main_screen)

        self.colleges_table_view.horizontalHeader().sectionClicked.connect(
            self.reset_sorting_state.reset_sorting_state)

        self.adjust_horizontal_header()

    def open_add_college_dialog(self):
        self.add_college_dialog = AddCollegeDialog(self.colleges_table_view, self.colleges_table_model)
        self.add_college_dialog.exec()

    def adjust_horizontal_header(self):
        h_header = self.colleges_table_view.horizontalHeader()

        h_header.resizeSection(0, 100)
        h_header.resizeSection(1, 530)

    def return_to_main_screen(self):
        self.main_screen.show()

        self.close()
