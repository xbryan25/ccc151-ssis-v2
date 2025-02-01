from PyQt6.QtWidgets import QDialog, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt

from programs.add_program_design import Ui_Dialog as AddProgramUI

from helper_dialogs.add_item_state.fail_add_item import FailAddItemDialog
from helper_dialogs.add_item_state.success_add_item import SuccessAddItemDialog

from utils.is_valid_verifiers import IsValidVerifiers
from utils.get_information_codes import GetInformationCodes
from utils.get_existing_information import GetExistingInformation

import re
import csv


class AddProgramDialog(QDialog, AddProgramUI):
    def __init__(self, programs_table):
        super().__init__()

        self.setupUi(self)

        self.programs_table = programs_table

        self.is_valid = IsValidVerifiers()
        self.get_information_codes = GetInformationCodes()
        self.get_existing_information = GetExistingInformation()

        self.add_college_codes_to_combobox()

        self.add_program_button.clicked.connect(self.add_program_to_csv)

    def add_program_to_csv(self):
        programs_information = self.get_existing_information.from_programs()
        issues = []

        if (self.program_code_lineedit.text()).strip() == "":
            issues.append("Program code is blank")
        elif not self.is_valid.program_code(self.program_code_lineedit.text()):
            issues.append("Program code is not in the correct format")
        elif (self.program_code_lineedit.text().upper()).strip() in programs_information["Program Code"]:
            issues.append("Program code already exists")

        if (self.program_name_lineedit.text()).strip() == "":
            issues.append("Program name is blank")
        elif not self.is_valid.program_name(self.program_name_lineedit.text()):
            issues.append("Program name is not in the correct format")
        elif (self.program_name_lineedit.text()).strip() in programs_information["Program Name"]:
            issues.append("Program name already exists")

        if issues:
            self.fail_add_item_dialog = FailAddItemDialog(issues, "program")
            self.fail_add_item_dialog.exec()
        else:
            # Convert program code to all caps
            # Convert all commas in program name to underscores because it messes up the csv
            program_to_add = [self.program_code_lineedit.text().upper(),
                              self.program_name_lineedit.text().replace(",", "_"),
                              self.college_code_combobox.currentText()]

            with open("databases/programs.csv", 'a', newline='') as from_programs_csv:
                writer = csv.writer(from_programs_csv)

                writer.writerow(program_to_add)

            self.add_program_to_table(program_to_add)

            self.success_add_item_dialog = SuccessAddItemDialog("programs", self)

            self.success_add_item_dialog.exec()

    def add_program_to_table(self, program_to_add):
        row_position = self.programs_table.rowCount()
        self.programs_table.insertRow(row_position)

        order_id = QTableWidgetItem()
        order_id.setData(Qt.ItemDataRole.DisplayRole, row_position)
        order_id.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        program_code = QTableWidgetItem(program_to_add[0])
        program_code.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        program_name = QTableWidgetItem(program_to_add[1].replace("_", ","))
        program_name.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        college_code = QTableWidgetItem(program_to_add[2])
        college_code.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        self.programs_table.setItem(row_position, 0, order_id)
        self.programs_table.setItem(row_position, 1, program_code)
        self.programs_table.setItem(row_position, 2, program_name)
        self.programs_table.setItem(row_position, 3, college_code)

    def add_college_codes_to_combobox(self):
        for college_code in self.get_information_codes.for_colleges():
            self.college_code_combobox.addItem(college_code)
