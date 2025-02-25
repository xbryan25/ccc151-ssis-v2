from PyQt6.QtWidgets import QDialog

from helper_dialogs.delete_item_state.success_delete_item_design import Ui_Dialog as SuccessDeleteItemUI


class SuccessDeleteItemDialog(QDialog, SuccessDeleteItemUI):
    def __init__(self, delete_item_type, delete_item_dialog=None):
        super().__init__()

        self.setupUi(self)

        self.set_external_stylesheet()

        self.delete_item_type = delete_item_type
        self.delete_item_dialog = delete_item_dialog

        self.proceed_button.clicked.connect(self.close_dialog)

        self.edit_message()

    def edit_message(self):
        if self.delete_item_type == "student":
            self.message_label.setText("No issues found when deleting the student")
        elif self.delete_item_type == "program":
            self.message_label.setText("No issues found when deleting the program")
        elif self.delete_item_type == "college":
            self.message_label.setText("No issues found when deleting the college")

    def close_dialog(self):
        if self.delete_item_dialog:
            self.delete_item_dialog.close()

        self.close()

    def set_external_stylesheet(self):

        with open("../assets/qss_files/dialog_style.qss", "r") as file:
            self.setStyleSheet(file.read())
