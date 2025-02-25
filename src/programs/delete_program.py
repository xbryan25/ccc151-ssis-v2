from PyQt6.QtWidgets import QDialog, QHeaderView
from PyQt6.QtCore import Qt

from programs.delete_program_design import Ui_Dialog as DeleteProgramUI

from helper_dialogs.delete_item_state.confirm_delete import ConfirmDeleteDialog
from helper_dialogs.delete_item_state.success_delete_item import SuccessDeleteItemDialog

from utils.get_information_codes import GetInformationCodes
from utils.get_connections import GetConnections


class DeleteProgramDialog(QDialog, DeleteProgramUI):
    def __init__(self, programs_table_view, programs_table_model, students_table_model, colleges_table_model,
                 reset_item_delegates_func, horizontal_header):

        super().__init__()

        self.setupUi(self)

        self.set_external_stylesheet()

        self.reset_item_delegates_func = reset_item_delegates_func
        self.horizontal_header = horizontal_header

        self.programs_table_view = programs_table_view
        self.programs_table_model = programs_table_model

        self.students_table_model = students_table_model
        self.colleges_table_model = colleges_table_model

        self.get_information_codes = GetInformationCodes()
        self.get_connections = GetConnections()

        self.add_program_codes_to_combobox()
        self.add_college_codes_to_combobox()

        self.add_signals()

        self.set_program_to_delete_combobox_scrollbar()
        self.set_college_code_combobox_scrollbar()

    def add_program_codes_to_combobox(self):
        for program_code in self.get_program_codes():
            self.program_to_delete_combobox.addItem(program_code)

    def add_college_codes_to_combobox(self):
        for college_code in self.get_college_codes():
            self.college_code_combobox.addItem(college_code)

    def delete_program_from_model(self):
        for program in self.programs_table_model.get_data():
            if program[0] == self.program_to_delete_combobox.currentText():

                program_code_to_delete = self.program_to_delete_combobox.currentText()
                len_of_students_under_program_code = self.len_of_students_under_program_code(program_code_to_delete)

                if len_of_students_under_program_code["students"] == 0:
                    self.confirm_to_delete_dialog = ConfirmDeleteDialog("program", program_code_to_delete)
                else:
                    self.confirm_to_delete_dialog = ConfirmDeleteDialog("program",
                                                                        program_code_to_delete,
                                                                        num_of_affected=
                                                                        len_of_students_under_program_code,
                                                                        information_code_affected=True)

                self.confirm_to_delete_dialog.exec()

                confirm_delete_decision = self.confirm_to_delete_dialog.get_confirm_delete_decision()

                if confirm_delete_decision:
                    self.delete_students_who_have_program_code(program_code_to_delete)

                    self.students_table_model.layoutAboutToBeChanged.emit()
                    self.programs_table_model.layoutAboutToBeChanged.emit()

                    self.programs_table_model.get_data().remove(program)

                    self.students_table_model.model_data_is_empty()
                    self.programs_table_model.model_data_is_empty()

                    self.students_table_model.layoutChanged.emit()
                    self.programs_table_model.layoutChanged.emit()

                    self.reset_item_delegates_func("delete_program")

                    if len_of_students_under_program_code["students"] > 0:
                        self.students_table_model.set_has_changes(True)

                    self.programs_table_model.set_has_changes(True)

                    self.program_to_delete_combobox.setCurrentText("--Select Program Code--")

                    self.success_delete_item_dialog = SuccessDeleteItemDialog("program", self)
                    self.success_delete_item_dialog.exec()

    def len_of_students_under_program_code(self, program_code):
        length = {"students": 0}

        for student in self.students_table_model.get_data():
            if student[5] == program_code:
                length["students"] += 1

        return length

    def delete_students_who_have_program_code(self, program_code):
        new_data_from_model = []

        for student in self.students_table_model.get_data():
            if student[5] != program_code:
                new_data_from_model.append(student)

        self.students_table_model.layoutAboutToBeChanged.emit()
        self.students_table_model.set_data(new_data_from_model)
        self.students_table_model.layoutChanged.emit()

    def filter_program_codes(self):
        college_code = self.college_code_combobox.currentText()

        self.reset_program_code_combobox()

        if college_code != "--Select a college--" and college_code in self.get_college_codes():
            self.add_program_codes_from_a_college_to_combobox(college_code)
        else:
            self.add_program_codes_to_combobox()

    def add_program_codes_from_a_college_to_combobox(self, college_code):
        num_of_programs = 0

        college_to_program_connections = self.get_college_to_program_connections()

        for program_code in self.get_program_codes():
            if program_code in college_to_program_connections[college_code]:
                self.program_to_delete_combobox.addItem(program_code)

                num_of_programs += 1

        if num_of_programs == 0:
            self.reset_program_code_combobox(has_programs=False)

    def reset_program_code_combobox(self, has_programs=True):
        self.program_to_delete_combobox.clear()

        if has_programs:
            self.program_to_delete_combobox.addItem("--Select a program--")
        else:
            self.program_to_delete_combobox.addItem("--No programs available--")

    def set_program_to_delete_combobox_scrollbar(self):
        self.program_to_delete_combobox.view().setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    def set_college_code_combobox_scrollbar(self):
        self.college_code_combobox.view().setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    def enable_delete_button(self):
        if self.program_to_delete_combobox.currentText() in self.get_program_codes():
            self.delete_program_button.setEnabled(True)
        else:
            self.delete_program_button.setEnabled(False)

    def add_signals(self):
        self.delete_program_button.clicked.connect(self.delete_program_from_model)

        self.college_code_combobox.currentTextChanged.connect(self.filter_program_codes)
        self.program_to_delete_combobox.currentTextChanged.connect(self.enable_delete_button)

    def get_program_codes(self):
        return self.get_information_codes.for_programs(self.programs_table_model.get_data())

    def get_college_codes(self):
        return self.get_information_codes.for_colleges(self.colleges_table_model.get_data())

    def get_program_to_student_connections(self):
        return self.get_connections.in_programs(self.students_table_model.get_data(),
                                                self.programs_table_model.get_data())

    def get_college_to_program_connections(self):
        return self.get_connections.in_programs(self.programs_table_model.get_data(),
                                                self.colleges_table_model.get_data())

    def set_external_stylesheet(self):
        with open("../assets/qss_files/dialog_style.qss", "r") as file:
            self.setStyleSheet(file.read())
