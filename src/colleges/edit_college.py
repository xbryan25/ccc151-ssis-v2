from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import Qt

import csv

from colleges.edit_college_design import Ui_Dialog as EditCollegeUI

from helper_dialogs.edit_item_state.fail_to_edit_item import FailToEditItemDialog
from helper_dialogs.edit_item_state.success_edit_item import SuccessEditItemDialog

from utils.is_valid_verifiers import IsValidVerifiers
from utils.get_information_codes import GetInformationCodes
from utils.get_existing_information import GetExistingInformation
from utils.is_valid_edit_value import IsValidEditValue


class EditCollegeDialog(QDialog, EditCollegeUI):
    def __init__(self, college_table_view, college_table_model):
        super().__init__()

        self.setupUi(self)

        self.college_table_view = college_table_view
        self.college_table_model = college_table_model
        self.data_from_csv = college_table_model.data_from_csv

        self.is_valid = IsValidVerifiers()
        self.is_valid_edit_value = IsValidEditValue()
        self.get_information_codes = GetInformationCodes()
        self.colleges_information = GetExistingInformation().from_colleges()

        self.add_college_codes_to_combobox()

        self.edit_college_button.clicked.connect(self.edit_college_information)

        self.college_to_edit_combobox.currentTextChanged.connect(self.enable_edit_fields)
        self.college_to_edit_combobox.currentTextChanged.connect(self.set_old_data_as_placeholders)

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

            # Check if there are any changes made from the old data of the college
            if self.data_from_csv[row_to_edit] != college_to_edit:

                # By doing this, the data in the model also gets updated, same reference
                self.data_from_csv[row_to_edit] = college_to_edit

                with open("../databases/colleges.csv", 'w', newline='') as from_colleges_csv:
                    writer = csv.writer(from_colleges_csv)

                    writer.writerows(self.data_from_csv)

                self.success_edit_item_dialog = SuccessEditItemDialog("college", self)

                self.success_edit_item_dialog.exec()
            else:
                print("No changes made")

    def add_college_codes_to_combobox(self):
        for college_code in self.get_information_codes.for_colleges():
            self.college_to_edit_combobox.addItem(college_code)

    # def set_college_code_combobox_scrollbar(self):
    #     self.new_college_code_combobox.view().setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    def enable_edit_fields(self, college_code):

        if college_code != "--Select College Code--" and college_code in self.colleges_information["College Code"]:
            self.edit_college_button.setEnabled(True)
            self.new_college_code_lineedit.setEnabled(True)
            self.new_college_name_lineedit.setEnabled(True)

        else:
            self.edit_college_button.setEnabled(False)
            self.new_college_code_lineedit.setEnabled(False)
            self.new_college_name_lineedit.setEnabled(False)

    def set_old_data_as_placeholders(self):
        for college in self.college_table_model.data_from_csv:
            if college[0] == self.college_to_edit_combobox.currentText():
                self.new_college_code_lineedit.setPlaceholderText(college[0])
                self.new_college_name_lineedit.setPlaceholderText(college[1])

    def row_to_edit(self):
        for college in self.college_table_model.data_from_csv:
            if college[0] == self.college_to_edit_combobox.currentText():
                return self.college_table_model.data_from_csv.index(college)

