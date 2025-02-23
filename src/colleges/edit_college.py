from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import Qt

from colleges.edit_college_design import Ui_Dialog as EditCollegeUI

from helper_dialogs.edit_item_state.fail_to_edit_item import FailToEditItemDialog
from helper_dialogs.edit_item_state.success_edit_item import SuccessEditItemDialog
from helper_dialogs.edit_item_state.confirm_edit import ConfirmEditDialog

from utils.is_valid_verifiers import IsValidVerifiers
from utils.get_information_codes import GetInformationCodes
from utils.get_existing_information import GetExistingInformation

import csv


class EditCollegeDialog(QDialog, EditCollegeUI):
    def __init__(self, colleges_table_view, college_table_model, programs_table_model, reset_item_delegates_func):
        super().__init__()

        self.setupUi(self)

        self.set_external_stylesheet()

        self.reset_item_delegates_func = reset_item_delegates_func

        self.programs_table_model = programs_table_model

        self.colleges_table_view = colleges_table_view
        self.colleges_table_model = college_table_model
        self.data_from_csv = college_table_model.get_data()

        self.is_valid = IsValidVerifiers()
        self.get_information_codes = GetInformationCodes()
        self.colleges_information = GetExistingInformation().from_colleges(self.colleges_table_model.get_data())

        self.add_college_codes_to_combobox()

        self.add_signals()

        # self.set_college_code_combobox_scrollbar()

    def edit_college_information(self):
        issues = []

        if not self.is_valid.college_code(self.new_college_code_lineedit.text().strip(), edit_state=True):
            issues.append("College code is not in the correct format")
        elif (self.new_college_code_lineedit.text()).strip() in self.colleges_information["College Code"]:
            issues.append("College code already exists")

        if not self.is_valid.college_name(self.new_college_name_lineedit.text().strip(), edit_state=True):
            issues.append("College name is not in the correct format")
        elif self.new_college_name_lineedit.text().strip() in self.colleges_information["College Name"]:
            issues.append("College name already exists")

        if issues:
            self.fail_to_edit_item_dialog = FailToEditItemDialog(issues, "college")
            self.fail_to_edit_item_dialog.exec()
        else:
            # If either the new ID number, new first name, or new last name is blank, their
            #   respective placeholder texts will be used

            college_to_edit = [self.new_college_code_lineedit.text()
                               if self.new_college_code_lineedit.text().strip()
                               else self.new_college_code_lineedit.placeholderText(),

                               self.new_college_name_lineedit.text().strip()
                               if self.new_college_name_lineedit.text().strip()
                               else self.new_college_name_lineedit.placeholderText()]

            row_to_edit = self.row_to_edit()

            old_college_code = self.college_to_edit_combobox.currentText()


            # If college code is not changed, a different confirm edit dialog will show
            if old_college_code == college_to_edit[0]:
                self.confirm_to_edit_dialog = ConfirmEditDialog("college",
                                                                old_college_code)
            else:
                len_of_programs_under_college_code = self.len_of_programs_under_college_code(old_college_code)

                self.confirm_to_edit_dialog = ConfirmEditDialog("college",
                                                                old_college_code,
                                                                num_of_affected=len_of_programs_under_college_code,
                                                                information_code_affected=True)

            # Halts the program where as this starts another loop
            self.confirm_to_edit_dialog.exec()

            confirm_edit_decision = self.confirm_to_edit_dialog.get_confirm_edit_decision()

            if confirm_edit_decision:
                self.edit_college_code_of_programs(old_college_code, college_to_edit[0])

                # Check if there are any changes made from the old data of the college
                if self.data_from_csv[row_to_edit] != college_to_edit:

                    # By doing this, the data in the model also gets updated, same reference
                    self.data_from_csv[row_to_edit] = college_to_edit

                    self.reset_item_delegates_func("edit_college")

                    self.colleges_table_model.set_has_changes(True)

                    self.success_edit_item_dialog = SuccessEditItemDialog("college", self)

                    self.success_edit_item_dialog.exec()
                else:
                    print("No changes made")
            else:
                print("Cancel edit")

    def add_college_codes_to_combobox(self):
        for college_code in self.get_information_codes.for_colleges(self.colleges_table_model.get_data()):
            self.college_to_edit_combobox.addItem(college_code)

    # def set_college_code_combobox_scrollbar(self):
    #     self.new_college_code_combobox.view().setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    def enable_edit_fields(self, college_code):

        if college_code != "--Select College Code--" and college_code in self.colleges_information["College Code"]:
            self.edit_college_button.setEnabled(True)
            self.new_college_code_lineedit.setEnabled(True)
            self.new_college_name_lineedit.setEnabled(True)

        else:
            self.new_college_code_lineedit.setPlaceholderText("")
            self.new_college_name_lineedit.setPlaceholderText("")

            self.edit_college_button.setEnabled(False)
            self.new_college_code_lineedit.setEnabled(False)
            self.new_college_name_lineedit.setEnabled(False)

    def set_old_data_as_placeholders(self):
        for college in self.colleges_table_model.data_from_csv:
            if college[0] == self.college_to_edit_combobox.currentText():
                self.new_college_code_lineedit.setPlaceholderText(college[0])
                self.new_college_name_lineedit.setPlaceholderText(college[1])

    def row_to_edit(self):
        for college in self.colleges_table_model.data_from_csv:
            if college[0] == self.college_to_edit_combobox.currentText():
                return self.colleges_table_model.data_from_csv.index(college)

    def len_of_programs_under_college_code(self, old_college_code):
        length = 0

        for program in self.programs_table_model.get_data():
            if program[2] == old_college_code:
                length += 1

        return length

    def edit_college_code_of_programs(self, old_college_code, new_college_code):
        for program in self.programs_table_model.get_data():
            if program[2] == old_college_code:
                program[2] = new_college_code

    def add_signals(self):
        self.edit_college_button.clicked.connect(self.edit_college_information)

        self.college_to_edit_combobox.currentTextChanged.connect(self.enable_edit_fields)
        self.college_to_edit_combobox.currentTextChanged.connect(self.set_old_data_as_placeholders)

    def set_external_stylesheet(self):

        with open("../assets/qss_files/dialog_style.qss", "r") as file:
            self.setStyleSheet(file.read())