from PyQt6.QtWidgets import QDialog, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt

from students.add_student_design import Ui_Dialog as AddStudentUI

from helper_dialogs.add_item_state.fail_add_item import FailAddItemDialog
from helper_dialogs.add_item_state.success_add_item import SuccessAddItemDialog

from utils.is_valid_verifiers import IsValidVerifiers
from utils.get_information_codes import GetInformationCodes
from utils.get_existing_information import GetExistingInformation

import re
import csv


class AddStudentDialog(QDialog, AddStudentUI):
    def __init__(self, students_table_view, students_table_model):
        super().__init__()

        self.setupUi(self)

        self.students_table_view = students_table_view
        self.students_table_model = students_table_model

        self.is_valid = IsValidVerifiers()
        self.get_information_codes = GetInformationCodes()
        self.get_existing_information = GetExistingInformation()

        self.add_program_codes_to_combobox()

        self.add_student_button.clicked.connect(self.add_student_to_csv)
        self.set_program_code_combobox_scrollbar()

    def add_student_to_csv(self):
        students_information = self.get_existing_information.from_students()
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

            with open("databases/students.csv", 'a', newline='') as from_students_csv:
                writer = csv.writer(from_students_csv)

                writer.writerow(student_to_add)

            self.add_student_to_table(student_to_add)

            self.success_add_item_dialog = SuccessAddItemDialog("student", self)

            self.success_add_item_dialog.exec()

    def add_student_to_table(self, student_to_add):
        self.students_table_model.layoutAboutToBeChanged.emit()
        self.students_table_model.data_from_csv.append(student_to_add)
        self.students_table_model.layoutChanged.emit()

    def add_program_codes_to_combobox(self):
        for program_code in self.get_information_codes.for_programs():
            self.program_code_combobox.addItem(program_code)

    def set_program_code_combobox_scrollbar(self):
        self.program_code_combobox.view().setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)


