from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QFont, QFontDatabase
from PyQt6.QtCore import QSize

from ui_py.confirm_delete_design import Ui_Dialog as ConfirmDeleteUI


class ConfirmDeleteDialog(QDialog, ConfirmDeleteUI):
    def __init__(self, entity_type, entities_to_delete):
        super().__init__()

        self.setupUi(self)

        self.set_external_stylesheet()
        self.load_fonts()

        self.confirm_delete_decision = False

        self.entity_type = entity_type
        self.entities_to_delete = entities_to_delete

        self.add_signals()

        self.edit_label_texts()

    def edit_label_texts(self):

        if len(self.entities_to_delete) == 1:
            self.setWindowTitle(f"Proceed in deleting {self.entities_to_delete[0]}?")
            self.header_label.setText(f"Are you sure you want to remove this {self.entity_type}?")

            self.setMinimumSize(QSize(495, 105))
            self.setMaximumSize(QSize(495, 105))
            self.resize(495, 105)
        else:
            self.setWindowTitle(f"Proceed in deleting {len(self.entities_to_delete)} {self.entity_type}s?")
            self.header_label.setText(f"Are you sure you want to remove these {self.entity_type}s?")

            self.setMinimumSize(QSize(515, 105))
            self.setMaximumSize(QSize(515, 105))
            self.resize(515, 105)


    def proceed_delete(self):
        self.confirm_delete_decision = True
        self.close_dialog()

    def close_dialog(self):
        self.close()

    def get_confirm_delete_decision(self):
        return self.confirm_delete_decision

    def add_signals(self):
        self.yes_button.clicked.connect(self.proceed_delete)
        self.no_button.clicked.connect(self.close_dialog)

    def set_external_stylesheet(self):
        with open("../assets/qss_files/dialog_style.qss", "r") as file:
            self.setStyleSheet(file.read())

    def load_fonts(self):
        self.cg_font_family = QFontDatabase.applicationFontFamilies(0)[0]

        self.header_label.setFont(QFont(self.cg_font_family, 16, QFont.Weight.DemiBold))

        self.no_button.setFont(QFont(self.cg_font_family, 14, QFont.Weight.Medium))
        self.yes_button.setFont(QFont(self.cg_font_family, 14, QFont.Weight.Medium))