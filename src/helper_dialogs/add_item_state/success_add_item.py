from PyQt6.QtWidgets import QDialog

from helper_dialogs.add_item_state.success_add_item_design import Ui_Dialog as SuccessAddItemUI


class SuccessAddItemDialog(QDialog, SuccessAddItemUI):
    def __init__(self, add_item_type, add_item_dialog=None):
        super().__init__()

        self.setupUi(self)

        self.set_external_stylesheet()

        self.add_item_type = add_item_type
        self.add_item_dialog = add_item_dialog

        self.proceed_button.clicked.connect(self.close_dialog)

        self.edit_message()

    def edit_message(self):

        if self.add_item_type == "student":
            self.message_label.setText("No issues found when adding the student")
        elif self.add_item_type == "program":
            self.message_label.setText("No issues found when adding the program")
        elif self.add_item_type == "college":
            self.message_label.setText("No issues found when adding the college")

    def close_dialog(self):
        if self.add_item_dialog:
            self.add_item_dialog.close()

        self.close()

    def set_external_stylesheet(self):

        with open("../assets/qss_files/dialog_style.qss", "r") as file:
            self.setStyleSheet(file.read())


