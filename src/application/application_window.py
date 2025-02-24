from PyQt6.QtWidgets import QMainWindow, QPushButton, QHeaderView
from PyQt6.QtGui import QFont

from application.application_window_design import Ui_MainWindow as ApplicationWindowDesign
from application.open_dialogs import OpenDialogs
from application.search_and_sort_header import SearchAndSortHeader
from application.reset_item_delegates import ResetItemDelegates
from application.entity_page_signals import EntityPageSignals

from utils.get_information_codes import GetInformationCodes
from utils.custom_sort_filter_proxy_model import CustomSortFilterProxyModel
from utils.save_all_changes import SaveAllChanges
from utils.combobox_item_delegate import ComboboxItemDelegate
from utils.specific_buttons_enabler import SpecificButtonsEnabler
from utils.load_information_from_database import LoadInformationFromDatabase
from utils.custom_table_model import CustomTableModel

from helper_dialogs.save_item_state.confirm_save import ConfirmSaveDialog
from helper_dialogs.save_item_state.success_save_changes import SuccessSaveChangesDialog


class ApplicationWindow(QMainWindow, ApplicationWindowDesign):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.set_external_stylesheet()

        # Load information from database upon entering the landing page for the first time
        self.students_data = LoadInformationFromDatabase.get_students()
        self.programs_data = LoadInformationFromDatabase.get_programs()
        self.colleges_data = LoadInformationFromDatabase.get_colleges()

        # Generate table models in landing page so that it can be accessed in different pages
        self.students_table_model = CustomTableModel(self.students_data, "student")

        self.programs_table_model = CustomTableModel(self.programs_data, "program")
        self.programs_table_model.set_students_data(self.students_table_model.get_data())

        self.colleges_table_model = CustomTableModel(self.colleges_data, "college")
        self.colleges_table_model.set_students_data(self.students_table_model.get_data())
        self.colleges_table_model.set_programs_data(self.programs_table_model.get_data())

        self.students_sort_filter_proxy_model = CustomSortFilterProxyModel(self.students_table_model)
        self.programs_sort_filter_proxy_model = CustomSortFilterProxyModel(self.programs_table_model)
        self.colleges_sort_filter_proxy_model = CustomSortFilterProxyModel(self.colleges_table_model)

        self.open_dialogs = OpenDialogs()

        # Declared in setup_table_views
        self.reset_item_delegates = None
        self.entity_page_signals = None

        self.back_to_main_button.clicked.connect(self.change_to_landing_page)
        self.about_this_app_back_to_main_button.clicked.connect(self.change_to_landing_page)

        self.setup_table_views()

        self.students_button.clicked.connect(self.change_to_entity_page_student)
        self.programs_button.clicked.connect(self.change_to_entity_page_program)
        self.colleges_button.clicked.connect(self.change_to_entity_page_college)
        self.about_this_app_button.clicked.connect(self.change_to_about_this_app_page)

    def set_external_stylesheet(self):
        with open("../assets/qss_files/landing_page_style.qss", "r") as file:
            self.landing_page.setStyleSheet(file.read())

        with open("../assets/qss_files/entity_page_style.qss", "r") as file:
            self.entity_page.setStyleSheet(file.read())

        with open("../assets/qss_files/about_this_app_page_style.qss", "r") as file:
            self.about_this_app_page.setStyleSheet(file.read())

    def change_to_landing_page(self):
        self.stackedWidget.setCurrentWidget(self.landing_page)
        self.setWindowTitle("Sequence")

    def setup_table_views(self):
        # Students table view
        # self.students_table_view.setSortingEnabled(True)
        self.students_table_view.setModel(self.students_sort_filter_proxy_model)
        self.students_table_view.setAlternatingRowColors(True)
        self.students_table_horizontal_header = self.students_table_view.horizontalHeader()

        # self.students_table_reset_sorting_state = ResetSortingState(self.students_sort_filter_proxy_model,
        #                                                             self.students_table_view, "student")

        self.students_table_horizontal_header.resizeSection(0, 75)
        self.students_table_horizontal_header.resizeSection(3, 75)
        self.students_table_horizontal_header.resizeSection(4, 150)

        self.students_table_horizontal_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.students_table_horizontal_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.students_table_horizontal_header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.students_table_horizontal_header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.students_table_horizontal_header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.students_table_horizontal_header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)

        # Programs table view
        # self.programs_table_view.setSortingEnabled(True)
        self.programs_table_view.setModel(self.programs_sort_filter_proxy_model)
        self.programs_table_view.setAlternatingRowColors(True)
        self.programs_table_horizontal_header = self.programs_table_view.horizontalHeader()

        # self.programs_table_reset_sorting_state = ResetSortingState(self.programs_sort_filter_proxy_model,
        #                                                             self.programs_table_view, "program")

        self.programs_table_horizontal_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.programs_table_horizontal_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.programs_table_horizontal_header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)

        # Colleges table view
        # self.colleges_table_view.setSortingEnabled(True)
        self.colleges_table_view.setModel(self.colleges_sort_filter_proxy_model)
        self.colleges_table_view.setAlternatingRowColors(True)
        self.colleges_table_horizontal_header = self.colleges_table_view.horizontalHeader()

        # self.colleges_table_reset_sorting_state = ResetSortingState(self.colleges_sort_filter_proxy_model,
        #                                                             self.colleges_table_view, "college")

        self.colleges_table_horizontal_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.colleges_table_horizontal_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

        self.reset_item_delegates = ResetItemDelegates(self.for_reset_item_delegates())

        self.entity_page_signals = EntityPageSignals(self.for_entity_page_signals())

    def change_to_entity_page_student(self):
        self.stackedWidget.setCurrentWidget(self.entity_page)
        self.entity_type_label.setText("Student")

        self.add_entity_button.setText("Add student")
        self.delete_entity_button.setText("Delete student")
        self.edit_entity_button.setText("Edit student")

        self.table_view_widgets.setCurrentWidget(self.students_table_view_widget)

        SpecificButtonsEnabler.enable_delete_and_edit_buttons([self.delete_entity_button,
                                                               self.edit_entity_button,
                                                               self.view_demographics_button],
                                                              self.students_table_model)

        SpecificButtonsEnabler.enable_save_button(self.save_changes_button,
                                                  self.students_table_model,
                                                  self.programs_table_model,
                                                  self.colleges_table_model)

        SearchAndSortHeader.change_contents("student", self.search_type_combobox)
        SearchAndSortHeader.change_contents("student", self.sort_type_combobox)

        self.entity_page_signals.add("student")

        self.reset_item_delegates.reset("student")

        self.setWindowTitle("Sequence | Student")

    def change_to_entity_page_program(self):
        self.stackedWidget.setCurrentWidget(self.entity_page)
        self.entity_type_label.setText("Program")

        self.add_entity_button.setText("Add program")
        self.delete_entity_button.setText("Delete program")
        self.edit_entity_button.setText("Edit program")

        self.table_view_widgets.setCurrentWidget(self.programs_table_view_widget)

        SpecificButtonsEnabler.enable_delete_and_edit_buttons([self.delete_entity_button,
                                                               self.edit_entity_button,
                                                               self.view_demographics_button],
                                                              self.programs_table_model)

        SpecificButtonsEnabler.enable_save_button(self.save_changes_button,
                                                  self.students_table_model,
                                                  self.programs_table_model,
                                                  self.colleges_table_model)

        SearchAndSortHeader.change_contents("program", self.search_type_combobox)
        SearchAndSortHeader.change_contents("program", self.sort_type_combobox)

        self.entity_page_signals.add("program")

        self.reset_item_delegates.reset("program")

        self.setWindowTitle("Sequence | Program")

    def change_to_entity_page_college(self):
        self.stackedWidget.setCurrentWidget(self.entity_page)
        self.entity_type_label.setText("College")

        self.add_entity_button.setText("Add college")
        self.delete_entity_button.setText("Delete college")
        self.edit_entity_button.setText("Edit college")

        self.table_view_widgets.setCurrentWidget(self.colleges_table_view_widget)

        SpecificButtonsEnabler.enable_delete_and_edit_buttons([self.delete_entity_button,
                                                               self.edit_entity_button,
                                                               self.view_demographics_button],
                                                              self.colleges_table_model)

        SpecificButtonsEnabler.enable_save_button(self.save_changes_button,
                                                  self.students_table_model,
                                                  self.programs_table_model,
                                                  self.colleges_table_model)

        SearchAndSortHeader.change_contents("college", self.search_type_combobox)
        SearchAndSortHeader.change_contents("college", self.sort_type_combobox)

        self.entity_page_signals.add("college")

        self.setWindowTitle("Sequence | College")

    def change_to_about_this_app_page(self):
        self.stackedWidget.setCurrentWidget(self.about_this_app_page)
        self.setWindowTitle("Sequence | About this app")

    def for_reset_item_delegates(self):
        return [self.students_table_view,
                self.programs_table_view,
                self.colleges_table_view,
                self.students_table_model,
                self.programs_table_model,
                self.students_sort_filter_proxy_model,
                self.programs_sort_filter_proxy_model,
                self.colleges_sort_filter_proxy_model,
                self.colleges_table_model]

    def for_entity_page_signals(self):
        return [self.students_table_view,
                self.programs_table_view,
                self.colleges_table_view,
                self.students_table_model,
                self.programs_table_model,
                self.colleges_table_model,
                self.students_sort_filter_proxy_model,
                self.programs_sort_filter_proxy_model,
                self.colleges_sort_filter_proxy_model,
                self.add_entity_button,
                self.delete_entity_button,
                self.edit_entity_button,
                self.save_changes_button,
                self.view_demographics_button,
                self.sort_type_combobox,
                self.sort_order_combobox,
                self.search_input_lineedit,
                self.search_type_combobox,
                self.students_table_horizontal_header,
                self.programs_table_horizontal_header,
                self.colleges_table_horizontal_header,
                self.reset_item_delegates
                ]

    def closeEvent(self, event):

        entity_type = ""

        if self.colleges_table_model.get_has_changes():
            entity_type = "college"

        elif self.programs_table_model.get_has_changes():
            entity_type = "program"

        elif self.students_table_model.get_has_changes():
            entity_type = "student"

        if entity_type != "":
            OpenDialogs.open_confirm_save_dialog(self.students_table_model,
                                                 self.programs_table_model,
                                                 self.colleges_table_model)

        event.accept()

    def resizeEvent(self, event):
        font = QFont()
        font.setFamily("Segoe UI Semibold")

        # 48 is an arbitrary number obtained from 534/11, 534 is the minimum width, 11 is the minimum font size
        font.setPointSize(int(self.height() / 48))

        font.setBold(True)
        font.setWeight(75)

        self.back_to_main_button.setFont(font)
        self.about_this_app_back_to_main_button.setFont(font)
        self.add_entity_button.setFont(font)
        self.delete_entity_button.setFont(font)
        self.edit_entity_button.setFont(font)
        self.save_changes_button.setFont(font)
        self.view_demographics_button.setFont(font)
