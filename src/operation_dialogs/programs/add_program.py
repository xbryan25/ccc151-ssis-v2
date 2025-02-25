from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import Qt

from operation_dialogs.programs.add_program_design import Ui_Dialog as AddProgramUI

from helper_dialogs.add_item_state.fail_add_item import FailAddItemDialog
from helper_dialogs.add_item_state.success_add_item import SuccessAddItemDialog

from utils.is_valid_verifiers import IsValidVerifiers
from utils.get_information_codes import GetInformationCodes
from utils.get_existing_information import GetExistingInformation


class AddProgramDialog(QDialog, AddProgramUI):
    def __init__(self, programs_table_view, programs_table_model, colleges_table_model, reset_item_delegates_func):
        super().__init__()

        self.setupUi(self)

        self.set_external_stylesheet()

        self.reset_item_delegates_func = reset_item_delegates_func

        self.colleges_table_model = colleges_table_model

        self.programs_table_view = programs_table_view
        self.programs_table_model = programs_table_model

        # Load utils
        self.is_valid = IsValidVerifiers()
        self.get_information_codes = GetInformationCodes()
        self.get_existing_information = GetExistingInformation()

        self.add_college_codes_to_combobox()

        self.add_signals()

        self.set_college_code_combobox_scrollbar()

    def add_program_confirmation(self):
        issues = self.find_issues()

        if issues:
            self.fail_add_item_dialog = FailAddItemDialog(issues, "program")
            self.fail_add_item_dialog.exec()
        else:
            # Convert program code to all caps
            # Convert all commas in program name to underscores because it messes up the csv
            program_to_add = [self.program_code_lineedit.text().upper(),
                              self.program_name_lineedit.text().replace(",", "_"),
                              self.college_code_combobox.currentText()]

            self.add_program_to_model(program_to_add)

            self.programs_table_model.set_has_changes(True)

            self.reset_item_delegates_func("add_program")

            self.success_add_item_dialog = SuccessAddItemDialog("program", self)
            self.success_add_item_dialog.exec()

    def add_program_to_model(self, program_to_add):
        self.programs_table_model.layoutAboutToBeChanged.emit()

        if self.programs_table_model.get_data()[0][0] == "":
            self.programs_table_model.get_data().pop()

        self.programs_table_model.get_data().append(program_to_add)
        self.programs_table_model.layoutChanged.emit()

    def add_college_codes_to_combobox(self):
        for college_code in self.get_college_codes():
            self.college_code_combobox.addItem(college_code)

    def set_college_code_combobox_scrollbar(self):
        self.college_code_combobox.view().setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    def enable_add_button(self):
        if ((self.college_code_combobox.currentText() != "--Select a college--") and
                (self.college_code_combobox.currentText() in self.get_college_codes())):

            self.add_program_button.setEnabled(True)
        else:
            self.add_program_button.setEnabled(False)

    def find_issues(self):
        programs_information = self.get_existing_programs()
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

        return issues

    def add_signals(self):
        self.add_program_button.clicked.connect(self.add_program_confirmation)

        self.college_code_combobox.currentTextChanged.connect(self.enable_add_button)

    def get_existing_programs(self):
        return self.get_existing_information.from_programs(self.programs_table_model.get_data())

    def get_program_codes(self):
        return self.get_information_codes.for_programs(self.programs_table_model.get_data())

    def get_college_codes(self):
        return self.get_information_codes.for_colleges(self.colleges_table_model.get_data())

    def set_external_stylesheet(self):
        with open("../assets/qss_files/dialog_style.qss", "r") as file:
            self.setStyleSheet(file.read())