from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QFontDatabase

from operation_dialogs.students.edit_student_design import Ui_Dialog as EditStudentUI

from helper_dialogs.edit_item_state.fail_to_edit_item import FailToEditItemDialog
from helper_dialogs.edit_item_state.success_edit_item import SuccessEditItemDialog
from helper_dialogs.edit_item_state.confirm_edit import ConfirmEditDialog

from utils.is_valid_verifiers import IsValidVerifiers


class EditStudentDialog(QDialog, EditStudentUI):
    def __init__(self, students_table_view, students_table_model, reset_item_delegates_func,
                 id_numbers_to_edit, selected_rows):
        super().__init__()

        self.setupUi(self)

        self.set_external_stylesheet()
        self.load_fonts()

        self.reset_item_delegates_func = reset_item_delegates_func

        self.students_table_view = students_table_view
        self.students_table_model = students_table_model

        self.id_numbers_to_edit = id_numbers_to_edit
        self.selected_rows = selected_rows

        if len(self.id_numbers_to_edit) == 1:
            self.set_old_data_as_placeholders()

            self.edit_mode = "single"
        else:
            self.populate_student_to_edit_list()
            self.disable_fields()

            self.edit_mode = "multiple"

        self.is_valid = IsValidVerifiers()

        self.add_program_codes_to_combobox()
        self.add_college_codes_to_combobox()

        self.add_signals()

        self.set_program_code_combobox_scrollbar()
        self.set_college_code_combobox_scrollbar()

    def populate_student_to_edit_list(self):

        formatted_string = ""

        for index, id_number in enumerate(self.id_numbers_to_edit):

            # Show 10 id_numbers at maximum
            if index == 9:
                formatted_string += f"{str(id_number)}..."
                break
            if index + 1 == len(self.id_numbers_to_edit):
                formatted_string += f"{str(id_number)}"
            else:
                formatted_string += f"{str(id_number)}, "

            if index + 1 % 3 == 0:
                formatted_string += "\n"

        self.setWindowTitle("Edit students")
        self.student_to_edit_label.setText("Students To Be Edited")
        self.student_to_edit_list.setText(formatted_string)

    def disable_fields(self):
        self.new_id_number_label.close()
        self.new_id_number_lineedit.close()

        self.new_first_name_label.close()
        self.new_first_name_lineedit.close()

        self.new_last_name_label.close()
        self.new_last_name_lineedit.close()

        self.setMinimumSize(QSize(445, 370))
        self.setMaximumSize(QSize(445, 370))

        self.resize(445, 370)

    def edit_single_student_information(self):
        issues = self.find_issues()

        if issues:
            self.fail_to_edit_item_dialog = FailToEditItemDialog(issues, "student")
            self.fail_to_edit_item_dialog.exec()

        else:

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

            actual_row_to_edit = ((self.students_table_model.max_row_per_page *
                                   (self.students_table_model.current_page_number - 1))
                                  + self.selected_rows[0])

            # Check if there are any changes made from the old data of the student
            if self.students_table_model.get_data()[actual_row_to_edit] != student_to_edit:

                # old_student_id_number = self.student_to_edit_combobox.currentText()
                self.confirm_to_edit_dialog = ConfirmEditDialog("student",
                                                                self.id_numbers_to_edit)

                # Halts the program whereas this starts another loop
                self.confirm_to_edit_dialog.exec()

                confirm_edit_decision = self.confirm_to_edit_dialog.get_confirm_edit_decision()

                if confirm_edit_decision:

                    # By doing this, the data in the model also gets updated, same reference
                    # self.students_table_model.get_data()[row_to_edit] = student_to_edit
                    self.students_table_model.update_entity(student_to_edit,
                                                            'student',
                                                            actual_row_to_edit=actual_row_to_edit,
                                                            edit_mode=self.edit_mode)

                    self.students_table_model.set_has_changes(True)

                    self.reset_item_delegates_func("edit_student")

                    self.success_edit_item_dialog = SuccessEditItemDialog("student", self)
                    self.success_edit_item_dialog.exec()
            else:
                self.fail_to_edit_item_dialog = FailToEditItemDialog(["No changes made to the student"], "student")
                self.fail_to_edit_item_dialog.exec()

    def edit_multiple_student_information(self):

        students_to_edit = ["",
                           "",
                           "",
                           self.new_year_level_combobox.currentText(),
                           self.new_gender_combobox.currentText(),
                           self.new_program_code_combobox.currentText()]

        self.confirm_to_edit_dialog = ConfirmEditDialog("student",
                                                        self.id_numbers_to_edit)

        # Halts the program whereas this starts another loop
        self.confirm_to_edit_dialog.exec()

        confirm_edit_decision = self.confirm_to_edit_dialog.get_confirm_edit_decision()

        if confirm_edit_decision:

            for selected_row in self.selected_rows:

                actual_row_to_edit = ((self.students_table_model.max_row_per_page *
                                       (self.students_table_model.current_page_number - 1))
                                      + selected_row)

                # By doing this, the data in the model also gets updated, same reference
                # self.students_table_model.get_data()[row_to_edit] = student_to_edit

                # list(students_to_edit) creates another copy that doesn't manipulate students_to_edit
                self.students_table_model.update_entity(list(students_to_edit),
                                                        'student',
                                                        actual_row_to_edit=actual_row_to_edit,
                                                        edit_mode=self.edit_mode)

            self.students_table_model.set_has_changes(True)

            self.reset_item_delegates_func("edit_student")

            self.success_edit_item_dialog = SuccessEditItemDialog("student", self.id_numbers_to_edit, self)
            self.success_edit_item_dialog.exec()

    def add_program_codes_to_combobox(self):
        for program_code in self.get_program_codes():
            self.new_program_code_combobox.addItem(program_code)

    def add_college_codes_to_combobox(self):
        for college_code in self.get_college_codes():
            self.college_code_combobox.addItem(college_code)

    def set_program_code_combobox_scrollbar(self):
        self.new_program_code_combobox.view().setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    def set_college_code_combobox_scrollbar(self):
        self.college_code_combobox.view().setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    def enable_edit_button(self):

        if (self.new_year_level_combobox.currentText() != "--Select year level--" or
                self.new_gender_combobox.currentText() != "--Select gender--" or
                (self.new_program_code_combobox.currentText() != "--Select a program--" and
                self.new_program_code_combobox.currentText() != "" and
                self.new_program_code_combobox.currentText() in self.get_program_codes())):

            self.edit_student_button.setEnabled(True)
        else:
            self.edit_student_button.setEnabled(False)

    def set_old_data_as_placeholders(self):
        # TODO: index is unused
        for index, student in enumerate(self.students_table_model.get_data()):
            if student[0] == self.id_numbers_to_edit[0]:

                self.new_id_number_lineedit.setPlaceholderText(student[0])
                self.new_first_name_lineedit.setPlaceholderText(student[1])
                self.new_last_name_lineedit.setPlaceholderText(student[2])
                self.new_year_level_combobox.setCurrentText(student[3])
                self.new_gender_combobox.setCurrentText(student[4])

                # student[5] is the program code
                for program_college_connection in (self.students_table_model.db_handler.
                        get_colleges_and_programs_connections().items()):

                    if student[5] in program_college_connection[1]:
                        self.college_code_combobox.setCurrentText(program_college_connection[0])
                        break

                self.new_program_code_combobox.setCurrentText(student[5])

    def filter_program_codes(self):
        college_code = self.college_code_combobox.currentText()

        if college_code != "--Select a college--" and college_code in self.get_college_codes():
            self.reset_program_code_combobox()
            self.add_program_codes_from_a_college_to_combobox(college_code)

        elif college_code != "":
            self.reset_program_code_combobox()
            self.add_program_codes_to_combobox()

    def add_program_codes_from_a_college_to_combobox(self, college_code):
        num_of_programs = 0

        college_to_program_connections = self.students_table_model.db_handler.get_colleges_and_programs_connections()

        for program_code in self.get_program_codes():
            if program_code in college_to_program_connections[college_code]:
                self.new_program_code_combobox.addItem(program_code)

                num_of_programs += 1

        if num_of_programs == 0:
            self.reset_program_code_combobox(has_programs=False)

    def reset_program_code_combobox(self, has_programs=True):
        self.new_program_code_combobox.clear()

        if has_programs:
            self.new_program_code_combobox.addItem("--Select a program--")
        else:
            self.new_program_code_combobox.addItem("--No programs available--")

    def find_issues(self):
        issues = []

        if not self.is_valid.id_number(self.new_id_number_lineedit.text().strip(), edit_state=True):
            issues.append("ID Number is not in the correct format")

        # Checks if the id number already exists and if it is not the same as the placeholder text
        elif (self.new_id_number_lineedit.text().strip() in self.get_existing_students()["ID Number"] and
              self.new_id_number_lineedit.text().strip() != self.new_id_number_lineedit.placeholderText()):
            issues.append("ID Number already exists")

        if not self.is_valid.first_name(self.new_first_name_lineedit.text().strip(), edit_state=True):
            issues.append("First name is not in the correct format")

        if not self.is_valid.last_name(self.new_last_name_lineedit.text().strip(), edit_state=True):
            issues.append("Last name is not in the correct format")

        full_name_list = [self.new_first_name_lineedit.text().strip()
                          if self.new_first_name_lineedit.text().strip()
                          else self.new_first_name_lineedit.placeholderText(),
                          self.new_last_name_lineedit.text().strip()
                          if self.new_last_name_lineedit.text().strip()
                          else self.new_last_name_lineedit.placeholderText()]

        full_name_str = f"{full_name_list[0]} {full_name_list[1]}"

        # Checks if the name combination already exists and if it is not the same as the placeholder texts
        if (full_name_str in self.get_existing_students()["Full Name"] and
                full_name_list[0] != self.new_first_name_lineedit.placeholderText() and
                full_name_list[1] != self.new_first_name_lineedit.placeholderText()):

            issues.append("Name combination already exists")

        return issues

    def add_signals(self):
        if self.edit_mode == "single":
            self.edit_student_button.clicked.connect(self.edit_single_student_information)
        elif self.edit_mode == "multiple":
            self.edit_student_button.clicked.connect(self.edit_multiple_student_information)

        self.new_year_level_combobox.currentTextChanged.connect(self.enable_edit_button)
        self.new_gender_combobox.currentTextChanged.connect(self.enable_edit_button)
        self.new_program_code_combobox.currentTextChanged.connect(self.enable_edit_button)

        self.college_code_combobox.currentTextChanged.connect(self.filter_program_codes)

    def get_existing_students(self):
        return self.students_table_model.db_handler.get_all_existing_students()

    def get_student_id_numbers(self):
        return self.students_table_model.db_handler.get_all_entity_information_codes('student')

    def get_program_codes(self):
        return self.students_table_model.db_handler.get_all_entity_information_codes('program')

    def get_college_codes(self):
        return self.students_table_model.db_handler.get_all_entity_information_codes('college')

    def set_external_stylesheet(self):
        with open("../assets/qss_files/dialog_style.qss", "r") as file:
            self.setStyleSheet(file.read())

    def load_fonts(self):
        self.cg_font_family = QFontDatabase.applicationFontFamilies(0)[0]

        self.header_label.setFont(QFont(self.cg_font_family, 16, QFont.Weight.DemiBold))

        self.student_to_edit_label.setFont(QFont(self.cg_font_family, 12, QFont.Weight.Medium))
        self.student_to_edit_list.setFont(QFont(self.cg_font_family, 10, QFont.Weight.Medium))
        self.new_id_number_label.setFont(QFont(self.cg_font_family, 12, QFont.Weight.Medium))
        self.new_first_name_label.setFont(QFont(self.cg_font_family, 12, QFont.Weight.Medium))
        self.new_last_name_label.setFont(QFont(self.cg_font_family, 12, QFont.Weight.Medium))
        self.new_year_level_label.setFont(QFont(self.cg_font_family, 12, QFont.Weight.Medium))
        self.new_gender_label.setFont(QFont(self.cg_font_family, 12, QFont.Weight.Medium))
        self.college_code_filter_label.setFont(QFont(self.cg_font_family, 12, QFont.Weight.Medium))
        self.new_program_code_label.setFont(QFont(self.cg_font_family, 12, QFont.Weight.Medium))

        self.new_id_number_lineedit.setFont(QFont(self.cg_font_family, 12, QFont.Weight.Normal))
        self.new_first_name_lineedit.setFont(QFont(self.cg_font_family, 12, QFont.Weight.Normal))
        self.new_last_name_lineedit.setFont(QFont(self.cg_font_family, 12, QFont.Weight.Normal))

        self.new_year_level_combobox.setStyleSheet(f"""
                                    QComboBox {{
                                        font-family: {self.cg_font_family};
                                        font-size: 15px;
                                        font-weight: {QFont.Weight.Normal};
                                    }}
                                """)

        self.new_gender_combobox.setStyleSheet(f"""
                                    QComboBox {{
                                        font-family: {self.cg_font_family};
                                        font-size: 15px;
                                        font-weight: {QFont.Weight.Normal};
                                    }}
                                """)

        self.college_code_combobox.setStyleSheet(f"""
                                    QComboBox {{
                                        font-family: {self.cg_font_family};
                                        font-size: 15px;
                                        font-weight: {QFont.Weight.Normal};
                                    }}
                                """)

        self.new_program_code_combobox.setStyleSheet(f"""
                                    QComboBox {{
                                        font-family: {self.cg_font_family};
                                        font-size: 15px;
                                        font-weight: {QFont.Weight.Normal};
                                    }}
                                """)

        self.edit_student_button.setFont(QFont(self.cg_font_family, 20, QFont.Weight.DemiBold))
