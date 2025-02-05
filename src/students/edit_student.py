from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import Qt

import csv

from students.edit_student_design import Ui_Dialog as EditStudentUI

from helper_dialogs.edit_item_state.fail_to_edit_item import FailToEditItemDialog
from helper_dialogs.edit_item_state.success_edit_item import SuccessEditItemDialog

from utils.is_valid_verifiers import IsValidVerifiers
from utils.get_information_codes import GetInformationCodes
from utils.get_existing_information import GetExistingInformation
from utils.is_valid_edit_value import IsValidEditValue


class EditStudentDialog(QDialog, EditStudentUI):
    def __init__(self, students_table_view, students_table_model):
        super().__init__()

        self.setupUi(self)

        self.students_table_view = students_table_view
        self.students_table_model = students_table_model
        self.data_from_csv = students_table_model.data_from_csv

        self.is_valid = IsValidVerifiers()
        self.is_valid_edit_value = IsValidEditValue()
        self.get_information_codes = GetInformationCodes()
        self.students_information = GetExistingInformation().from_students()

        self.add_id_numbers_to_combobox()
        self.add_program_codes_to_combobox()

        self.edit_student_button.clicked.connect(self.edit_student_information)

        self.student_to_edit_combobox.currentTextChanged.connect(self.enable_edit_fields)
        self.student_to_edit_combobox.currentTextChanged.connect(self.set_old_data_as_placeholders)


        self.set_program_code_combobox_scrollbar()

    def edit_student_information(self):
        issues = []

        if not self.is_valid.id_number(self.new_id_number_lineedit.text().strip(), edit_state=True):
            issues.append("ID Number is not in the correct format")
        elif (self.new_id_number_lineedit.text()).strip() in self.students_information["ID Number"]:
            issues.append("ID Number already exists")

        if not self.is_valid.first_name(self.new_first_name_lineedit.text().strip(), edit_state=True):
            issues.append("First name is not in the correct format")

        if not self.is_valid.last_name(self.new_last_name_lineedit.text().strip(), edit_state=True):
            issues.append("Last name is not in the correct format")

        full_name = f"{(self.new_first_name_lineedit.text()).strip()} {(self.new_last_name_lineedit.text()).strip()}"
        if full_name in self.students_information["Full Name"]:
            issues.append("Name combination already exists")

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

            # Check if there are any changes made from the old data of the student
            if self.data_from_csv[row_to_edit] != student_to_edit:

                # By doing this, the data in the model also gets updated, same reference
                self.data_from_csv[row_to_edit] = student_to_edit

                with open("../databases/students.csv", 'w', newline='') as from_students_csv:
                    writer = csv.writer(from_students_csv)

                    writer.writerows(self.data_from_csv)

                self.success_edit_item_dialog = SuccessEditItemDialog("student", self)

                self.success_edit_item_dialog.exec()
            else:
                print("No changes made")


    def add_id_numbers_to_combobox(self):
        for id_number in self.get_information_codes.for_students():
            print(id_number)
            self.student_to_edit_combobox.addItem(id_number)

    def add_program_codes_to_combobox(self):
        for program_code in self.get_information_codes.for_programs():
            self.new_program_code_combobox.addItem(program_code)

    def set_program_code_combobox_scrollbar(self):
        self.new_program_code_combobox.view().setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    def enable_edit_fields(self, id_number):

        if id_number != "--Select ID Number--" and id_number in self.students_information["ID Number"]:
            self.edit_student_button.setEnabled(True)
            self.new_id_number_lineedit.setEnabled(True)
            self.new_first_name_lineedit.setEnabled(True)
            self.new_last_name_lineedit.setEnabled(True)
            self.new_year_level_combobox.setEnabled(True)
            self.new_gender_combobox.setEnabled(True)
            self.new_program_code_combobox.setEnabled(True)

        else:
            self.edit_student_button.setEnabled(False)
            self.new_id_number_lineedit.setEnabled(False)
            self.new_first_name_lineedit.setEnabled(False)
            self.new_last_name_lineedit.setEnabled(False)
            self.new_year_level_combobox.setEnabled(False)
            self.new_gender_combobox.setEnabled(False)
            self.new_program_code_combobox.setEnabled(False)

    def set_old_data_as_placeholders(self):
        for student in self.students_table_model.data_from_csv:
            if student[0] == self.student_to_edit_combobox.currentText():
                self.new_id_number_lineedit.setPlaceholderText(student[0])
                self.new_first_name_lineedit.setPlaceholderText(student[1])
                self.new_last_name_lineedit.setPlaceholderText(student[2])
                self.new_year_level_combobox.setCurrentText(student[3])
                self.new_gender_combobox.setCurrentText(student[4])
                self.new_program_code_combobox.setCurrentText(student[5])

    def row_to_edit(self):
        for student in self.students_table_model.data_from_csv:
            if student[0] == self.student_to_edit_combobox.currentText():
                return self.students_table_model.data_from_csv.index(student)

