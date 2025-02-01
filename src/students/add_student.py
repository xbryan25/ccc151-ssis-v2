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
    def __init__(self, students_table):
        super().__init__()

        self.setupUi(self)

        self.students_table = students_table

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
            self.fail_add_item_dialog = FailAddItemDialog(issues)
            self.fail_add_item_dialog.show()
        else:
            student_to_add = [self.id_number_lineedit.text(),
                              self.first_name_lineedit.text().strip(),
                              self.last_name_lineedit.text().strip(),
                              self.year_level_combobox.currentText(),
                              self.gender_combobox.currentText(),
                              self.program_code_lineedit.text().upper()]

            with open("databases/students.csv", 'a', newline='') as from_students_csv:
                writer = csv.writer(from_students_csv)

                writer.writerow(student_to_add)

            self.add_student_to_table(student_to_add)

            self.success_add_item_dialog = SuccessAddItemDialog("student", self)

            self.success_add_item_dialog.show()

    def add_student_to_table(self, student_to_add):
        row_position = self.students_table.rowCount()
        self.students_table.insertRow(row_position)

        order_id = QTableWidgetItem()
        order_id.setData(Qt.ItemDataRole.DisplayRole, row_position)
        order_id.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        id_number = QTableWidgetItem(student_to_add[0])
        id_number.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        first_name = QTableWidgetItem(student_to_add[1])
        first_name.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        last_name = QTableWidgetItem(student_to_add[2])
        last_name.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        year_level = QTableWidgetItem(student_to_add[3])
        year_level.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        gender = QTableWidgetItem(student_to_add[4])
        gender.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        program_code = QTableWidgetItem(student_to_add[5])
        program_code.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        self.students_table.setItem(row_position, 0, order_id)
        self.students_table.setItem(row_position, 1, id_number)
        self.students_table.setItem(row_position, 2, first_name)
        self.students_table.setItem(row_position, 3, last_name)
        self.students_table.setItem(row_position, 4, year_level)
        self.students_table.setItem(row_position, 5, gender)
        self.students_table.setItem(row_position, 6, program_code)

    def add_program_codes_to_combobox(self):
        for program_code in self.get_information_codes.for_programs():
            self.program_code_combobox.addItem(program_code)

    # Put all is_valid functions in a util file

    # def is_valid_id_number(self):
    #     valid_id_number = re.match(r'^[0-9]{4}-[0-9]{4}$', self.id_number_lineedit.text())
    #
    #     return True if valid_id_number else False
    #
    # def is_valid_first_name(self):
    #     valid_first_name = re.match(r'^[a-zA-Z ]+$', self.first_name_lineedit.text())
    #
    #     return True if valid_first_name else False
    #
    # def is_valid_last_name(self):
    #     valid_last_name = re.match(r'^[a-zA-Z ]+$', self.last_name_lineedit.text())
    #
    #     return True if valid_last_name else False

    def set_program_code_combobox_scrollbar(self):
        self.program_code_combobox.view().setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    # def is_valid_program_code(self):
    #     valid_program_code = re.match(r'^[a-zA-Z]{3,}$', self.program_code_lineedit.text())
    #
    #     return True if valid_program_code else False
