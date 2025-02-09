from PyQt6.QtWidgets import QDialog

from helper_dialogs.save_item_state.confirm_save_design import Ui_Dialog as ConfirmSaveUI


class ConfirmSaveDialog(QDialog, ConfirmSaveUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.confirm_edit_decision = False

        self.yes_button.clicked.connect(self.proceed_edit)
        self.no_button.clicked.connect(self.close_dialog)

    def proceed_edit(self):
        self.confirm_edit_decision = True
        self.close_dialog()

    def close_dialog(self):
        self.close()

    def get_confirm_edit_decision(self):
        return self.confirm_edit_decision

