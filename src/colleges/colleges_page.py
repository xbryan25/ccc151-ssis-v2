from PyQt6.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt
import csv

from colleges.colleges_page_design import Ui_MainWindow as CollegesPageUI

from colleges.add_college import AddCollegeDialog

from utils.reset_sorting_state import ResetSortingState


class CollegesPage(QMainWindow, CollegesPageUI):
    def __init__(self, main_screen):
        super().__init__()

        self.setupUi(self)
        self.load_colleges_from_database()

        self.main_screen = main_screen

        self.add_college_button.clicked.connect(self.open_add_college_dialog)
        self.back_to_main_button.clicked.connect(self.return_to_main_screen)

        self.reset_sorting_state_helper = ResetSortingState(self.colleges_table, Qt.SortOrder.AscendingOrder)

        self.colleges_table.horizontalHeader().sectionClicked.connect(
            self.reset_sorting_state_helper.reset_sorting_state)

    def open_add_college_dialog(self):
        self.add_college_dialog = AddCollegeDialog(self.colleges_table)
        self.add_college_dialog.exec()

    def load_colleges_from_database(self):
        with open("databases/colleges.csv", 'r') as from_colleges_csv:
            reader = csv.reader(from_colleges_csv)

            for index, row in enumerate(reader):
                rowPosition = self.colleges_table.rowCount()
                self.colleges_table.insertRow(rowPosition)

                order_id = QTableWidgetItem()
                order_id.setData(Qt.ItemDataRole.DisplayRole, index + 1)
                order_id.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                college_code = QTableWidgetItem(row[0])
                college_code.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                college_name = QTableWidgetItem(row[1].replace("_", ","))
                college_name.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                self.colleges_table.setItem(rowPosition, 0, order_id)
                self.colleges_table.setItem(rowPosition, 1, college_code)
                self.colleges_table.setItem(rowPosition, 2, college_name)

            self.colleges_table.setSortingEnabled(True)
            self.adjust_horizontal_header()

    def adjust_horizontal_header(self):
        h_header = self.colleges_table.horizontalHeader()

        # Hide 'Order ID' column
        h_header.resizeSection(0, 0)

        h_header.resizeSection(1, 100)
        h_header.resizeSection(2, 560)

    def return_to_main_screen(self):
        self.main_screen.show()

        self.close()
