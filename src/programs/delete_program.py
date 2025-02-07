from PyQt6.QtWidgets import QDialog

from programs.delete_program_design import Ui_Dialog as DeleteProgramUI

from helper_dialogs.delete_item_state.confirm_delete import ConfirmDeleteDialog
from helper_dialogs.delete_item_state.success_delete_item import SuccessDeleteItemDialog

from utils.get_information_codes import GetInformationCodes


class DeleteProgramDialog(QDialog, DeleteProgramUI):
    def __init__(self, programs_table_view, programs_table_model, students_table_model):
        super().__init__()

        self.setupUi(self)

        self.students_table_model = students_table_model

        self.programs_table_view = programs_table_view
        self.programs_table_model = programs_table_model

        self.get_information_codes = GetInformationCodes()

        self.add_program_codes_to_combobox()

        self.delete_program_button.clicked.connect(self.delete_program_from_table)

        self.program_to_delete_combobox.currentTextChanged.connect(self.enable_delete_button)

    def add_program_codes_to_combobox(self):
        for program_code in self.get_information_codes.for_programs():
            print(program_code)
            self.program_to_delete_combobox.addItem(program_code)

    def delete_program_from_table(self):
        for program in self.programs_table_model.data_from_csv:
            if program[0] == self.program_to_delete_combobox.currentText():

                program_code_to_delete = self.program_to_delete_combobox.currentText()
                len_of_students_under_program_code = self.len_of_students_under_program_code(program_code_to_delete)

                if len_of_students_under_program_code == 0:
                    self.confirm_to_delete_dialog = ConfirmDeleteDialog("program", program_code_to_delete)
                else:
                    self.confirm_to_delete_dialog = ConfirmDeleteDialog("program",
                                                                        program_code_to_delete,
                                                                        num_of_affected=
                                                                        len_of_students_under_program_code,
                                                                        information_code_affected=True)

                self.confirm_to_delete_dialog.exec()

                confirm_delete_decision = self.confirm_to_delete_dialog.get_confirm_delete_decision()

                if confirm_delete_decision:
                    self.delete_students_who_have_program_code(program_code_to_delete)

                    self.programs_table_model.layoutAboutToBeChanged.emit()
                    self.programs_table_model.data_from_csv.remove(program)
                    self.programs_table_model.layoutChanged.emit()

                    self.program_to_delete_combobox.setCurrentText("--Select Program Code--")

                    self.success_delete_item_dialog = SuccessDeleteItemDialog("program", self)

                    self.success_delete_item_dialog.exec()

    def enable_delete_button(self):
        if self.program_to_delete_combobox.currentText() in self.get_information_codes.for_programs():
            self.delete_program_button.setEnabled(True)
        else:
            self.delete_program_button.setEnabled(False)

    def len_of_students_under_program_code(self, program_code):
        length = 0

        for student in self.students_table_model.get_data():
            if student[5] == program_code:
                length += 1

        print(length)

        return length

    def delete_students_who_have_program_code(self, program_code):
        new_data_from_csv = []

        for student in self.students_table_model.get_data():
            if student[5] != program_code:
                new_data_from_csv.append(student)

        self.students_table_model.layoutAboutToBeChanged.emit()
        self.students_table_model.set_data(new_data_from_csv)
        self.students_table_model.layoutChanged.emit()
