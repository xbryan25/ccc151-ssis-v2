from PyQt6.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt, QSortFilterProxyModel, QAbstractTableModel, QRegularExpression
import csv

from programs.programs_page_design import Ui_MainWindow as ProgramsPageUI

from utils.reset_sorting_state import ResetSortingState
from utils.get_information_codes import GetInformationCodes
from utils.custom_sort_filter_proxy_model import CustomSortFilterProxyModel
from utils.save_all_changes import SaveAllChanges
from utils.combobox_item_delegate import ComboboxItemDelegate
from utils.enable_edit_and_delete_buttons import EnableEditAndDeleteButtons

from programs.add_program import AddProgramDialog
from programs.edit_program import EditProgramDialog
from programs.delete_program import DeleteProgramDialog

from helper_dialogs.input_prerequisite.input_prerequisite import InputPrerequisiteDialog
from helper_dialogs.save_item_state.confirm_save import ConfirmSaveDialog
from helper_dialogs.save_item_state.success_save_changes import SuccessSaveChangesDialog


class ProgramsPage(QMainWindow, ProgramsPageUI):
    def __init__(self, main_screen, students_table_model, programs_table_model, colleges_table_model):
        super().__init__()

        self.setupUi(self)

        self.set_external_stylesheet()

        self.main_screen = main_screen

        self.colleges_table_model = colleges_table_model

        self.students_table_model = students_table_model
        self.programs_table_model = programs_table_model

        self.sort_filter_proxy_model = CustomSortFilterProxyModel(self.programs_table_model)

        self.programs_table_view.setSortingEnabled(True)
        self.programs_table_view.setModel(self.sort_filter_proxy_model)

        self.programs_table_view.setAlternatingRowColors(True)

        self.horizontal_header = self.programs_table_view.horizontalHeader()

        self.reset_sorting_state = ResetSortingState(self.programs_table_model,
                                                     self.programs_table_view)

        self.add_signals()

        EnableEditAndDeleteButtons.enable_button(self.delete_program_button, self.programs_table_model)
        EnableEditAndDeleteButtons.enable_button(self.edit_program_button, self.programs_table_model)

    def open_add_program_dialog(self):

        if self.colleges_table_model.get_data()[0][0] != "":
            # Note: self.reset_item_delegates is a function

            self.add_program_dialog = AddProgramDialog(self.programs_table_view, self.programs_table_model,
                                                       self.colleges_table_model, self.reset_item_delegates)
            self.add_program_dialog.exec()

            EnableEditAndDeleteButtons.enable_button(self.delete_program_button, self.programs_table_model)
            EnableEditAndDeleteButtons.enable_button(self.edit_program_button, self.programs_table_model)

        else:
            self.input_college_dialog = InputPrerequisiteDialog("college")
            self.input_college_dialog.exec()


    def open_edit_program_dialog(self):
        self.edit_program_dialog = EditProgramDialog(self.programs_table_view,
                                                     self.programs_table_model,
                                                     self.students_table_model,
                                                     self.colleges_table_model)
        self.edit_program_dialog.exec()

    def open_delete_program_dialog(self):
        self.delete_program_dialog = DeleteProgramDialog(self.programs_table_view,
                                                         self.programs_table_model,
                                                         self.students_table_model,
                                                         self.colleges_table_model,
                                                         self.reset_item_delegates,
                                                         self.horizontal_header)
        self.delete_program_dialog.exec()

        EnableEditAndDeleteButtons.enable_button(self.delete_program_button, self.programs_table_model)
        EnableEditAndDeleteButtons.enable_button(self.edit_program_button, self.programs_table_model)


    def open_confirm_save_dialog(self, save_type):
        self.confirm_save_dialog = ConfirmSaveDialog()
        self.confirm_save_dialog.exec()

        if self.confirm_save_dialog.get_confirm_edit_decision():
            self.save_all_changes = SaveAllChanges(save_type,
                                                   self.students_table_model.get_data(),
                                                   self.programs_table_model.get_data())

            self.save_all_changes.to_csv()

            self.success_save_changes = SuccessSaveChangesDialog()
            self.success_save_changes.exec()

    def return_to_main_screen(self):
        self.main_screen.show()

        self.setVisible(False)

    def search_program_using_lineedit(self):
        search_type = self.search_type_combobox.currentIndex()

        self.programs_table_model.layoutAboutToBeChanged.emit()

        self.sort_filter_proxy_model.setFilterKeyColumn(search_type)

        self.sort_filter_proxy_model.setFilterRegularExpression(
            QRegularExpression('^' + self.search_input_lineedit.text(),
                               QRegularExpression.PatternOption.CaseInsensitiveOption))

        self.programs_table_model.layoutChanged.emit()

    def change_search_lineedit_placeholder(self):
        self.search_input_lineedit.setPlaceholderText(f"Input {self.search_type_combobox.currentText()}")

    def add_signals(self):
        self.add_program_button.clicked.connect(self.open_add_program_dialog)
        self.edit_program_button.clicked.connect(self.open_edit_program_dialog)
        self.delete_program_button.clicked.connect(self.open_delete_program_dialog)
        self.save_changes_button.clicked.connect(lambda: self.open_confirm_save_dialog("program"))
        self.back_to_main_button.clicked.connect(self.return_to_main_screen)

        self.programs_table_view.horizontalHeader().sectionClicked.connect(
            self.reset_sorting_state.reset_sorting_state)

        self.search_input_lineedit.textChanged.connect(self.search_program_using_lineedit)
        self.search_type_combobox.currentIndexChanged.connect(self.change_search_lineedit_placeholder)

    def get_college_codes(self):
        return GetInformationCodes.for_colleges(self.colleges_table_model.get_data())

    def closeEvent(self, event):

        if self.programs_table_model.get_has_changes():
            self.open_confirm_save_dialog("program")

        elif self.students_table_model.get_has_changes():
            self.open_confirm_save_dialog("student")

        event.accept()

    def load_item_delegates_college_codes(self):

        # Check if self.programs_table_model is empty, if so, disable combobox item delegate

        if self.programs_table_model.get_data()[0][2] != "":
            # For College Codes

            combobox_item_delegate = ComboboxItemDelegate(self, self.get_college_codes())
            # combobox_item_delegate.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

            self.programs_table_view.setItemDelegateForColumn(2, combobox_item_delegate)

            for row in range(0, self.sort_filter_proxy_model.rowCount()):
                self.programs_table_view.openPersistentEditor(self.sort_filter_proxy_model.index(row, 2))

    # Dynamic change of combobox
    # https://www.pythonguis.com/faq/how-to-clear-remove-combobox-delegate-data-from-qtableview/

    def reset_item_delegates(self):
        self.sort_filter_proxy_model.beginResetModel()
        self.sort_filter_proxy_model.endResetModel()

        self.load_item_delegates_college_codes()

    def set_external_stylesheet(self):
        with open("../assets/qss_files/entity_page_style.qss", "r") as file:
            self.setStyleSheet(file.read())
