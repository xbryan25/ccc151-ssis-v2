from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QFont, QFontDatabase

from helper_dialogs.delete_item_state.confirm_delete_design import Ui_Dialog as ConfirmDeleteUI


class ConfirmDeleteDialog(QDialog, ConfirmDeleteUI):
    def __init__(self, information_type, information_to_delete):
        super().__init__()

        self.setupUi(self)

        self.set_external_stylesheet()
        self.load_fonts()

        self.confirm_delete_decision = False

        self.information_type = information_type
        self.information_to_delete = information_to_delete

        self.add_signals()

        self.edit_label_texts()

    def edit_label_texts(self):
        self.setWindowTitle(f"Proceed in deleting {self.information_to_delete}?")
        self.header_label.setText(f"Are you sure you want to remove this {self.information_type}?")

        self.affected_num_label.close()
        self.verticalLayout.removeItem(self.spacerItem2)
        self.setMinimumHeight(105)
        self.resize(495, 105)

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
        self.affected_num_label.setFont(QFont(self.cg_font_family, 12, QFont.Weight.Medium))

        self.no_button.setFont(QFont(self.cg_font_family, 14, QFont.Weight.Medium))
        self.yes_button.setFont(QFont(self.cg_font_family, 14, QFont.Weight.Medium))