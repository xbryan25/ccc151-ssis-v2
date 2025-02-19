from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import Qt

from programs.edit_program_design import Ui_Dialog as EditProgramUI

from helper_dialogs.edit_item_state.fail_to_edit_item import FailToEditItemDialog
from helper_dialogs.edit_item_state.success_edit_item import SuccessEditItemDialog
from helper_dialogs.edit_item_state.confirm_edit import ConfirmEditDialog

from utils.is_valid_verifiers import IsValidVerifiers
from utils.get_information_codes import GetInformationCodes
from utils.get_existing_information import GetExistingInformation

import csv


class EditProgramDialog(QDialog, EditProgramUI):
    def __init__(self, programs_table_view, programs_table_model, students_table_model, colleges_table_model,
                 reset_item_delegates_func):
        super().__init__()

        self.setupUi(self)

        self.reset_item_delegates_func = reset_item_delegates_func

        self.students_table_model = students_table_model
        self.colleges_table_model = colleges_table_model

        self.programs_table_view = programs_table_view
        self.programs_table_model = programs_table_model
        self.data_from_programs_model = programs_table_model.data_from_csv

        self.is_valid = IsValidVerifiers()
        self.get_information_codes = GetInformationCodes()
        self.programs_information = GetExistingInformation().from_programs(self.programs_table_model.get_data())

        self.add_program_codes_to_combobox()
        self.add_college_codes_to_combobox()

        self.add_signals()

        self.set_college_code_combobox_scrollbar()

    def edit_program_information(self):
        issues = self.has_issues()

        if issues:
            self.fail_to_edit_item_dialog = FailToEditItemDialog(issues, "program")
            self.fail_to_edit_item_dialog.exec()
        else:
            # If either the new ID number, new first name, or new last name is blank, their
            #   respective placeholder texts will be used

            program_to_edit = [self.new_program_code_lineedit.text()
                               if self.new_program_code_lineedit.text().strip()
                               else self.new_program_code_lineedit.placeholderText(),

                               self.new_program_name_lineedit.text().strip()
                               if self.new_program_name_lineedit.text().strip()
                               else self.new_program_name_lineedit.placeholderText(),

                               self.new_college_code_combobox.currentText()]

            row_to_edit = self.row_to_edit()

            old_program_code = self.program_to_edit_combobox.currentText()

            # If program code is not changed, a different confirm edit dialog will show
            if old_program_code == program_to_edit[0]:
                self.confirm_to_edit_dialog = ConfirmEditDialog("program",
                                                                old_program_code)
            else:
                len_of_students_under_program_code = self.len_of_students_under_program_code(old_program_code)

                self.confirm_to_edit_dialog = ConfirmEditDialog("program",
                                                                old_program_code,
                                                                num_of_affected=len_of_students_under_program_code,
                                                                information_code_affected=True)

            # Halts the program as this starts another loop
            self.confirm_to_edit_dialog.exec()

            confirm_edit_decision = self.confirm_to_edit_dialog.get_confirm_edit_decision()

            if confirm_edit_decision:
                self.edit_program_code_of_students(old_program_code, program_to_edit[0])

                # Check if there are any changes made from the old data of the program
                if self.data_from_programs_model[row_to_edit] != program_to_edit:

                    # By doing this, the data in the model also gets updated, same reference
                    self.data_from_programs_model[row_to_edit] = program_to_edit

                    self.programs_table_model.set_has_changes(True)

                    self.reset_item_delegates_func("edit_program")

                    self.success_edit_item_dialog = SuccessEditItemDialog("program", self)
                    self.success_edit_item_dialog.exec()

                else:
                    print("No changes made")
            else:
                print("Cancel edit")

    def add_program_codes_to_combobox(self):
        for program_code in self.get_program_codes():
            self.program_to_edit_combobox.addItem(program_code)

    def add_college_codes_to_combobox(self):
        for college_code in self.get_college_codes():
            self.new_college_code_combobox.addItem(college_code)

    def set_college_code_combobox_scrollbar(self):
        self.new_college_code_combobox.view().setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    def enable_edit_fields(self, program_code):

        if program_code != "--Select Program Code--" and program_code in self.get_program_codes():
            self.edit_program_button.setEnabled(True)
            self.new_program_code_lineedit.setEnabled(True)
            self.new_program_name_lineedit.setEnabled(True)
            self.new_college_code_combobox.setEnabled(True)

        else:
            self.edit_program_button.setEnabled(False)
            self.new_program_code_lineedit.setEnabled(False)
            self.new_program_name_lineedit.setEnabled(False)
            self.new_college_code_combobox.setEnabled(False)

    def set_old_data_as_placeholders(self):
        for program in self.programs_table_model.get_data():
            if program[0] == self.program_to_edit_combobox.currentText():
                self.new_program_code_lineedit.setPlaceholderText(program[0])
                self.new_program_name_lineedit.setPlaceholderText(program[1])
                self.new_college_code_combobox.setCurrentText(program[2])

    def row_to_edit(self):
        program_codes = self.get_program_codes()

        for program_code in program_codes:
            if program_code == self.program_to_edit_combobox.currentText():
                return program_codes.index(program_code)

    def len_of_students_under_program_code(self, old_program_code):
        length = 0

        for student in self.students_table_model.get_data():
            if student[5] == old_program_code:
                length += 1

        return length

    def edit_program_code_of_students(self, old_program_code, new_program_code):
        for student in self.students_table_model.get_data():
            if student[5] == old_program_code:
                student[5] = new_program_code

    def add_signals(self):
        self.edit_program_button.clicked.connect(self.edit_program_information)

        self.program_to_edit_combobox.currentTextChanged.connect(self.enable_edit_fields)
        self.program_to_edit_combobox.currentTextChanged.connect(self.set_old_data_as_placeholders)

    def has_issues(self):
        issues = []

        if not self.is_valid.program_code(self.new_program_code_lineedit.text().strip(), edit_state=True):
            issues.append("Program code is not in the correct format")
        elif (self.new_program_code_lineedit.text()).strip() in self.programs_information["Program Code"]:
            issues.append("Program code already exists")

        if not self.is_valid.program_name(self.new_program_name_lineedit.text().strip(), edit_state=True):
            issues.append("Program name is not in the correct format")
        elif self.new_program_name_lineedit.text().strip() in self.programs_information["Program Name"]:
            issues.append("Program name already exists")

        return issues

    def get_student_codes(self):
        return self.get_information_codes.for_students(self.students_table_model.get_data())

    def get_program_codes(self):
        return self.get_information_codes.for_programs(self.programs_table_model.get_data())

    def get_college_codes(self):
        return self.get_information_codes.for_colleges(self.colleges_table_model.get_data())
