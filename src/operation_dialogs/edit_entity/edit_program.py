from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QFontDatabase

from operation_dialogs.edit_entity.edit_program_design import Ui_Dialog as EditProgramUI

from helper_dialogs.edit_item_state.fail_to_edit_item import FailToEditItemDialog
from helper_dialogs.edit_item_state.success_edit_item import SuccessEditItemDialog
from helper_dialogs.edit_item_state.confirm_edit import ConfirmEditDialog

from utils.is_valid_verifiers import IsValidVerifiers
from utils.specific_buttons_enabler import SpecificButtonsEnabler


class EditProgramDialog(QDialog, EditProgramUI):
    def __init__(self, programs_table_view, programs_table_model, save_changes_button, undo_all_changes_button,
                 reset_item_delegates_func, program_codes_to_edit, selected_rows):

        super().__init__()

        self.setupUi(self)

        self.set_external_stylesheet()
        self.load_fonts()

        self.programs_table_view = programs_table_view
        self.programs_table_model = programs_table_model

        self.save_changes_button = save_changes_button
        self.undo_all_changes_button = undo_all_changes_button

        self.reset_item_delegates_func = reset_item_delegates_func

        self.program_codes_to_edit = program_codes_to_edit
        self.selected_rows = selected_rows

        if len(self.program_codes_to_edit) == 1:
            self.current_program_data = None

            self.set_old_data_as_placeholders()

            self.edit_mode = "single"
        else:
            self.populate_program_to_edit_list()
            self.disable_fields()

            self.edit_mode = "multiple"

        self.is_valid = IsValidVerifiers()

        # self.add_program_codes_to_combobox()
        self.add_college_codes_to_combobox()

        self.add_signals()

        # self.set_program_code_combobox_scrollbar()
        self.set_college_code_combobox_scrollbar()

    def populate_program_to_edit_list(self):

        formatted_string = ""

        for index, program_code in enumerate(self.program_codes_to_edit):

            # Show 10 program codes at maximum
            if index == 9:
                formatted_string += f"{str(program_code)}..."
                break
            if index + 1 == len(self.program_codes_to_edit):
                formatted_string += f"{str(program_code)}"
            else:
                formatted_string += f"{str(program_code)}, "

            # if index + 1 % 3 == 0:
            #     formatted_string += "\n"

        self.setWindowTitle("Edit programs")
        self.program_to_edit_label.setText("Programs To Be Edited")
        self.program_to_edit_list.setText(formatted_string)

    def disable_fields(self):
        self.new_program_code_label.close()
        self.new_program_code_lineedit.close()

        self.new_program_name_label.close()
        self.new_program_name_lineedit.close()

        self.setMinimumSize(QSize(465, 320))
        self.setMaximumSize(QSize(465, 320))

        self.resize(465, 320)

    def edit_single_program_information(self):
        issues = self.has_issues()

        if issues:
            self.fail_to_edit_item_dialog = FailToEditItemDialog(issues, "program")
            self.fail_to_edit_item_dialog.exec()
        else:
            # If either the program code or program name is blank, their
            #   respective placeholder texts will be used

            program_to_edit = [self.new_program_code_lineedit.text()
                               if self.new_program_code_lineedit.text().strip()
                               else self.new_program_code_lineedit.placeholderText(),

                               self.new_program_name_lineedit.text().strip()
                               if self.new_program_name_lineedit.text().strip()
                               else self.new_program_name_lineedit.placeholderText(),

                               self.new_college_code_combobox.currentText()]

            row_to_edit = self.selected_rows[0]

            # Check if there are any changes made from the old data of the program
            if self.programs_table_model.get_data()[row_to_edit] != program_to_edit:
                len_of_students_under_program_code = self.len_of_students_under_program_code(self.program_codes_to_edit[0])

                # If program code is not changed, a different confirm edit dialog will show
                if self.program_codes_to_edit[0] == program_to_edit[0]:
                    self.confirm_to_edit_dialog = ConfirmEditDialog("program",
                                                                    self.program_codes_to_edit)
                else:
                    self.confirm_to_edit_dialog = ConfirmEditDialog("program",
                                                                    self.program_codes_to_edit,
                                                                    num_of_affected=len_of_students_under_program_code,
                                                                    entity_code_affected=True)

                # Halts the program as this starts another loop
                self.confirm_to_edit_dialog.exec()

                confirm_edit_decision = self.confirm_to_edit_dialog.get_confirm_edit_decision()

                if confirm_edit_decision:

                    self.programs_table_model.update_entity(program_to_edit,
                                                            'program',
                                                            row_to_edit=row_to_edit)

                    self.programs_table_model.set_has_changes(True)

                    SpecificButtonsEnabler.enable_save_and_undo_buttons(self.save_changes_button,
                                                                        self.undo_all_changes_button,
                                                                        programs_table_model=self.programs_table_model)

                    self.reset_item_delegates_func("edit_program")

                    self.success_edit_item_dialog = SuccessEditItemDialog("program", self.program_codes_to_edit, self)
                    self.success_edit_item_dialog.exec()

            else:
                self.fail_to_edit_item_dialog = FailToEditItemDialog(["No changes made to the program"], "program")
                self.fail_to_edit_item_dialog.exec()

    def edit_multiple_program_information(self):

        programs_to_edit = ["",
                            "",
                            self.new_college_code_combobox.currentText()]

        self.confirm_to_edit_dialog = ConfirmEditDialog("program",
                                                        self.program_codes_to_edit)

        # Halts the program whereas this starts another loop
        self.confirm_to_edit_dialog.exec()

        confirm_edit_decision = self.confirm_to_edit_dialog.get_confirm_edit_decision()

        if confirm_edit_decision:

            for selected_row in self.selected_rows:

                # By doing this, the data in the model also gets updated, same reference
                # self.students_table_model.get_data()[row_to_edit] = student_to_edit

                # list(programs_to_edit) creates another copy that doesn't manipulate programs_to_edit
                self.programs_table_model.update_entity(list(programs_to_edit),
                                                        'program',
                                                        row_to_edit=selected_row,
                                                        edit_mode=self.edit_mode)

            self.programs_table_model.set_has_changes(True)

            SpecificButtonsEnabler.enable_save_and_undo_buttons(self.save_changes_button,
                                                                self.undo_all_changes_button,
                                                                programs_table_model=self.programs_table_model)

            self.reset_item_delegates_func("edit_program")

            self.success_edit_item_dialog = SuccessEditItemDialog("program", self.program_codes_to_edit, self)
            self.success_edit_item_dialog.exec()

    def add_program_codes_to_combobox(self):
        for program_code in self.get_program_codes():
            self.program_to_edit_combobox.addItem(program_code)

    def add_college_codes_to_combobox(self):
        for college_code in self.get_college_codes():
            self.new_college_code_combobox.addItem(college_code)

    def set_program_code_combobox_scrollbar(self):
        self.program_to_edit_combobox.view().setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    def set_college_code_combobox_scrollbar(self):
        self.new_college_code_combobox.view().setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    def enable_edit_button(self):

        if self.edit_mode == "single":
            current_program_code = self.current_program_data[0]
            current_program_name = self.current_program_data[1]
            current_college_code = self.current_program_data[2]

            new_program_code = self.new_program_code_lineedit.text().strip()
            new_program_name = self.new_program_name_lineedit.text().strip()
            new_college_code = self.new_college_code_combobox.currentText()

            if ((new_program_code != "" and new_program_code != current_program_code) or
                    (new_program_name != "" and new_program_name != current_program_name) or
                    (new_college_code != "--Select a college--" and new_college_code != "" and
                     new_college_code in self.get_college_codes() and new_college_code != current_college_code)):

                self.edit_program_button.setEnabled(True)
                return

        elif self.edit_mode == "multiple":

            new_college_code = self.new_college_code_combobox.currentText()

            if (new_college_code != "--Select a college--" and new_college_code != "" and
                    new_college_code in self.get_college_codes()):

                self.edit_program_button.setEnabled(True)
                return

        self.edit_program_button.setEnabled(False)

    def set_old_data_as_placeholders(self):
        for program in self.programs_table_model.get_data():
            if program[0] == self.program_codes_to_edit[0]:

                self.current_program_data = program

                self.program_to_edit_list.setText(self.program_codes_to_edit[0])

                self.new_program_code_lineedit.setPlaceholderText(program[0])
                self.new_program_name_lineedit.setPlaceholderText(program[1])
                self.new_college_code_combobox.setCurrentText(program[2])

                break

    def len_of_students_under_program_code(self, old_program_code):
        length = 0

        for student in self.programs_table_model.db_handler.get_all_entities('student'):
            if student[5] == old_program_code:
                length += 1

        return length

    def has_issues(self):
        issues = []

        if not self.is_valid.program_code(self.new_program_code_lineedit.text().strip(), edit_state=True):
            issues.append("Program code is not in the correct format")

        # Checks if the program code already exists and if it is not the same as the placeholder text
        elif (self.new_program_code_lineedit.text().strip() in self.get_existing_programs()["Program Code"] and
              self.new_program_code_lineedit.text().strip() != self.new_program_code_lineedit.placeholderText()):
            issues.append("Program code already exists")

        # Checks if the program name already exists and if it is not the same as the placeholder text
        if not self.is_valid.program_name(self.new_program_name_lineedit.text().strip(), edit_state=True):
            issues.append("Program name is not in the correct format")
        elif (self.new_program_name_lineedit.text().strip() in self.get_existing_programs()["Program Name"] and
              self.new_program_name_lineedit.text().strip() != self.new_program_name_lineedit.placeholderText()):
            issues.append("Program name already exists")

        return issues

    def add_signals(self):

        if self.edit_mode == "single":
            self.edit_program_button.clicked.connect(self.edit_single_program_information)
        elif self.edit_mode == "multiple":
            self.edit_program_button.clicked.connect(self.edit_multiple_program_information)

        self.new_program_code_lineedit.textChanged.connect(self.enable_edit_button)
        self.new_program_name_lineedit.textChanged.connect(self.enable_edit_button)
        self.new_college_code_combobox.currentTextChanged.connect(self.enable_edit_button)

    def get_existing_programs(self):
        return self.programs_table_model.db_handler.get_all_existing_programs()

    def get_student_codes(self):
        return self.programs_table_model.db_handler.get_all_entity_information_codes('student')

    def get_program_codes(self):
        return self.programs_table_model.db_handler.get_all_entity_information_codes('program')

    def get_college_codes(self):
        return self.programs_table_model.db_handler.get_all_entity_information_codes('college')

    def set_external_stylesheet(self):
        with open("../assets/qss_files/dialog_style.qss", "r") as file:
            self.setStyleSheet(file.read())

    def load_fonts(self):
        self.cg_font_family = QFontDatabase.applicationFontFamilies(0)[0]

        self.header_label.setFont(QFont(self.cg_font_family, 16, QFont.Weight.DemiBold))

        self.program_to_edit_label.setFont(QFont(self.cg_font_family, 12, QFont.Weight.Medium))
        self.program_to_edit_list.setFont(QFont(self.cg_font_family, 10, QFont.Weight.Medium))
        self.new_program_code_label.setFont(QFont(self.cg_font_family, 12, QFont.Weight.Medium))
        self.new_program_name_label.setFont(QFont(self.cg_font_family, 12, QFont.Weight.Medium))
        self.new_college_code_label.setFont(QFont(self.cg_font_family, 12, QFont.Weight.Medium))

        self.new_program_code_lineedit.setFont(QFont(self.cg_font_family, 12, QFont.Weight.Normal))
        self.new_program_name_lineedit.setFont(QFont(self.cg_font_family, 12, QFont.Weight.Normal))


        self.new_college_code_combobox.setStyleSheet(f"""
                                                        QComboBox {{
                                                            font-family: {self.cg_font_family};
                                                            font-size: 15px;
                                                            font-weight: {QFont.Weight.Normal};
                                                        }}
                                                    """)

        self.edit_program_button.setFont(QFont(self.cg_font_family, 20, QFont.Weight.DemiBold))
