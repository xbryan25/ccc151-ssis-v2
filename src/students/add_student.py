from PyQt6.QtWidgets import QDialog, QTableWidget, QTableWidgetItem

from students.add_student_design import Ui_Dialog as AddStudentUI
from add_item_state.fail_add_item import FailAddItemDialog
from add_item_state.success_add_item import SuccessAddItemDialog

import re
import csv


class AddStudentDialog(QDialog, AddStudentUI):
    def __init__(self, students_table):
        super().__init__()

        self.setupUi(self)

        self.students_table = students_table

        self.add_student_button.clicked.connect(self.add_student_to_csv)

    def add_student_to_csv(self):

        students_information = self.get_existing_students_information()
        issues = []

        if (self.id_number_lineedit.text()).strip() == "":
            issues.append("ID Number is blank")
        elif not self.is_valid_id_number():
            issues.append("ID Number is not in the correct format")
        elif (self.id_number_lineedit.text()).strip() in students_information["ID Number"]:
            issues.append("ID Number has already been taken")

        if (self.first_name_lineedit.text()).strip() == "":
            issues.append("First name is blank")
        elif not self.is_valid_first_name():
            issues.append("First name is not in the correct format")

        if (self.last_name_lineedit.text()).strip() == "":
            issues.append("Last name is blank")
        elif not self.is_valid_last_name():
            issues.append("Last name is not in the correct format")

        full_name = f"{(self.first_name_lineedit.text()).strip()} {(self.last_name_lineedit.text()).strip()}"
        if full_name in students_information["Full Name"]:
            issues.append("Name combination already exists")

        if (self.program_code_lineedit.text()).strip() == "":
            issues.append("Program code is blank")
        elif not self.is_valid_program_code():
            issues.append("Program code is not in the correct format")

        if issues:
            self.fail_add_item_dialog = FailAddItemDialog(issues)
            self.fail_add_item_dialog.show()
        else:
            student_to_add = [self.id_number_lineedit.text(),
                              self.first_name_lineedit.text(),
                              self.last_name_lineedit.text(),
                              self.year_level_combobox.currentText(),
                              self.gender_combobox.currentText(),
                              self.program_code_lineedit.text()]

            with open("databases/students.csv", 'a', newline='') as from_students_csv:
                writer = csv.writer(from_students_csv)

                writer.writerow(student_to_add)

            self.add_student_to_table(student_to_add)

            self.success_add_item_dialog = SuccessAddItemDialog(self)

            self.success_add_item_dialog.show()


    def get_existing_students_information(self):
        students_information = {"ID Number": [], "Full Name": []}

        with open("databases/students.csv", 'r') as from_students_csv:
            reader = csv.reader(from_students_csv)

            for row in reader:
                students_information["ID Number"].append(row[0])
                students_information["Full Name"].append(f"{row[1].strip()} {row[2].strip()}")

        return students_information

    def add_student_to_table(self, student_to_add):
        rowPosition = self.students_table.rowCount()
        self.students_table.insertRow(rowPosition)

        self.students_table.setItem(rowPosition, 0, QTableWidgetItem(student_to_add[0]))
        self.students_table.setItem(rowPosition, 1, QTableWidgetItem(student_to_add[1]))
        self.students_table.setItem(rowPosition, 2, QTableWidgetItem(student_to_add[2]))
        self.students_table.setItem(rowPosition, 3, QTableWidgetItem(student_to_add[3]))
        self.students_table.setItem(rowPosition, 4, QTableWidgetItem(student_to_add[4]))
        self.students_table.setItem(rowPosition, 5, QTableWidgetItem(student_to_add[5]))


    def is_valid_id_number(self):
        valid_id_number = re.match(r'^[0-9]{4}-[0-9]{4}$', self.id_number_lineedit.text())

        return True if valid_id_number else False

    def is_valid_first_name(self):
        valid_first_name = re.match(r'^[a-zA-Z ]+$', self.first_name_lineedit.text())

        return True if valid_first_name else False

    def is_valid_last_name(self):
        valid_last_name = re.match(r'^[a-zA-Z ]+$', self.last_name_lineedit.text())

        return True if valid_last_name else False

    def is_valid_program_code(self):
        valid_program_code = re.match(r'^[A-Z]{3,}$', self.program_code_lineedit.text())

        return True if valid_program_code else False
