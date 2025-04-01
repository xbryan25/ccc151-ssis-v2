from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QFont, QFontDatabase

from helper_dialogs.edit_item_state.confirm_edit_design import Ui_Dialog as ConfirmEditUI


class ConfirmEditDialog(QDialog, ConfirmEditUI):
    def __init__(self, entity_type, entities_to_edit, num_of_affected=0, entity_code_affected=False):
        super().__init__()

        self.setupUi(self)

        self.set_external_stylesheet()
        self.load_fonts()

        self.confirm_edit_decision = False

        self.entity_type = entity_type
        self.entities_to_edit = entities_to_edit
        self.num_of_affected = num_of_affected
        self.entity_code_affected = entity_code_affected

        self.add_signals()

        self.edit_label_texts()

    def edit_label_texts(self):
        if len(self.entities_to_edit) == 1:
            self.setWindowTitle(f"Proceed in editing {self.entities_to_edit[0]}?")
            self.header_label.setText(f"Are you sure you want to edit this {self.entity_type}?")
        else:
            self.setWindowTitle(f"Proceed in editing {len(self.entities_to_edit)} {self.entity_type}s?")
            self.header_label.setText(f"Are you sure you want to edit these {self.entity_type}s?")

        if self.entity_code_affected:
            if self.entity_type == "program":
                if self.num_of_affected == 1:
                    self.affected_num_label.setText(f"{self.num_of_affected} student "
                                                    f"under this program will be affected")
                else:
                    self.affected_num_label.setText(f"{self.num_of_affected} students "
                                                    f"under this program will be affected")
            elif self.entity_type == "college":
                if self.num_of_affected == 1:
                    self.affected_num_label.setText(f"{self.num_of_affected} program "
                                                    f"under this college will be affected")
                else:
                    self.affected_num_label.setText(f"{self.num_of_affected} programs "
                                                    f"under this college will be affected")
        else:
            self.affected_num_label.close()
            self.verticalLayout.removeItem(self.spacerItem2)
            self.resize(495, 105)

    def proceed_edit(self):
        self.confirm_edit_decision = True
        self.close_dialog()

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
        self.affected_num_label.setFont(QFont(self.cg_font_family, 12, QFont.Weight.Medium))

        self.no_button.setFont(QFont(self.cg_font_family, 14, QFont.Weight.Medium))
        self.yes_button.setFont(QFont(self.cg_font_family, 14, QFont.Weight.Medium))
