from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QFont, QFontDatabase

from helper_dialogs.save_or_undo_state.success_save_changes_design import Ui_Dialog as SuccessChangesItemUI


class SuccessSaveChangesDialog(QDialog, SuccessChangesItemUI):
    def __init__(self, save_or_undo):
        super().__init__()

        self.setupUi(self)

        self.set_external_stylesheet()
        self.load_fonts()

        self.save_or_undo = save_or_undo

        self.set_text()

        self.proceed_button.clicked.connect(self.close_dialog)

    def close_dialog(self):
        self.close()

    def set_text(self):
        if self.save_or_undo == "save":
            self.message_label.setText("No issues found when saving the changes")
        elif self.save_or_undo == "undo":
            self.message_label.setText("No issues found when undoing the changes")

    def set_external_stylesheet(self):
        with open("../assets/qss_files/dialog_style.qss", "r") as file:
            self.setStyleSheet(file.read())

    def load_fonts(self):
        self.cg_font_family = QFontDatabase.applicationFontFamilies(0)[0]

        self.message_label.setFont(QFont(self.cg_font_family, 16, QFont.Weight.DemiBold))
        self.proceed_button.setFont(QFont(self.cg_font_family, 14, QFont.Weight.Medium))
