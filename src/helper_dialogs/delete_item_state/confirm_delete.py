from PyQt6.QtWidgets import QDialog

from helper_dialogs.delete_item_state.confirm_delete_design import Ui_Dialog as ConfirmDeleteUI


class ConfirmDeleteDialog(QDialog, ConfirmDeleteUI):
    def __init__(self, information_type, information_to_delete, num_of_affected=None, information_code_affected=False):
        super().__init__()

        self.setupUi(self)

        self.set_external_stylesheet()

        self.confirm_delete_decision = False

        self.information_type = information_type
        self.information_to_delete = information_to_delete

        if num_of_affected is None:
            self.num_of_affected = {}
        else:
            self.num_of_affected = num_of_affected

        self.information_code_affected = information_code_affected

        self.add_signals()

        self.edit_label_texts()

    def edit_label_texts(self):
        self.setWindowTitle(f"Proceed in deleting {self.information_to_delete}?")
        self.header_label.setText(f"Are you sure you want to remove this {self.information_type}?")

        if self.information_code_affected:
            student_text = "students"
            program_text = "programs"

            if "students" in self.num_of_affected and self.num_of_affected["students"] == 1:
                student_text = "student"

            if "programs" in self.num_of_affected and self.num_of_affected["programs"] == 1:
                program_text = "program"

            if self.information_type == "program":
                self.affected_num_label.setText(f"{self.num_of_affected["students"]} {student_text} "
                                                f"under this program will also be removed")

            elif self.information_type == "college":
                self.affected_num_label.setText(f"{self.num_of_affected["students"]} {student_text} and "
                                                f"{self.num_of_affected["programs"]} {program_text} "
                                                f"under this college will also be removed")

                self.setMinimumWidth(520)
                self.setMaximumWidth(520)
                self.resize(520, 145)

        else:
            self.affected_num_label.close()
            self.verticalLayout.removeItem(self.spacerItem2)
            self.setMinimumHeight(105)
            self.resize(495, 105)

    def proceed_delete(self):
        self.confirm_delete_decision = True
        self.close_dialog()

    def close_dialog(self):
        self.close()

    def get_confirm_delete_decision(self):
        return self.confirm_delete_decision

    def add_signals(self):
        self.yes_button.clicked.connect(self.proceed_delete)
        self.no_button.clicked.connect(self.close_dialog)

    def set_external_stylesheet(self):

        with open("../assets/qss_files/dialog_style.qss", "r") as file:
            self.setStyleSheet(file.read())