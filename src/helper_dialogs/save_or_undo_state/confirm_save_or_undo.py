from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QFont, QFontDatabase

from helper_dialogs.save_or_undo_state.confirm_save_or_undo_design import Ui_Dialog as ConfirmSaveUI


class ConfirmSaveOrUndoDialog(QDialog, ConfirmSaveUI):
    def __init__(self, save_or_undo):
        super().__init__()

        self.setupUi(self)

        self.set_external_stylesheet()
        self.load_fonts()

        self.save_or_undo = save_or_undo

        self.confirm_edit_decision = False

        self.set_text()

        self.add_signals()

    def proceed_edit(self):
        self.confirm_edit_decision = True
        self.close_dialog()

    def set_text(self):
        if self.save_or_undo == "save":
            self.setWindowTitle("Proceed in saving recent changes made?")
            self.header_label.setText("Save all recent changes?")
        else:
            self.setWindowTitle("Proceed in undoing all recent changes made?")
            self.header_label.setText("Undo all recent changes?")

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

    def load_fonts(self):
        self.cg_font_family = QFontDatabase.applicationFontFamilies(0)[0]

        self.header_label.setFont(QFont(self.cg_font_family, 16, QFont.Weight.DemiBold))

        self.no_button.setFont(QFont(self.cg_font_family, 14, QFont.Weight.Medium))
        self.yes_button.setFont(QFont(self.cg_font_family, 14, QFont.Weight.Medium))
