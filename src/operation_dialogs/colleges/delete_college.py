from PyQt6.QtWidgets import QDialog, QHeaderView
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QFontDatabase

from operation_dialogs.colleges.delete_college_design import Ui_Dialog as DeleteCollegeUI

from helper_dialogs.delete_item_state.confirm_delete import ConfirmDeleteDialog
from helper_dialogs.delete_item_state.success_delete_item import SuccessDeleteItemDialog

from utils.get_information_codes import GetInformationCodes
from utils.get_connections import GetConnections


class DeleteCollegeDialog(QDialog, DeleteCollegeUI):
    def __init__(self, colleges_table_view, colleges_table_model, students_table_model, programs_table_model,
                 reset_item_delegates_func, horizontal_header):

        super().__init__()

        self.setupUi(self)

        self.set_external_stylesheet()
        self.load_fonts()

        self.reset_item_delegates_func = reset_item_delegates_func
        self.horizontal_header = horizontal_header

        self.students_table_model = students_table_model
        self.programs_table_model = programs_table_model

        self.colleges_table_view = colleges_table_view
        self.colleges_table_model = colleges_table_model

        self.get_information_codes = GetInformationCodes()
        self.get_connections = GetConnections()

        self.add_college_codes_to_combobox()

        self.add_signals()

        self.set_college_to_delete_combobox_scrollbar()

    def add_college_codes_to_combobox(self):
        for college_code in self.get_college_codes():
            self.college_to_delete_combobox.addItem(college_code)

    def delete_college_from_model(self):
        for college in self.colleges_table_model.get_data():
            if college[0] == self.college_to_delete_combobox.currentText():

                college_code_to_delete = self.college_to_delete_combobox.currentText()
                quantities_under_college_code = self.len_of_programs_under_college_code(college_code_to_delete)

                if quantities_under_college_code["programs"] == 0:
                    self.confirm_to_delete_dialog = ConfirmDeleteDialog("college", college_code_to_delete)
                else:
                    self.confirm_to_delete_dialog = ConfirmDeleteDialog("college",
                                                                        college_code_to_delete)

                self.confirm_to_delete_dialog.exec()

                confirm_delete_decision = self.confirm_to_delete_dialog.get_confirm_delete_decision()

                if confirm_delete_decision:
                    self.add_na_to_programs(college_code_to_delete)

                    self.students_table_model.layoutAboutToBeChanged.emit()
                    self.programs_table_model.layoutAboutToBeChanged.emit()

                    self.colleges_table_model.delete_entity(college, 'college')

                    self.students_table_model.model_data_is_empty()
                    self.programs_table_model.model_data_is_empty()

                    self.students_table_model.layoutChanged.emit()
                    self.programs_table_model.layoutChanged.emit()
                    self.colleges_table_model.layoutChanged.emit()

                    self.reset_item_delegates_func("delete_college")

                    self.horizontal_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
                    self.horizontal_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

                    if quantities_under_college_code["students"] > 0:
                        self.students_table_model.set_has_changes(True)

                    if quantities_under_college_code["programs"] > 0:
                        self.programs_table_model.set_has_changes(True)

                    self.colleges_table_model.set_has_changes(True)

                    self.college_to_delete_combobox.setCurrentText("--Select College Code--")

                    self.success_delete_item_dialog = SuccessDeleteItemDialog("college", self)
                    self.success_delete_item_dialog.exec()

    def len_of_programs_under_college_code(self, college_code):
        lengths = {"programs": 0, "students": 0}

        for program in self.programs_table_model.get_data():
            if program[2] == college_code:
                lengths["students"] += self.len_of_students_under_program_code(program[0])

                lengths["programs"] += 1

        return lengths

    def len_of_students_under_program_code(self, program_code):
        length = 0

        for student in self.students_table_model.get_data():
            if student[5] == program_code:
                length += 1

        return length

    def add_na_to_programs(self, college_code):
        for program in self.programs_table_model.get_data():
            if program[2] == college_code:
                program[2] = "N/A"

    def set_college_to_delete_combobox_scrollbar(self):
        self.college_to_delete_combobox.view().setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    def enable_delete_button(self):
        if self.college_to_delete_combobox.currentText() in self.get_information_codes.for_colleges(
                self.colleges_table_model.get_data()):

            self.delete_college_button.setEnabled(True)
        else:
            self.delete_college_button.setEnabled(False)

    def add_signals(self):
        self.delete_college_button.clicked.connect(self.delete_college_from_model)
        self.college_to_delete_combobox.currentTextChanged.connect(self.enable_delete_button)

    def get_college_codes(self):
        return self.get_information_codes.for_colleges(self.colleges_table_model.get_data())

    def set_external_stylesheet(self):
        with open("../assets/qss_files/dialog_style.qss", "r") as file:
            self.setStyleSheet(file.read())

    def load_fonts(self):
        self.cg_font_family = QFontDatabase.applicationFontFamilies(0)[0]

        self.header_label.setFont(QFont(self.cg_font_family, 16, QFont.Weight.DemiBold))
        self.college_code_label.setFont(QFont(self.cg_font_family, 12, QFont.Weight.Medium))

        self.college_to_delete_combobox.setStyleSheet(f"""
                                                            QComboBox {{
                                                                font-family: {self.cg_font_family};
                                                                font-size: 15px;
                                                                font-weight: {QFont.Weight.Normal};
                                                            }}
                                                        """)

        self.delete_college_button.setFont(QFont(self.cg_font_family, 20, QFont.Weight.DemiBold))
