from PyQt6.QtWidgets import QDialog

from colleges.delete_college_design import Ui_Dialog as DeleteCollegeUI

from helper_dialogs.delete_item_state.confirm_delete import ConfirmDeleteDialog
from helper_dialogs.delete_item_state.success_delete_item import SuccessDeleteItemDialog

from utils.get_information_codes import GetInformationCodes

# TODO: Finish delete college
class DeleteCollegeDialog(QDialog, DeleteCollegeUI):
    def __init__(self, colleges_table_view, colleges_table_model, students_table_model, programs_table_model):
        super().__init__()

        self.setupUi(self)

        self.students_table_model = students_table_model
        self.programs_table_model = programs_table_model

        self.colleges_table_view = colleges_table_view
        self.colleges_table_model = colleges_table_model

        self.get_information_codes = GetInformationCodes()

        self.add_college_codes_to_combobox()

        self.delete_college_button.clicked.connect(self.delete_college_from_table)

        self.college_to_delete_combobox.currentTextChanged.connect(self.enable_delete_button)

    def add_college_codes_to_combobox(self):
        for college_code in self.get_information_codes.for_colleges():
            print(college_code)
            self.college_to_delete_combobox.addItem(college_code)

    def delete_college_from_table(self):
        for college in self.colleges_table_model.data_from_csv:
            if college[0] == self.college_to_delete_combobox.currentText():

                college_code_to_delete = self.college_to_delete_combobox.currentText()
                len_of_programs_under_college_code = self.len_of_programs_under_college_code(college_code_to_delete)

                if len_of_programs_under_college_code == 0:
                    self.confirm_to_delete_dialog = ConfirmDeleteDialog("college", college_code_to_delete)
                else:
                    self.confirm_to_delete_dialog = ConfirmDeleteDialog("college",
                                                                        college_code_to_delete,
                                                                        num_of_affected=
                                                                        len_of_programs_under_college_code,
                                                                        information_code_affected=True)

                self.confirm_to_delete_dialog.exec()

                confirm_delete_decision = self.confirm_to_delete_dialog.get_confirm_delete_decision()

                if confirm_delete_decision:
                    self.delete_programs_who_have_college_code(college_code_to_delete)

                    self.colleges_table_model.layoutAboutToBeChanged.emit()
                    self.colleges_table_model.data_from_csv.remove(college)
                    self.colleges_table_model.layoutChanged.emit()

                    self.college_to_delete_combobox.setCurrentText("--Select College Code--")

                    self.success_delete_item_dialog = SuccessDeleteItemDialog("college", self)

                    self.success_delete_item_dialog.exec()

    def enable_delete_button(self):
        if self.college_to_delete_combobox.currentText() in self.get_information_codes.for_colleges():
            self.delete_college_button.setEnabled(True)
        else:
            self.delete_college_button.setEnabled(False)

    def len_of_programs_under_college_code(self, college_code):
        length = 0

        for program in self.programs_table_model.get_data():
            if program[2] == college_code:
                length += 1

        print(length)

        return length

    def delete_programs_who_have_college_code(self, college_code):
        new_data_from_csv = []

        for program in self.programs_table_model.get_data():
            if program[2] != college_code:
                new_data_from_csv.append(program)

        self.programs_table_model.layoutAboutToBeChanged.emit()
        self.programs_table_model.set_data(new_data_from_csv)
        self.programs_table_model.layoutChanged.emit()
