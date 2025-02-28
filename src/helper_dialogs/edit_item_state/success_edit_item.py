from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QFont, QFontDatabase

from helper_dialogs.edit_item_state.success_edit_item_design import Ui_Dialog as SuccessEditItemUI


class SuccessEditItemDialog(QDialog, SuccessEditItemUI):
    def __init__(self, edit_item_type, edit_item_dialog=None):
        super().__init__()

        self.setupUi(self)

        self.set_external_stylesheet()
        self.load_fonts()

        self.edit_item_type = edit_item_type
        self.edit_item_dialog = edit_item_dialog

        self.proceed_button.clicked.connect(self.close_dialog)

        self.edit_message()

    def edit_message(self):
        if self.edit_item_type == "student":
            self.message_label.setText("No issues found when editing the student")
        elif self.edit_item_type == "program":
            self.message_label.setText("No issues found when editing the program")
        elif self.edit_item_type == "college":
            self.message_label.setText("No issues found when editing the college")

    def close_dialog(self):
        if self.edit_item_dialog:
            self.edit_item_dialog.close()

        self.close()

    def set_external_stylesheet(self):
        with open("../assets/qss_files/dialog_style.qss", "r") as file:
            self.setStyleSheet(file.read())

    def load_fonts(self):
        self.cg_font_family = QFontDatabase.applicationFontFamilies(0)[0]

        self.message_label.setFont(QFont(self.cg_font_family, 16, QFont.Weight.DemiBold))
        self.proceed_button.setFont(QFont(self.cg_font_family, 14, QFont.Weight.Medium))
