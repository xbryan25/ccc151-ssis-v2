from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QFont, QFontDatabase

from helper_dialogs.save_item_state.success_save_changes_design import Ui_Dialog as SuccessChangesItemUI


class SuccessSaveChangesDialog(QDialog, SuccessChangesItemUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.set_external_stylesheet()
        self.load_fonts()

        self.proceed_button.clicked.connect(self.close_dialog)

    def close_dialog(self):
        self.close()

    def set_external_stylesheet(self):
        with open("../assets/qss_files/dialog_style.qss", "r") as file:
            self.setStyleSheet(file.read())

    def load_fonts(self):
        self.cg_font_family = QFontDatabase.applicationFontFamilies(0)[0]

        self.message_label.setFont(QFont(self.cg_font_family, 16, QFont.Weight.DemiBold))
        self.proceed_button.setFont(QFont(self.cg_font_family, 14, QFont.Weight.Medium))
