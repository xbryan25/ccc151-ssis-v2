from PyQt6.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt, QSortFilterProxyModel, QAbstractTableModel
import csv

from students.students_page_design import Ui_MainWindow as StudentsPageUI

from utils.reset_sorting_state import ResetSortingState
from utils.get_information_codes import GetInformationCodes
from utils.custom_table_model import CustomTableModel

from students.add_student import AddStudentDialog

from helper_dialogs.input_prerequisite.input_prerequisite import InputPrerequisiteDialog


class StudentsPage(QMainWindow, StudentsPageUI):
    def __init__(self, main_screen):
        super().__init__()

        self.setupUi(self)

        self.main_screen = main_screen

        self.program_codes = GetInformationCodes.for_programs()

        self.students_data = self.load_students_from_database()
        self.columns = ["ID Number", "First Name", "Last Name", "Year Level", "Gender", "Program Code"]

        self.students_table_model = CustomTableModel(self.students_data, self.columns)

        self.sort_filter_proxy_model = QSortFilterProxyModel()
        self.sort_filter_proxy_model.setSourceModel(self.students_table_model)
        self.sort_filter_proxy_model.setSortCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.sort_filter_proxy_model.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)

        self.students_table_view.setSortingEnabled(True)
        self.students_table_view.setModel(self.sort_filter_proxy_model)

        self.reset_sorting_state = ResetSortingState(self.sort_filter_proxy_model, self.students_table_model)

        self.add_student_button.clicked.connect(self.open_add_student_dialog)
        self.back_to_main_button.clicked.connect(self.return_to_main_screen)

        self.students_table_view.horizontalHeader().sectionClicked.connect(
            self.reset_sorting_state.reset_sorting_state)

        self.adjust_horizontal_header()

    def open_add_student_dialog(self):
        if not self.program_codes:
            self.input_programs_dialog = InputPrerequisiteDialog("programs")
            self.input_programs_dialog.exec()
        else:
            self.add_student_dialog = AddStudentDialog(self.students_table_view, self.students_table_model)
            self.add_student_dialog.exec()

    def adjust_horizontal_header(self):
        h_header = self.students_table_view.horizontalHeader()

        # self.students_table_view.setColumnHidden(0, True)

        h_header.resizeSection(0, 90)
        h_header.resizeSection(1, 220)
        h_header.resizeSection(2, 220)
        h_header.resizeSection(3, 90)
        h_header.resizeSection(4, 120)
        h_header.resizeSection(5, 100)

    def load_students_from_database(self):
        students_data = []

        with open("databases/students.csv", 'r') as from_students_csv:
            reader = csv.reader(from_students_csv)

            for index, row in enumerate(reader):
                students_data.append(row)

        return students_data

    def return_to_main_screen(self):
        self.main_screen.show()

        self.close()
