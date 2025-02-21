from PyQt6.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QHeaderView, QComboBox, QPushButton, \
     QLineEdit, QLabel, QFrame

from PyQt6.QtCore import Qt, QSortFilterProxyModel, QAbstractTableModel, QRegularExpression
from PyQt6.QtGui import QCursor, QFont

from utils.reset_sorting_state import ResetSortingState
from utils.custom_sort_filter_proxy_model import CustomSortFilterProxyModel
from utils.save_all_changes import SaveAllChanges
from utils.reset_sorting_state import ResetSortingState
from utils.specific_buttons_enabler import SpecificButtonsEnabler

from colleges.colleges_page_design import Ui_MainWindow as CollegesPageUI
from colleges.add_college import AddCollegeDialog
from colleges.edit_college import EditCollegeDialog
from colleges.delete_college import DeleteCollegeDialog

from helper_dialogs.save_item_state.confirm_save import ConfirmSaveDialog
from helper_dialogs.save_item_state.success_save_changes import SuccessSaveChangesDialog

import csv


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

        self.reset_sorting_state = ResetSortingState(self.sort_filter_proxy_model,
                                                     self.colleges_table_view,
                                                     "college")

        self.page_controls = self.get_page_controls()

        self.add_signals()

        SpecificButtonsEnabler.enable_delete_and_edit_buttons([self.page_controls["delete_college_button"],
                                                               self.page_controls["edit_college_button"]],
                                                              self.programs_table_model)

        SpecificButtonsEnabler.enable_save_button(self.page_controls["save_changes_button"], self.colleges_table_model)

    def open_add_college_dialog(self):

        self.add_college_dialog = AddCollegeDialog(self.colleges_table_view, self.colleges_table_model)
        self.add_college_dialog.exec()

        SpecificButtonsEnabler.enable_delete_and_edit_buttons([self.page_controls["delete_college_button"],
                                                               self.page_controls["edit_college_button"]],
                                                              self.programs_table_model)

        SpecificButtonsEnabler.enable_save_button(self.page_controls["save_changes_button"], self.colleges_table_model)

    def open_edit_college_dialog(self):
        self.edit_college_dialog = EditCollegeDialog(self.colleges_table_view, self.colleges_table_model,
                                                     self.programs_table_model)
        self.edit_college_dialog.exec()

        SpecificButtonsEnabler.enable_save_button(self.page_controls["save_changes_button"], self.colleges_table_model)

    def open_delete_college_dialog(self):
        self.delete_college_dialog = DeleteCollegeDialog(self.colleges_table_view, self.colleges_table_model,
                                                         self.students_table_model, self.programs_table_model,
                                                         self.reset_item_delegates, self.horizontal_header)

        self.delete_college_dialog.exec()

        SpecificButtonsEnabler.enable_delete_and_edit_buttons([self.page_controls["delete_college_button"],
                                                               self.page_controls["edit_college_button"]],
                                                              self.programs_table_model)

        SpecificButtonsEnabler.enable_save_button(self.page_controls["save_changes_button"], self.colleges_table_model)

    def open_confirm_save_dialog(self, save_type):
        self.confirm_save_dialog = ConfirmSaveDialog()
        self.confirm_save_dialog.exec()

        if self.confirm_save_dialog.get_confirm_edit_decision():

            self.save_all_changes = SaveAllChanges(save_type,
                                                   self.students_table_model,
                                                   self.programs_table_model,
                                                   self.colleges_table_model)

            self.save_all_changes.to_csv()

            SpecificButtonsEnabler.enable_save_button(self.page_controls["save_changes_button"], self.colleges_table_model)

            self.success_save_changes = SuccessSaveChangesDialog()
            self.success_save_changes.exec()

    def return_to_main_screen(self):
        self.main_screen.show()

        self.setVisible(False)

    def search_college_using_lineedit(self):
        search_type = self.page_controls["search_type_combobox"].currentIndex()

        self.colleges_table_model.layoutAboutToBeChanged.emit()

        self.sort_filter_proxy_model.setFilterKeyColumn(search_type)

        self.sort_filter_proxy_model.setFilterRegularExpression(
            QRegularExpression('^' + self.search_input_lineedit.text(),
                               QRegularExpression.PatternOption.CaseInsensitiveOption))

        self.colleges_table_model.layoutChanged.emit()

    def change_search_lineedit_placeholder(self):
        self.page_controls["search_input_lineedit"].setPlaceholderText(f"Input "
                                                                       f"{self.search_type_combobox.currentText()}")

    def add_signals(self):
        self.page_controls["add_college_button"].clicked.connect(self.open_add_college_dialog)
        self.page_controls["edit_college_button"].clicked.connect(self.open_edit_college_dialog)
        self.page_controls["delete_college_button"].clicked.connect(self.open_delete_college_dialog)
        self.page_controls["save_changes_button"].clicked.connect(lambda: self.open_confirm_save_dialog("college"))
        self.page_controls["back_to_main_button"].clicked.connect(self.return_to_main_screen)

        self.horizontal_header.sectionClicked.connect(self.reset_sorting_state.reset_sorting_state)

        self.horizontal_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.horizontal_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

        self.page_controls["search_input_lineedit"].textChanged.connect(self.search_college_using_lineedit)
        self.page_controls["search_type_combobox"].currentIndexChanged.connect(self.change_search_lineedit_placeholder)

    def reset_item_delegates(self):
        self.sort_filter_proxy_model.beginResetModel()
        self.sort_filter_proxy_model.endResetModel()

    def set_external_stylesheet(self):
        with open("../assets/qss_files/entity_page_style.qss", "r") as file:
            self.setStyleSheet(file.read())

    def get_page_controls(self):
        back_to_main_button = (self.back_and_search_frame.findChild(QFrame, "back_frame").
                               findChild(QPushButton, "back_to_main_button"))

        search_input_lineedit = (self.back_and_search_frame.findChild(QFrame, "search_frame").
                                 findChild(QLineEdit, "search_input_lineedit"))

        search_type_combobox = (self.back_and_search_frame.findChild(QFrame, "search_frame").
                                findChild(QComboBox, "search_type_combobox"))

        add_college_button = (self.buttons_frame.findChild(QPushButton, "add_college_button"))

        delete_college_button = (self.buttons_frame.findChild(QPushButton, "delete_college_button"))

        edit_college_button = (self.buttons_frame.findChild(QPushButton, "edit_college_button"))

        save_changes_button = (self.buttons_frame.findChild(QPushButton, "save_changes_button"))

        view_demographics_button = (self.buttons_frame.findChild(QPushButton, "view_demographics_button"))

        title_label = (self.header_frame.findChild(QLabel, "title_label"))

        type_label = (self.header_frame.findChild(QLabel, "type_label"))

        print("Yo")

        return {"back_to_main_button": back_to_main_button,
                "search_input_lineedit": search_input_lineedit,
                "search_type_combobox": search_type_combobox,
                "add_college_button": add_college_button,
                "delete_college_button": delete_college_button,
                "edit_college_button": edit_college_button,
                "save_changes_button": save_changes_button,
                "view_demographics_button": view_demographics_button,
                "title_label": title_label,
                "type_label": type_label}

    def closeEvent(self, event):
        if self.colleges_table_model.get_has_changes():
            self.open_confirm_save_dialog("college")

        elif self.programs_table_model.get_has_changes():
            self.open_confirm_save_dialog("program")

        elif self.students_table_model.get_has_changes():
            self.open_confirm_save_dialog("student")

        print(event)

        event.accept()

    def resizeEvent(self, event):
        print(self.size())

        # TODO: Increase/decrease font of buttons when it is getting resized
        font = QFont()
        font.setFamily("Segoe UI Semibold")

        # 48 is an arbitrary number obtained from 534/11, 534 is the minimum width, 11 is the minimum font size
        font.setPointSize(int(self.height() / 48))

        font.setBold(True)
        font.setWeight(75)

        self.page_controls["back_to_main_button"].setFont(font)
        self.page_controls["add_college_button"].setFont(font)
        self.page_controls["delete_college_button"].setFont(font)
        self.page_controls["edit_college_button"].setFont(font)
        self.page_controls["save_changes_button"].setFont(font)
        self.page_controls["view_demographics_button"].setFont(font)