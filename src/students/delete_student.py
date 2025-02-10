from PyQt6.QtWidgets import QDialog

from students.delete_student_design import Ui_Dialog as DeleteStudentUI

from helper_dialogs.delete_item_state.confirm_delete import ConfirmDeleteDialog
from helper_dialogs.delete_item_state.success_delete_item import SuccessDeleteItemDialog

from utils.get_information_codes import GetInformationCodes


class DeleteStudentDialog(QDialog, DeleteStudentUI):
    def __init__(self, students_table_view, students_table_model):
        super().__init__()

        self.setupUi(self)

        self.students_table_view = students_table_view
        self.students_table_model = students_table_model

        self.get_information_codes = GetInformationCodes()

        self.add_id_numbers_to_combobox()

        self.delete_student_button.clicked.connect(self.delete_student_from_table)

        self.student_to_delete_combobox.currentTextChanged.connect(self.enable_delete_button)

    def add_id_numbers_to_combobox(self):
        for id_number in self.get_information_codes.for_students():
            print(id_number)
            self.student_to_delete_combobox.addItem(id_number)

    def delete_student_from_table(self):
        for student in self.students_table_model.data_from_csv:
            if student[0] == self.student_to_delete_combobox.currentText():

                id_number_to_delete = self.student_to_delete_combobox.currentText()

                self.confirm_to_delete_dialog = ConfirmDeleteDialog("student", id_number_to_delete)
                self.confirm_to_delete_dialog.exec()

                confirm_delete_decision = self.confirm_to_delete_dialog.get_confirm_delete_decision()

                if confirm_delete_decision:
                    self.students_table_model.layoutAboutToBeChanged.emit()
                    self.students_table_model.data_from_csv.remove(student)
                    self.students_table_model.layoutChanged.emit()

                    self.students_table_model.set_has_changes(True)

                    self.success_delete_item_dialog = SuccessDeleteItemDialog("student", self)

                    self.success_delete_item_dialog.exec()

    def enable_delete_button(self):
        if self.student_to_delete_combobox.currentText() in self.get_information_codes.for_students():
            self.delete_student_button.setEnabled(True)
        else:
            self.delete_student_button.setEnabled(False)
