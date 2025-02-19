from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import Qt

import csv

from students.edit_student_design import Ui_Dialog as EditStudentUI

from helper_dialogs.edit_item_state.fail_to_edit_item import FailToEditItemDialog
from helper_dialogs.edit_item_state.success_edit_item import SuccessEditItemDialog
from helper_dialogs.edit_item_state.confirm_edit import ConfirmEditDialog

from utils.is_valid_verifiers import IsValidVerifiers
from utils.get_information_codes import GetInformationCodes
from utils.get_existing_information import GetExistingInformation
from utils.get_connections import GetConnections


class EditStudentDialog(QDialog, EditStudentUI):
    def __init__(self, students_table_view, students_table_model, programs_table_model, colleges_table_model,
                 reset_item_delegates_func):

        super().__init__()

        self.setupUi(self)

        self.reset_item_delegates_func = reset_item_delegates_func

        self.programs_table_model = programs_table_model
        self.colleges_table_model = colleges_table_model

        self.students_table_view = students_table_view
        self.students_table_model = students_table_model
        # self.data_from_csv = students_table_model.data_from_csv

        self.is_valid = IsValidVerifiers()
        self.get_information_codes = GetInformationCodes()
        self.get_connections = GetConnections()
        self.students_information = GetExistingInformation().from_students(self.students_table_model.get_data())

        self.add_id_numbers_to_combobox()
        self.add_program_codes_to_combobox()
        self.add_college_codes_to_combobox()

        self.add_signals()

        self.set_program_code_combobox_scrollbar()

    def edit_student_information(self):
        issues = self.find_issues()

        if issues:
            self.fail_to_edit_item_dialog = FailToEditItemDialog(issues, "student")
            self.fail_to_edit_item_dialog.exec()
        else:
            # If either the new ID number, new first name, or new last name is blank, their
            #   respective placeholder texts will be used

            student_to_edit = [self.new_id_number_lineedit.text()
                               if self.new_id_number_lineedit.text().strip()
                               else self.new_id_number_lineedit.placeholderText(),

                               self.new_first_name_lineedit.text().strip()
                               if self.new_first_name_lineedit.text().strip()
                               else self.new_first_name_lineedit.placeholderText(),

                               self.new_last_name_lineedit.text().strip() if self.new_last_name_lineedit.text().strip()
                               else self.new_last_name_lineedit.placeholderText(),

                               self.new_year_level_combobox.currentText(),
                               self.new_gender_combobox.currentText(),
                               self.new_program_code_combobox.currentText()]

            row_to_edit = self.row_to_edit()

            old_student_id_number = self.student_to_edit_combobox.currentText()
            self.confirm_to_edit_dialog = ConfirmEditDialog("student",
                                                            old_student_id_number)

            # Halts the program where as this starts another loop
            self.confirm_to_edit_dialog.exec()

            confirm_edit_decision = self.confirm_to_edit_dialog.get_confirm_edit_decision()

            if confirm_edit_decision:
                # Check if there are any changes made from the old data of the student
                if self.students_table_model.get_data()[row_to_edit] != student_to_edit:

                    # By doing this, the data in the model also gets updated, same reference
                    self.students_table_model.get_data()[row_to_edit] = student_to_edit

                    self.students_table_model.set_has_changes(True)

                    self.reset_item_delegates_func("edit_student")

                    self.success_edit_item_dialog = SuccessEditItemDialog("student", self)
                    self.success_edit_item_dialog.exec()
                else:
                    print("No changes made")
            else:
                print("no changes made")

    def add_id_numbers_to_combobox(self):
        for id_number in self.get_student_id_numbers():
            self.student_to_edit_combobox.addItem(id_number)

    def add_program_codes_to_combobox(self):
        for program_code in self.get_program_codes():
            self.new_program_code_combobox.addItem(program_code)

    def add_college_codes_to_combobox(self):
        for college_code in self.get_college_codes():
            self.college_code_combobox.addItem(college_code)

    def set_program_code_combobox_scrollbar(self):
        self.new_program_code_combobox.view().setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    def enable_edit_fields(self, id_number):
        if id_number != "--Select ID Number--" and id_number in self.get_existing_students()["ID Number"]:
            self.new_id_number_lineedit.setEnabled(True)
            self.new_first_name_lineedit.setEnabled(True)
            self.new_last_name_lineedit.setEnabled(True)
            self.new_year_level_combobox.setEnabled(True)
            self.new_gender_combobox.setEnabled(True)
            self.college_code_combobox.setEnabled(True)
            self.new_program_code_combobox.setEnabled(True)

            # No need to check the other comboboxes
            if self.new_year_level_combobox.currentText() == "":

                # Remove "" in comboboxes
                self.new_year_level_combobox.removeItem(0)
                self.new_gender_combobox.removeItem(0)
                self.college_code_combobox.setItemText(0, "--Select a college--")
                self.new_program_code_combobox.removeItem(0)

        else:
            # Add "" in comboboxes
            self.new_year_level_combobox.insertItem(0, "")
            self.new_gender_combobox.insertItem(0, "")
            self.college_code_combobox.setItemText(0, "")
            self.new_program_code_combobox.insertItem(0, "")

            self.new_year_level_combobox.setCurrentIndex(0)
            self.new_gender_combobox.setCurrentIndex(0)
            self.college_code_combobox.setCurrentIndex(0)
            self.new_program_code_combobox.setCurrentIndex(0)

            self.new_id_number_lineedit.setPlaceholderText("")
            self.new_first_name_lineedit.setPlaceholderText("")
            self.new_last_name_lineedit.setPlaceholderText("")

            self.new_id_number_lineedit.setEnabled(False)
            self.new_first_name_lineedit.setEnabled(False)
            self.new_last_name_lineedit.setEnabled(False)
            self.new_year_level_combobox.setEnabled(False)
            self.new_gender_combobox.setEnabled(False)
            self.college_code_combobox.setEnabled(False)
            self.new_program_code_combobox.setEnabled(False)

    def enable_edit_button(self, program_code):
        if program_code != "--Select a program--" and program_code != "":
            self.edit_student_button.setEnabled(True)
        else:
            self.edit_student_button.setEnabled(False)

    def set_old_data_as_placeholders(self):
        for student in self.students_table_model.get_data():
            if student[0] == self.student_to_edit_combobox.currentText():
                self.new_id_number_lineedit.setPlaceholderText(student[0])
                self.new_first_name_lineedit.setPlaceholderText(student[1])
                self.new_last_name_lineedit.setPlaceholderText(student[2])
                self.new_year_level_combobox.setCurrentText(student[3])
                self.new_gender_combobox.setCurrentText(student[4])

                # student[5] is the program code
                for program_college_connection in self.get_connections.in_programs(
                        self.programs_table_model.get_data(),
                        self.colleges_table_model.get_data()).items():

                    if student[5] in program_college_connection[1]:
                        self.college_code_combobox.setCurrentText(program_college_connection[0])
                        break

                self.new_program_code_combobox.setCurrentText(student[5])

    def row_to_edit(self):
        for student in self.students_table_model.get_data():
            if student[0] == self.student_to_edit_combobox.currentText():
                return self.students_table_model.get_data().index(student)

    def filter_program_codes(self):
        college_code = self.college_code_combobox.currentText()

        if college_code != "--Select a college--" and college_code in self.get_college_codes():
            self.reset_program_code_combobox()
            self.add_program_codes_from_a_college_to_combobox(college_code)

        elif college_code != "":
            self.reset_program_code_combobox()
            self.add_program_codes_to_combobox()

    def add_program_codes_from_a_college_to_combobox(self, college_code):
        num_of_programs = 0

        college_to_program_connections = self.get_connections.in_programs(self.programs_table_model.get_data(),
                                                                          self.colleges_table_model.get_data())

        for program_code in self.get_program_codes():
            if program_code in college_to_program_connections[college_code]:
                self.new_program_code_combobox.addItem(program_code)

                num_of_programs += 1

        if num_of_programs == 0:
            self.reset_program_code_combobox(has_programs=False)

    def reset_program_code_combobox(self, has_programs=True):
        self.new_program_code_combobox.clear()

        if has_programs:
            self.new_program_code_combobox.addItem("--Select a program--")
        else:
            self.new_program_code_combobox.addItem("--No programs available--")

    def add_signals(self):
        self.edit_student_button.clicked.connect(self.edit_student_information)

        self.student_to_edit_combobox.currentTextChanged.connect(self.enable_edit_fields)
        self.student_to_edit_combobox.currentTextChanged.connect(self.set_old_data_as_placeholders)

        self.new_program_code_combobox.currentTextChanged.connect(self.enable_edit_button)

        self.college_code_combobox.currentTextChanged.connect(self.filter_program_codes)

    def find_issues(self):
        issues = []

        if not self.is_valid.id_number(self.new_id_number_lineedit.text().strip(), edit_state=True):
            issues.append("ID Number is not in the correct format")
        elif (self.new_id_number_lineedit.text()).strip() in self.get_existing_students()["ID Number"]:
            issues.append("ID Number already exists")

        if not self.is_valid.first_name(self.new_first_name_lineedit.text().strip(), edit_state=True):
            issues.append("First name is not in the correct format")

        if not self.is_valid.last_name(self.new_last_name_lineedit.text().strip(), edit_state=True):
            issues.append("Last name is not in the correct format")

        full_name = f"{(self.new_first_name_lineedit.text()).strip()} {(self.new_last_name_lineedit.text()).strip()}"
        if full_name in self.get_existing_students()["Full Name"]:
            issues.append("Name combination already exists")

        return issues

    def get_existing_students(self):
        return GetExistingInformation().from_students(self.students_table_model.get_data())

    def get_student_id_numbers(self):
        return self.get_information_codes.for_students(self.students_table_model.get_data())

    def get_program_codes(self):
        return self.get_information_codes.for_programs(self.programs_table_model.get_data())

    def get_college_codes(self):
        return self.get_information_codes.for_colleges(self.colleges_table_model.get_data())
