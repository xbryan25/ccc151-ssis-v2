from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import QSize

from helper_dialogs.add_item_state.fail_add_item_design import Ui_Dialog as FailAddItemUI


class FailAddItemDialog(QDialog, FailAddItemUI):
    def __init__(self, issues, type):
        super().__init__()

        self.setupUi(self)

        self.issues = issues
        self.type = type

        self.pushButton.clicked.connect(self.close_dialog)

        self.load_issues()
        self.edit_window_title()

    def load_issues(self):
        issues_str = '\n'.join(self.issues)

        additional_space = (len(self.issues) - 1) * 15

        print(issues_str)

        self.label_2.setText(issues_str)

        self.setMinimumHeight(self.height() + additional_space)
        self.setMaximumHeight(self.height())

    def edit_window_title(self):
        if self.type == "student":
            self.setWindowTitle("Fail to add student")
        elif self.type == "program":
            self.setWindowTitle("Fail to add program")
        elif self.type == "college":
            self.setWindowTitle("Fail to add college")

    def close_dialog(self):
        self.close()
