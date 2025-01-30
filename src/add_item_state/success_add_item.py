from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import QSize

from add_item_state.success_add_item_design import Ui_Dialog as SuccessAddItemUI


class SuccessAddItemDialog(QDialog, SuccessAddItemUI):
    def __init__(self, add_item_dialog=None):
        super().__init__()

        self.setupUi(self)

        self.add_item_dialog = add_item_dialog
        self.proceed_button.clicked.connect(self.close_dialog)

    def close_dialog(self):
        if self.add_item_dialog:
            self.add_item_dialog.close()

        self.close()


