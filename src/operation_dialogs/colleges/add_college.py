from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QFont, QFontDatabase

from operation_dialogs.colleges.add_college_design import Ui_Dialog as AddCollegeUI

from helper_dialogs.add_item_state.fail_add_item import FailAddItemDialog
from helper_dialogs.add_item_state.success_add_item import SuccessAddItemDialog

from utils.is_valid_verifiers import IsValidVerifiers
from utils.get_existing_information import GetExistingInformation

import re
import csv


class AddCollegeDialog(QDialog, AddCollegeUI):
    def __init__(self, colleges_table_view, colleges_table_model, reset_items_delegates_func):
        super().__init__()

        self.setupUi(self)

        self.set_external_stylesheet()
        self.load_fonts()

        self.reset_item_delegates_func = reset_items_delegates_func

        self.colleges_table_view = colleges_table_view
        self.colleges_table_model = colleges_table_model

        # Load utils
        self.is_valid = IsValidVerifiers()
        self.get_existing_information = GetExistingInformation()

        self.add_signals()

    def add_college_confirmation(self):
        issues = self.find_issues()

        if issues:
            self.fail_add_item_dialog = FailAddItemDialog(issues, "college")
            self.fail_add_item_dialog.exec()
        else:
            # Convert college code to all caps
            # Convert all commas in college name to underscores because it messes up the csv
            college_to_add = [self.college_code_lineedit.text().upper(),
                              self.college_name_lineedit.text().replace(",", "_")]

            self.add_college_to_model(college_to_add)

            self.reset_item_delegates_func("add_college")

            # Notifies the CustomTableModel instance that something had changed
            self.colleges_table_model.set_has_changes(True)

            self.success_add_item_dialog = SuccessAddItemDialog("college", self)
            self.success_add_item_dialog.exec()

    def add_college_to_model(self, college_to_add):
        self.colleges_table_model.layoutAboutToBeChanged.emit()

        if self.colleges_table_model.get_data()[0][0] == "":
            self.colleges_table_model.get_data().pop()

        self.colleges_table_model.add_entity(college_to_add, "college")
        self.colleges_table_model.layoutChanged.emit()

    def find_issues(self):
        colleges_information = self.colleges_table_model.db_handler.get_all_existing_colleges()

        issues = []

        if (self.college_code_lineedit.text()).strip() == "":
            issues.append("College code is blank")
        elif not self.is_valid.college_code(self.college_code_lineedit.text()):
            issues.append("College code is not in the correct format")
        elif (self.college_code_lineedit.text().upper()).strip() in colleges_information["College Code"]:
            issues.append("College code already exists")

        if (self.college_name_lineedit.text()).strip() == "":
            issues.append("College name is blank")
        elif not self.is_valid.college_name(self.college_name_lineedit.text()):
            issues.append("College name is not in the correct format")
        elif (self.college_name_lineedit.text()).strip() in colleges_information["College Name"]:
            issues.append("College name already exists")

        return issues

    def add_signals(self):
        self.add_college_button.clicked.connect(self.add_college_confirmation)

    def set_external_stylesheet(self):
        with open("../assets/qss_files/dialog_style.qss", "r") as file:
            self.setStyleSheet(file.read())

    def load_fonts(self):
        self.cg_font_family = QFontDatabase.applicationFontFamilies(0)[0]

        self.header_label.setFont(QFont(self.cg_font_family, 16, QFont.Weight.DemiBold))

        self.college_code_label.setFont(QFont(self.cg_font_family, 12, QFont.Weight.Medium))
        self.college_name_label.setFont(QFont(self.cg_font_family, 12, QFont.Weight.Medium))

        self.college_code_lineedit.setFont(QFont(self.cg_font_family, 12, QFont.Weight.Normal))
        self.college_name_lineedit.setFont(QFont(self.cg_font_family, 12, QFont.Weight.Normal))

        self.add_college_button.setFont(QFont(self.cg_font_family, 20, QFont.Weight.DemiBold))
