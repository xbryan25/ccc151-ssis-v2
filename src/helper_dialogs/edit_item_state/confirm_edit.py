from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import QSize

from helper_dialogs.edit_item_state.confirm_edit_design import Ui_Dialog as ConfirmEditUI


class ConfirmEditDialog(QDialog, ConfirmEditUI):
    def __init__(self, information_type, information_to_edit, num_of_affected=0, information_code_affected=False):
        super().__init__()

        self.setupUi(self)

        self.set_external_stylesheet()

        self.confirm_edit_decision = False

        self.information_type = information_type
        self.information_to_edit = information_to_edit
        self.num_of_affected = num_of_affected
        self.information_code_affected = information_code_affected

        self.add_signals()

        self.edit_label_texts()

    def edit_label_texts(self):
        self.setWindowTitle(f"Proceed in editing {self.information_to_edit}?")
        self.header_label.setText(f"Are you sure you want to edit this {self.information_type}?")

        if self.information_code_affected:
            if self.information_type == "program":
                if self.num_of_affected == 1:
                    self.affected_num_label.setText(f"{self.num_of_affected} student "
                                                    f"under this program will be affected")
                else:
                    self.affected_num_label.setText(f"{self.num_of_affected} students "
                                                    f"under this program will be affected")
            elif self.information_type == "college":
                if self.num_of_affected == 1:
                    self.affected_num_label.setText(f"{self.num_of_affected} program "
                                                    f"under this college will be affected")
                else:
                    self.affected_num_label.setText(f"{self.num_of_affected} programs "
                                                    f"under this college will be affected")
        else:
            self.affected_num_label.close()
            self.verticalLayout.removeItem(self.spacerItem2)
            self.resize(495, 105)

    def proceed_edit(self):
        self.confirm_edit_decision = True
        self.close_dialog()

    def close_dialog(self):
        self.close()

    def get_confirm_edit_decision(self):
        return self.confirm_edit_decision

    def add_signals(self):
        self.yes_button.clicked.connect(self.proceed_edit)
        self.no_button.clicked.connect(self.close_dialog)

    def set_external_stylesheet(self):

        with open("../assets/qss_files/dialog_style.qss", "r") as file:
            self.setStyleSheet(file.read())
