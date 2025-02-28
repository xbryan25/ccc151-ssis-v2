from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QFont, QFontDatabase

from helper_dialogs.edit_item_state.fail_to_edit_item_design import Ui_Dialog as FailToEditItemUI


class FailToEditItemDialog(QDialog, FailToEditItemUI):
    def __init__(self, issues, information_type):
        super().__init__()

        self.setupUi(self)

        self.set_external_stylesheet()
        self.load_fonts()

        self.issues = issues
        self.information_type = information_type

        self.proceed_button.clicked.connect(self.close_dialog)

        self.load_issues()
        self.edit_window_title()

    def load_issues(self):
        issues_str = '\n'.join(self.issues)

        additional_space = (len(self.issues) - 1) * 15

        self.issues_label.setText(issues_str)

        self.setMinimumHeight(self.height() + additional_space)
        self.setMaximumHeight(self.height())

    def edit_window_title(self):
        if self.information_type == "student":
            self.setWindowTitle("Fail to edit student")
        elif self.information_type == "program":
            self.setWindowTitle("Fail to edit program")
        elif self.information_type == "college":
            self.setWindowTitle("Fail to edit college")

    def close_dialog(self):
        self.close()

    def set_external_stylesheet(self):
        with open("../assets/qss_files/dialog_style.qss", "r") as file:
            self.setStyleSheet(file.read())

    def load_fonts(self):
        self.cg_font_family = QFontDatabase.applicationFontFamilies(0)[0]

        self.header_label.setFont(QFont(self.cg_font_family, 16, QFont.Weight.DemiBold))

        self.issues_label.setFont(QFont(self.cg_font_family, 10, QFont.Weight.Medium))
        self.proceed_button.setFont(QFont(self.cg_font_family, 14, QFont.Weight.Medium))
