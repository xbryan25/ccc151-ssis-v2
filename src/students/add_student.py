from PyQt6.QtWidgets import QDialog, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt

from students.add_student_design import Ui_Dialog as AddStudentUI

from helper_dialogs.add_item_state.fail_add_item import FailAddItemDialog
from helper_dialogs.add_item_state.success_add_item import SuccessAddItemDialog

from utils.is_valid_verifiers import IsValidVerifiers
from utils.get_information_codes import GetInformationCodes
from utils.get_existing_information import GetExistingInformation
from utils.get_connections import GetConnections

import re
import csv


class AddStudentDialog(QDialog, AddStudentUI):
    def __init__(self, students_table_view, students_table_model, programs_table_model, colleges_table_model,
                 reset_item_delegates_func):
        super().__init__()

        self.setupUi(self)

        self.reset_item_delegates_func = reset_item_delegates_func

        self.has_added_student = False

        self.programs_table_model = programs_table_model
        self.colleges_table_model = colleges_table_model

        self.students_table_view = students_table_view
        self.students_table_model = students_table_model

        self.is_valid = IsValidVerifiers()
        self.get_information_codes = GetInformationCodes()
        self.get_existing_information = GetExistingInformation()
        self.get_connections = GetConnections()

        self.add_college_codes_to_combobox()

        self.add_signals()

        self.set_program_code_combobox_scrollbar()
        self.set_college_code_combobox_scrollbar()

    def add_student_to_csv(self):
        issues = self.find_issues()

        if issues:
            self.fail_add_item_dialog = FailAddItemDialog(issues, "student")
            self.fail_add_item_dialog.exec()
        else:
            student_to_add = [self.id_number_lineedit.text(),
                              self.first_name_lineedit.text().strip(),
                              self.last_name_lineedit.text().strip(),
                              self.year_level_combobox.currentText(),
                              self.gender_combobox.currentText(),
                              self.program_code_combobox.currentText()]


            self.add_student_to_table(student_to_add)

            self.students_table_model.set_has_changes(True)

            self.reset_item_delegates_func()

            self.success_add_item_dialog = SuccessAddItemDialog("student", self)
            self.success_add_item_dialog.exec()

    def add_student_to_table(self, student_to_add):
        self.students_table_model.layoutAboutToBeChanged.emit()

        if self.students_table_model.get_data()[0][0] == "":
            self.students_table_model.get_data().pop()

        self.students_table_model.data_from_csv.append(student_to_add)
        self.students_table_model.layoutChanged.emit()

    def add_program_codes_from_a_college_to_combobox(self, college_code):
        num_of_programs = 0

        college_to_program_connections = self.get_connections.in_programs(self.programs_table_model.get_data(),
                                                                          self.colleges_table_model.get_data())

        for program_code in self.get_program_codes():
            if program_code in college_to_program_connections[college_code]:
                self.program_code_combobox.addItem(program_code)

                num_of_programs += 1

        if num_of_programs == 0:
            self.reset_program_code_combobox(has_programs=False)

    def add_college_codes_to_combobox(self):
        for college_code in self.get_college_codes():
            self.college_code_combobox.addItem(college_code)

    def set_program_code_combobox_scrollbar(self):
        self.program_code_combobox.view().setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    def set_college_code_combobox_scrollbar(self):
        self.college_code_combobox.view().setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    def filter_program_codes(self):
        college_code = self.college_code_combobox.currentText()

        if college_code != "--Select a college--" and college_code in self.get_college_codes():

            self.program_code_combobox.setEnabled(True)
            self.reset_program_code_combobox()

            self.add_program_codes_from_a_college_to_combobox(college_code)

        else:
            self.program_code_combobox.setEnabled(False)
            self.program_code_combobox.setCurrentText("")

    def reset_program_code_combobox(self, has_programs=True):
        self.program_code_combobox.clear()

        if has_programs:
            self.program_code_combobox.addItem("--Select a program--")
        else:
            self.program_code_combobox.addItem("--No programs available--")

    def enable_add_button(self):
        if (self.college_code_combobox.currentText() != "--Select a college--" and
                (self.program_code_combobox.currentText() != "--Select a program--" and
                    self.program_code_combobox.currentText() != "--No programs available--")):

            self.add_student_button.setEnabled(True)
        else:
            self.add_student_button.setEnabled(False)

    # def any_changes_made(self):
    #     return self.has_added_student

    def find_issues(self):
        students_information = self.get_existing_students()

        issues = []

        if (self.id_number_lineedit.text()).strip() == "":
            issues.append("ID Number is blank")
        elif not self.is_valid.id_number(self.id_number_lineedit.text()):
            issues.append("ID Number is not in the correct format")
        elif (self.id_number_lineedit.text()).strip() in students_information["ID Number"]:
            issues.append("ID Number has already been taken")

        if (self.first_name_lineedit.text()).strip() == "":
            issues.append("First name is blank")
        elif not self.is_valid.first_name(self.first_name_lineedit.text()):
            issues.append("First name is not in the correct format")

        if (self.last_name_lineedit.text()).strip() == "":
            issues.append("Last name is blank")
        elif not self.is_valid.last_name(self.last_name_lineedit.text()):
            issues.append("Last name is not in the correct format")

        full_name = f"{(self.first_name_lineedit.text()).strip()} {(self.last_name_lineedit.text()).strip()}"
        if full_name in students_information["Full Name"]:
            issues.append("Name combination already exists")

        return issues

    def add_signals(self):
        self.add_student_button.clicked.connect(self.add_student_to_csv)

        self.program_code_combobox.currentTextChanged.connect(self.enable_add_button)
        self.college_code_combobox.currentTextChanged.connect(self.filter_program_codes)

    def get_existing_students(self):
        return self.get_existing_information.from_students(self.students_table_model.get_data())

    def get_program_codes(self):
        return self.get_information_codes.for_programs(self.programs_table_model.get_data())

    def get_college_codes(self):
        return self.get_information_codes.for_colleges(self.colleges_table_model.get_data())
