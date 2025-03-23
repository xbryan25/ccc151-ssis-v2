from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QFont, QFontDatabase

from operation_dialogs.students.delete_student_design import Ui_Dialog as DeleteStudentUI

from helper_dialogs.delete_item_state.confirm_delete import ConfirmDeleteDialog
from helper_dialogs.delete_item_state.success_delete_item import SuccessDeleteItemDialog


class DeleteStudentDialog(QDialog, DeleteStudentUI):
    def __init__(self, students_table_view, students_table_model, reset_item_delegates_func,
                 horizontal_header):

        super().__init__()

        self.setupUi(self)

        self.set_external_stylesheet()
        self.load_fonts()

        self.reset_item_delegates_func = reset_item_delegates_func
        self.horizontal_header = horizontal_header

        self.students_table_view = students_table_view
        self.students_table_model = students_table_model

        self.add_id_numbers_to_combobox()

        self.add_signals()

    def add_id_numbers_to_combobox(self):
        for id_number in self.get_student_id_numbers():
            self.student_to_delete_combobox.addItem(id_number)

    def delete_student_from_model(self):
        for student in self.students_table_model.get_data():
            if student[0] == self.student_to_delete_combobox.currentText():

                id_number_to_delete = self.student_to_delete_combobox.currentText()

                self.confirm_to_delete_dialog = ConfirmDeleteDialog("student", id_number_to_delete)
                self.confirm_to_delete_dialog.exec()

                confirm_delete_decision = self.confirm_to_delete_dialog.get_confirm_delete_decision()

                if confirm_delete_decision:
                    self.students_table_model.layoutAboutToBeChanged.emit()

                    self.students_table_model.delete_entity(student, 'student')

                    self.students_table_model.layoutChanged.emit()

                    self.reset_item_delegates_func("delete_student")

                    self.students_table_model.set_has_changes(True)

                    self.success_delete_item_dialog = SuccessDeleteItemDialog("student", self)
                    self.success_delete_item_dialog.exec()

    def enable_delete_button(self):
        if self.student_to_delete_combobox.currentText() in self.get_student_id_numbers():
            self.delete_student_button.setEnabled(True)
        else:
            self.delete_student_button.setEnabled(False)

    def add_signals(self):
        self.delete_student_button.clicked.connect(self.delete_student_from_model)
        self.student_to_delete_combobox.currentTextChanged.connect(self.enable_delete_button)

    def get_student_id_numbers(self):
        return self.students_table_model.db_handler.get_all_entity_information_codes('student')

    def set_external_stylesheet(self):
        with open("../assets/qss_files/dialog_style.qss", "r") as file:
            self.setStyleSheet(file.read())

    def load_fonts(self):
        self.cg_font_family = QFontDatabase.applicationFontFamilies(0)[0]

        self.header_label.setFont(QFont(self.cg_font_family, 16, QFont.Weight.DemiBold))

        self.id_number_label.setFont(QFont(self.cg_font_family, 12, QFont.Weight.Medium))

        self.student_to_delete_combobox.setStyleSheet(f"""
                                            QComboBox {{
                                                font-family: {self.cg_font_family};
                                                font-size: 15px;
                                                font-weight: {QFont.Weight.Normal};
                                            }}
                                        """)

        self.delete_student_button.setFont(QFont(self.cg_font_family, 20, QFont.Weight.DemiBold))
