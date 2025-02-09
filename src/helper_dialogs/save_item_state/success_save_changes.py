from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import QSize

from helper_dialogs.save_item_state.success_save_changes_design import Ui_Dialog as SuccessChangesItemUI


class SuccessSaveChangesDialog(QDialog, SuccessChangesItemUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.proceed_button.clicked.connect(self.close_dialog)

    def close_dialog(self):

        self.close()
