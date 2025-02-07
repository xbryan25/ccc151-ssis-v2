from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import QSize

from helper_dialogs.delete_item_state.confirm_delete_design import Ui_Dialog as ConfirmDeleteUI


class ConfirmDeleteDialog(QDialog, ConfirmDeleteUI):
    def __init__(self, information_type, information_to_delete, num_of_affected=0, information_code_affected=False):
        super().__init__()

        self.setupUi(self)

        self.confirm_delete_decision = False

        self.information_type = information_type
        self.information_to_delete = information_to_delete
        self.num_of_affected = num_of_affected
        self.information_code_affected = information_code_affected

        self.yes_button.clicked.connect(self.proceed_delete)
        self.no_button.clicked.connect(self.close_dialog)

        self.edit_label_texts()

    def edit_label_texts(self):
        self.setWindowTitle(f"Proceed in deleting {self.information_to_delete}?")
        self.header_label.setText(f"Are you sure you want to remove this {self.information_type}?")

        if self.information_code_affected:
            if self.information_type == "program":
                if self.num_of_affected == 1:
                    self.affected_num_label.setText(f"{self.num_of_affected} student "
                                                    f"under this program will also be removed")
                else:
                    self.affected_num_label.setText(f"{self.num_of_affected} students "
                                                    f"under this program will also be removed")
            elif self.information_type == "college":
                if self.num_of_affected == 1:
                    self.affected_num_label.setText(f"{self.num_of_affected} program "
                                                    f"under this college will also be removed")
                else:
                    self.affected_num_label.setText(f"{self.num_of_affected} programs "
                                                    f"under this college will also be removed")
        else:
            self.affected_num_label.close()
            self.verticalLayout.removeItem(self.spacerItem2)
            self.resize(495, 105)

    def proceed_delete(self):
        self.confirm_delete_decision = True
        self.close_dialog()

    def close_dialog(self):
        self.close()

    def get_confirm_delete_decision(self):
        return self.confirm_delete_decision
