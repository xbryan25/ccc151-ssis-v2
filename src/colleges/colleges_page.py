from PyQt6.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt, QRegularExpression
import csv

from colleges.colleges_page_design import Ui_MainWindow as CollegesPageUI
from colleges.add_college import AddCollegeDialog
from colleges.edit_college import EditCollegeDialog
from colleges.delete_college import DeleteCollegeDialog

from utils.reset_sorting_state import ResetSortingState
from utils.custom_sort_filter_proxy_model import CustomSortFilterProxyModel
from utils.save_all_changes import SaveAllChanges
from utils.reset_sorting_state import ResetSortingState
from utils.enable_edit_and_delete_buttons import EnableEditAndDeleteButtons

from helper_dialogs.save_item_state.confirm_save import ConfirmSaveDialog
from helper_dialogs.save_item_state.success_save_changes import SuccessSaveChangesDialog


class CollegesPage(QMainWindow, CollegesPageUI):
    def __init__(self, main_screen, students_table_model, programs_table_model, colleges_table_model):
        super().__init__()

        self.setupUi(self)

        self.set_external_stylesheet()

        self.main_screen = main_screen

        self.students_table_model = students_table_model
        self.programs_table_model = programs_table_model
        self.colleges_table_model = colleges_table_model

        self.sort_filter_proxy_model = CustomSortFilterProxyModel(self.colleges_table_model)

        self.colleges_table_view.setSortingEnabled(True)
        self.colleges_table_view.setModel(self.sort_filter_proxy_model)

        self.colleges_table_view.setAlternatingRowColors(True)

        self.horizontal_header = self.colleges_table_view.horizontalHeader()

        self.reset_sorting_state = ResetSortingState(self.colleges_table_model,
                                                     self.colleges_table_view)

        self.add_signals()

        EnableEditAndDeleteButtons.enable_button(self.delete_college_button, self.colleges_table_model)
        EnableEditAndDeleteButtons.enable_button(self.edit_college_button, self.colleges_table_model)

    def open_add_college_dialog(self):

        self.add_college_dialog = AddCollegeDialog(self.colleges_table_view, self.colleges_table_model)
        self.add_college_dialog.exec()

        EnableEditAndDeleteButtons.enable_button(self.delete_college_button, self.colleges_table_model)
        EnableEditAndDeleteButtons.enable_button(self.edit_college_button, self.colleges_table_model)

    def open_edit_college_dialog(self):
        self.edit_college_dialog = EditCollegeDialog(self.colleges_table_view, self.colleges_table_model,
                                                     self.programs_table_model)
        self.edit_college_dialog.exec()

    def open_delete_college_dialog(self):
        self.delete_college_dialog = DeleteCollegeDialog(self.colleges_table_view, self.colleges_table_model,
                                                         self.students_table_model, self.programs_table_model,
                                                         self.reset_item_delegates, self.horizontal_header)

        self.delete_college_dialog.exec()

        EnableEditAndDeleteButtons.enable_button(self.delete_college_button, self.colleges_table_model)
        EnableEditAndDeleteButtons.enable_button(self.edit_college_button, self.colleges_table_model)

    def open_confirm_save_dialog(self, save_type):
        self.confirm_save_dialog = ConfirmSaveDialog()
        self.confirm_save_dialog.exec()

        if self.confirm_save_dialog.get_confirm_edit_decision():
            self.save_all_changes = SaveAllChanges(save_type,
                                                   self.students_table_model.get_data(),
                                                   self.programs_table_model.get_data(),
                                                   self.colleges_table_model.get_data())

            self.save_all_changes.to_csv()

            self.success_save_changes = SuccessSaveChangesDialog()
            self.success_save_changes.exec()

    def return_to_main_screen(self):
        self.main_screen.show()

        self.setVisible(False)

    def search_program_using_lineedit(self):
        search_type = self.search_type_combobox.currentIndex()

        self.colleges_table_model.layoutAboutToBeChanged.emit()

        self.sort_filter_proxy_model.setFilterKeyColumn(search_type)

        self.sort_filter_proxy_model.setFilterRegularExpression(
            QRegularExpression('^' + self.search_input_lineedit.text(),
                               QRegularExpression.PatternOption.CaseInsensitiveOption))

        self.colleges_table_model.layoutChanged.emit()

    def change_search_lineedit_placeholder(self):
        self.search_input_lineedit.setPlaceholderText(f"Input {self.search_type_combobox.currentText()}")

    def add_signals(self):
        self.add_college_button.clicked.connect(self.open_add_college_dialog)
        self.edit_college_button.clicked.connect(self.open_edit_college_dialog)
        self.delete_college_button.clicked.connect(self.open_delete_college_dialog)
        self.save_changes_button.clicked.connect(lambda: self.open_confirm_save_dialog("college"))
        self.back_to_main_button.clicked.connect(self.return_to_main_screen)

        self.colleges_table_view.horizontalHeader().sectionClicked.connect(
            self.reset_sorting_state.reset_sorting_state)

        self.search_input_lineedit.textChanged.connect(self.search_program_using_lineedit)
        self.search_type_combobox.currentIndexChanged.connect(self.change_search_lineedit_placeholder)

    def closeEvent(self, event):
        if self.colleges_table_model.get_has_changes():
            self.open_confirm_save_dialog("college")

        elif self.programs_table_model.get_has_changes():
            self.open_confirm_save_dialog("program")

        elif self.students_table_model.get_has_changes():
            self.open_confirm_save_dialog("student")

        print(event)

        event.accept()


    def reset_item_delegates(self):
        self.sort_filter_proxy_model.beginResetModel()
        self.sort_filter_proxy_model.endResetModel()

    def set_external_stylesheet(self):
        with open("../assets/qss_files/entity_page_style.qss", "r") as file:
            self.setStyleSheet(file.read())