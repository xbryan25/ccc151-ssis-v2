from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QFontDatabase

from operation_dialogs.edit_entity.edit_college_design import Ui_Dialog as EditCollegeUI

from helper_dialogs.edit_item_state.fail_to_edit_item import FailToEditItemDialog
from helper_dialogs.edit_item_state.success_edit_item import SuccessEditItemDialog
from helper_dialogs.edit_item_state.confirm_edit import ConfirmEditDialog

from utils.is_valid_verifiers import IsValidVerifiers
from utils.specific_buttons_enabler import SpecificButtonsEnabler


class EditCollegeDialog(QDialog, EditCollegeUI):
    def __init__(self, colleges_table_view, college_table_model, save_changes_button, undo_all_changes_button,
                 reset_item_delegates_func, college_codes_to_edit, selected_rows):

        super().__init__()

        self.setupUi(self)

        self.set_external_stylesheet()
        self.load_fonts()

        self.colleges_table_view = colleges_table_view
        self.colleges_table_model = college_table_model

        self.save_changes_button = save_changes_button
        self.undo_all_changes_button = undo_all_changes_button

        self.reset_item_delegates_func = reset_item_delegates_func

        self.college_codes_to_edit = college_codes_to_edit
        self.selected_rows = selected_rows

        self.set_old_data_as_placeholders()

        self.is_valid = IsValidVerifiers()
        self.existing_colleges_information = self.colleges_table_model.db_handler.get_all_existing_colleges()

        self.add_signals()

    def edit_single_college_information(self):
        issues = self.has_issues()

        if issues:
            self.fail_to_edit_item_dialog = FailToEditItemDialog(issues, "college")
            self.fail_to_edit_item_dialog.exec()
        else:
            # If either the college code or college name is blank, their
            #   respective placeholder texts will be used

            college_to_edit = [self.new_college_code_lineedit.text().upper()
                               if self.new_college_code_lineedit.text().strip()
                               else self.new_college_code_lineedit.placeholderText(),

                               self.new_college_name_lineedit.text().strip()
                               if self.new_college_name_lineedit.text().strip()
                               else self.new_college_name_lineedit.placeholderText()]

            actual_row_to_edit = ((self.colleges_table_model.max_row_per_page *
                                   (self.colleges_table_model.current_page_number - 1))
                                  + self.selected_rows[0])

            # Check if there are any changes made from the old data of the college
            if self.colleges_table_model.get_data()[actual_row_to_edit] != college_to_edit:
                len_of_programs_under_college_code = self.len_of_programs_under_college_code(self.college_codes_to_edit[0])

                # If college code is not changed, a different confirm edit dialog will show
                if self.college_codes_to_edit[0] == college_to_edit[0]:
                    self.confirm_to_edit_dialog = ConfirmEditDialog("college",
                                                                    self.college_codes_to_edit[0])
                else:

                    self.confirm_to_edit_dialog = ConfirmEditDialog("college",
                                                                    self.college_codes_to_edit[0],
                                                                    num_of_affected=len_of_programs_under_college_code,
                                                                    entity_code_affected=True)

                # Halts the program where as this starts another loop
                self.confirm_to_edit_dialog.exec()

                confirm_edit_decision = self.confirm_to_edit_dialog.get_confirm_edit_decision()

                if confirm_edit_decision:

                    self.colleges_table_model.update_entity(college_to_edit,
                                                            'college',
                                                            actual_row_to_edit=actual_row_to_edit)

                    self.colleges_table_model.set_has_changes(True)

                    SpecificButtonsEnabler.enable_save_and_undo_buttons(self.save_changes_button,
                                                                        self.undo_all_changes_button,
                                                                        colleges_table_model=self.colleges_table_model)

                    self.reset_item_delegates_func("edit_college")

                    self.success_edit_item_dialog = SuccessEditItemDialog("college", self.college_codes_to_edit, self)
                    self.success_edit_item_dialog.exec()

            else:
                self.fail_to_edit_item_dialog = FailToEditItemDialog(["No changes made to the college"], "college")
                self.fail_to_edit_item_dialog.exec()

    def enable_edit_button(self):

        if self.new_college_code_lineedit.text().strip() != "" or self.new_college_name_lineedit.text().strip() != "":
            self.edit_college_button.setEnabled(True)
        else:
            self.edit_college_button.setEnabled(False)

    def set_old_data_as_placeholders(self):
        for college in self.colleges_table_model.get_data():
            if college[0] == self.college_codes_to_edit[0]:
                self.college_to_edit_list.setText(self.college_codes_to_edit[0])

                self.new_college_code_lineedit.setPlaceholderText(college[0])
                self.new_college_name_lineedit.setPlaceholderText(college[1])

    def len_of_programs_under_college_code(self, old_college_code):
        length = 0

        for program in self.colleges_table_model.db_handler.get_all_entities('program'):
            if program[2] == old_college_code:
                length += 1

        return length

    def has_issues(self):
        issues = []

        if not self.is_valid.college_code(self.new_college_code_lineedit.text().strip(), edit_state=True):
            issues.append("College code is not in the correct format")

        # Checks if the college code already exists and if it is not the same as the placeholder text
        elif (self.new_college_code_lineedit.text().strip() in self.get_existing_colleges()["College Code"] and
              self.new_college_code_lineedit.text().strip() != self.new_college_code_lineedit.placeholderText()):
            issues.append("College code already exists")

        if not self.is_valid.college_name(self.new_college_name_lineedit.text().strip(), edit_state=True):
            issues.append("College name is not in the correct format")

        # Checks if the college name already exists and if it is not the same as the placeholder text
        elif (self.new_college_name_lineedit.text().strip() in self.get_existing_colleges()["College Name"] and
              self.new_college_name_lineedit.text().strip() != self.new_college_name_lineedit.placeholderText()):
            issues.append("College name already exists")

        return issues

    def add_signals(self):
        self.edit_college_button.clicked.connect(self.edit_single_college_information)

        self.new_college_code_lineedit.textChanged.connect(self.enable_edit_button)
        self.new_college_name_lineedit.textChanged.connect(self.enable_edit_button)

    def get_existing_colleges(self):
        return self.colleges_table_model.db_handler.get_all_existing_colleges()

    def get_college_codes(self):
        return self.colleges_table_model.db_handler.get_all_entity_information_codes('college')

    def set_external_stylesheet(self):
        with open("../assets/qss_files/dialog_style.qss", "r") as file:
            self.setStyleSheet(file.read())

    def load_fonts(self):
        self.cg_font_family = QFontDatabase.applicationFontFamilies(0)[0]

        self.header_label.setFont(QFont(self.cg_font_family, 16, QFont.Weight.DemiBold))

        self.college_to_edit_label.setFont(QFont(self.cg_font_family, 12, QFont.Weight.Medium))
        self.college_to_edit_list.setFont(QFont(self.cg_font_family, 10, QFont.Weight.Medium))
        self.new_college_code_label.setFont(QFont(self.cg_font_family, 12, QFont.Weight.Medium))
        self.new_college_name_label.setFont(QFont(self.cg_font_family, 12, QFont.Weight.Medium))

        self.new_college_code_lineedit.setFont(QFont(self.cg_font_family, 12, QFont.Weight.Normal))
        self.new_college_name_lineedit.setFont(QFont(self.cg_font_family, 12, QFont.Weight.Normal))

        self.edit_college_button.setFont(QFont(self.cg_font_family, 20, QFont.Weight.DemiBold))