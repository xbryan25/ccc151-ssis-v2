from PyQt6.QtWidgets import QDialog

from helper_dialogs.save_item_state.confirm_save_design import Ui_Dialog as ConfirmSaveUI


class ConfirmSaveDialog(QDialog, ConfirmSaveUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.set_external_stylesheet()

        self.confirm_edit_decision = False

        self.add_signals()

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