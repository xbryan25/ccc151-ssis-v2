from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import Qt

import csv

from programs.edit_program_design import Ui_Dialog as EditProgramUI

from helper_dialogs.edit_item_state.fail_to_edit_item import FailToEditItemDialog
from helper_dialogs.edit_item_state.success_edit_item import SuccessEditItemDialog

from utils.is_valid_verifiers import IsValidVerifiers
from utils.get_information_codes import GetInformationCodes
from utils.get_existing_information import GetExistingInformation
from utils.is_valid_edit_value import IsValidEditValue


class EditProgramDialog(QDialog, EditProgramUI):
    def __init__(self, programs_table_view, programs_table_model):
        super().__init__()

        self.setupUi(self)

        self.programs_table_view = programs_table_view
        self.programs_table_model = programs_table_model
        self.data_from_csv = programs_table_model.data_from_csv

        self.is_valid = IsValidVerifiers()
        self.is_valid_edit_value = IsValidEditValue()
        self.get_information_codes = GetInformationCodes()
        self.programs_information = GetExistingInformation().from_programs()

        self.add_program_codes_to_combobox()
        self.add_college_codes_to_combobox()

        self.edit_program_button.clicked.connect(self.edit_program_information)

        self.program_to_edit_combobox.currentTextChanged.connect(self.enable_edit_fields)
        self.program_to_edit_combobox.currentTextChanged.connect(self.set_old_data_as_placeholders)

        self.set_college_code_combobox_scrollbar()

    def edit_program_information(self):
        issues = []

        if not self.is_valid.program_code(self.new_program_code_lineedit.text().strip(), edit_state=True):
            issues.append("Program code is not in the correct format")
        elif (self.new_program_code_lineedit.text()).strip() in self.programs_information["Program Code"]:
            issues.append("Program code already exists")

        if not self.is_valid.program_name(self.new_program_name_lineedit.text().strip(), edit_state=True):
            issues.append("Program name is not in the correct format")
        elif self.new_program_name_lineedit.text().strip() in self.programs_information["Program Name"]:
            issues.append("Program name already exists")

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

            # Check if there are any changes made from the old data of the program
            if self.data_from_csv[row_to_edit] != program_to_edit:

                # By doing this, the data in the model also gets updated, same reference
                self.data_from_csv[row_to_edit] = program_to_edit

                with open("../databases/programs.csv", 'w', newline='') as from_programs_csv:
                    writer = csv.writer(from_programs_csv)

                    writer.writerows(self.data_from_csv)

                self.success_edit_item_dialog = SuccessEditItemDialog("program", self)

                self.success_edit_item_dialog.exec()
            else:
                print("No changes made")

    def add_program_codes_to_combobox(self):
        for program_code in self.get_information_codes.for_programs():
            self.program_to_edit_combobox.addItem(program_code)

    def add_college_codes_to_combobox(self):
        for college_code in self.get_information_codes.for_colleges():
            self.new_college_code_combobox.addItem(college_code)

    def set_college_code_combobox_scrollbar(self):
        self.new_college_code_combobox.view().setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    def enable_edit_fields(self, program_code):

        if program_code != "--Select Program Code--" and program_code in self.programs_information["Program Code"]:
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
        for program in self.programs_table_model.data_from_csv:
            if program[0] == self.program_to_edit_combobox.currentText():
                self.new_program_code_lineedit.setPlaceholderText(program[0])
                self.new_program_name_lineedit.setPlaceholderText(program[1])
                self.new_college_code_combobox.setCurrentText(program[2])

    def row_to_edit(self):
        for program in self.programs_table_model.data_from_csv:
            if program[0] == self.program_to_edit_combobox.currentText():
                return self.programs_table_model.data_from_csv.index(program)

