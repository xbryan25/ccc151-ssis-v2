from PyQt6.QtWidgets import QDialog, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt

from colleges.add_college_design import Ui_Dialog as AddCollegeUI

from helper_dialogs.add_item_state.fail_add_item import FailAddItemDialog
from helper_dialogs.add_item_state.success_add_item import SuccessAddItemDialog

import re
import csv


class AddCollegeDialog(QDialog, AddCollegeUI):
    def __init__(self, colleges_table):
        super().__init__()

        self.setupUi(self)

        self.colleges_table = colleges_table

        self.add_college_button.clicked.connect(self.add_college_to_csv)

    def add_college_to_csv(self):
        colleges_information = self.get_existing_colleges_information()
        issues = []

        if (self.college_code_lineedit.text()).strip() == "":
            issues.append("College code is blank")
        elif not self.is_valid_college_code():
            issues.append("College code is not in the correct format")
        elif (self.college_code_lineedit.text().upper()).strip() in colleges_information["College Code"]:
            issues.append("College code already exists")

        if (self.college_name_lineedit.text()).strip() == "":
            issues.append("College name is blank")
        elif not self.is_valid_college_name():
            issues.append("College name is not in the correct format")
        elif (self.college_name_lineedit.text()).strip() in colleges_information["College Name"]:
            issues.append("College name already exists")

        if issues:
            self.fail_add_item_dialog = FailAddItemDialog(issues, "college")
            self.fail_add_item_dialog.exec()
        else:
            # Convert college code to all caps
            # Convert all commas in college name to underscores because it messes up the csv

            college_to_add = [self.college_code_lineedit.text().upper(),
                              self.college_name_lineedit.text().replace(",", "_")]

            with open("databases/colleges.csv", 'a', newline='') as from_colleges_csv:
                writer = csv.writer(from_colleges_csv)

                writer.writerow(college_to_add)

            self.add_college_to_table(college_to_add)

            self.success_add_item_dialog = SuccessAddItemDialog("college", self)

            self.success_add_item_dialog.exec()

    @staticmethod
    def get_existing_colleges_information():
        colleges_information = {"College Code": [], "College Name": []}

        with open("databases/colleges.csv", 'r') as from_colleges_csv:
            reader = csv.reader(from_colleges_csv)

            for row in reader:
                colleges_information["College Code"].append(row[0])
                colleges_information["College Name"].append(row[1].replace("_", ","))

        return colleges_information

    def add_college_to_table(self, college_to_add):
        row_position = self.colleges_table.rowCount()
        self.colleges_table.insertRow(row_position)

        order_id = QTableWidgetItem()
        order_id.setData(Qt.ItemDataRole.DisplayRole, row_position)
        order_id.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        college_code = QTableWidgetItem(college_to_add[0])
        college_code.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        college_name = QTableWidgetItem(college_to_add[1].replace("_", ","))
        college_name.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        self.colleges_table.setItem(row_position, 0, order_id)
        self.colleges_table.setItem(row_position, 1, college_code)
        self.colleges_table.setItem(row_position, 2, college_name)

    def is_valid_college_code(self):
        valid_college_code = re.match(r'^[a-zA-Z]{3,}$', self.college_code_lineedit.text())

        return True if valid_college_code else False

    def is_valid_college_name(self):
        valid_college_name = re.match(r'^[a-zA-Z, ]+$', self.college_name_lineedit.text())

        return True if valid_college_name else False
