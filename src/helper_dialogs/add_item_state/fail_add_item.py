from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import QSize

from helper_dialogs.add_item_state.fail_add_item_design import Ui_Dialog as FailAddItemUI


class FailAddItemDialog(QDialog, FailAddItemUI):
    def __init__(self, issues):
        super().__init__()

        self.setupUi(self)

        self.issues = issues

        self.pushButton.clicked.connect(self.close_dialog)

        self.load_issues()

    def load_issues(self):
        issues_str = '\n'.join(self.issues)

        additional_space = (len(self.issues) - 1) * 15

        print(issues_str)

        self.label_2.setText(issues_str)

        self.setMinimumHeight(self.height() + additional_space)
        self.setMaximumHeight(self.height())



    def close_dialog(self):
        self.close()
