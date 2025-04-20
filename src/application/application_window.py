from PyQt6.QtWidgets import QMainWindow, QHeaderView, QTableView, QMenu
from PyQt6.QtGui import QFont, QFontDatabase, QPixmap, QIcon, QGuiApplication
from PyQt6.QtCore import Qt, QEvent, QModelIndex

from ui_py.application_window_design import Ui_MainWindow as ApplicationWindowDesign

from application.open_dialogs import OpenDialogs
from application.search_and_sort_header import SearchAndSortHeader
from application.reset_item_delegates import ResetItemDelegates
from application.load_application_window_fonts import LoadApplicationWindowFonts

from application.page_controls.entity_page_controls import EntityPageControls
from application.page_controls.view_demographics_page_controls import ViewDemographicsPageControls
from application.page_controls.table_view_page_controls import TableViewPageControls

from utils.custom_sort_filter_proxy_model import CustomSortFilterProxyModel
from utils.custom_table_model import CustomTableModel
from utils.specific_buttons_enabler import SpecificButtonsEnabler

from database_handler.database_handler import DatabaseHandler


class ApplicationWindow(QMainWindow, ApplicationWindowDesign):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.set_external_stylesheet()
        self.load_fonts()

        self.mode = "viewer"

        self.database_handler = DatabaseHandler()

        # Generate table models in landing page so that it can be accessed in different pages
        self.students_table_model = CustomTableModel("student", self.database_handler)
        self.programs_table_model = CustomTableModel("program", self.database_handler)
        self.colleges_table_model = CustomTableModel("college", self.database_handler)

        self.students_table_model.set_search_and_sort_fields(self.sort_order_combobox, self.search_input_lineedit)
        self.programs_table_model.set_search_and_sort_fields(self.sort_order_combobox, self.search_input_lineedit)
        self.colleges_table_model.set_search_and_sort_fields(self.sort_order_combobox, self.search_input_lineedit)

        self.students_sort_filter_proxy_model = CustomSortFilterProxyModel(self.students_table_model)
        self.programs_sort_filter_proxy_model = CustomSortFilterProxyModel(self.programs_table_model)
        self.colleges_sort_filter_proxy_model = CustomSortFilterProxyModel(self.colleges_table_model)

        # Declared in setup_table_views
        self.reset_item_delegates = None
        self.entity_page_controls = None

        self.add_signals()

        self.setup_table_views()

        self.reset_item_delegates = ResetItemDelegates(self)
        self.entity_page_controls = EntityPageControls(self)

        self.setWindowIcon(QIcon("../assets/images/sequence_icon.ico"))

    def set_external_stylesheet(self):
        with open("../assets/qss_files/landing_page_style.qss", "r") as file:
            self.landing_page.setStyleSheet(file.read())

        with open("../assets/qss_files/entity_page_style.qss", "r") as file:
            self.entity_page.setStyleSheet(file.read())

        with open("../assets/qss_files/about_this_app_page_style.qss", "r") as file:
            self.about_this_app_page.setStyleSheet(file.read())

        with open("../assets/qss_files/view_demographics_page_style.qss", "r") as file:
            self.demographics_page.setStyleSheet(file.read())

    def add_signals(self):
        # Back to landing page buttons
        self.back_to_main_button.clicked.connect(self.change_to_landing_page)
        self.about_this_app_back_to_main_button.clicked.connect(self.change_to_landing_page)
        self.demographics_back_to_main_button.clicked.connect(self.change_to_landing_page)

        # Go to entity pages

        self.students_button.clicked.connect(lambda: self.change_to_entity_page("student"))
        self.programs_button.clicked.connect(lambda: self.change_to_entity_page("program"))
        self.colleges_button.clicked.connect(lambda: self.change_to_entity_page("college"))

        # Go to view demographics page
        self.view_demographics_button.clicked.connect(self.change_to_demographics_page)

        # Go to about this app page
        self.about_this_app_button.clicked.connect(self.change_to_about_this_app_page)

        self.mode_button.clicked.connect(self.change_mode)

    def setup_table_views(self):
        # Students table view
        self.students_table_view.setModel(self.students_sort_filter_proxy_model)
        self.students_table_view.setAlternatingRowColors(True)

        # Programs table view
        self.programs_table_view.setModel(self.programs_sort_filter_proxy_model)
        self.programs_table_view.setAlternatingRowColors(True)

        self.programs_table_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

        # Colleges table view
        self.colleges_table_view.setModel(self.colleges_sort_filter_proxy_model)
        self.colleges_table_view.setAlternatingRowColors(True)

        self.colleges_table_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

        self.setup_table_views_column_widths()

    def setup_table_views_column_widths(self):
        self.students_table_horizontal_header = self.students_table_view.horizontalHeader()

        self.students_table_horizontal_header.resizeSection(0, 110)
        self.students_table_horizontal_header.resizeSection(3, 110)
        self.students_table_horizontal_header.resizeSection(4, 130)

        self.students_table_horizontal_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.students_table_horizontal_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.students_table_horizontal_header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.students_table_horizontal_header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.students_table_horizontal_header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.students_table_horizontal_header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)


        self.programs_table_horizontal_header = self.programs_table_view.horizontalHeader()

        self.programs_table_horizontal_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.programs_table_horizontal_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.programs_table_horizontal_header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)


        self.colleges_table_horizontal_header = self.colleges_table_view.horizontalHeader()

        self.colleges_table_horizontal_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.colleges_table_horizontal_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

    def change_to_landing_page(self):
        self.stackedWidget.setCurrentWidget(self.landing_page)
        self.setWindowTitle("Sequence")

    def change_to_entity_page(self, entity_type):
        self.stackedWidget.setCurrentWidget(self.entity_page)

        self.entity_page_controls.remove()

        current_model = None
        current_table_view = None

        if entity_type == "student":

            current_model = self.students_table_model
            current_table_view = self.students_table_view

            self.reset_item_delegates.load_item_delegates_for_students_table_view()
            self.entity_type_icon.setPixmap(QPixmap("../assets/images/student_icon.svg"))

            self.table_view_widgets.setCurrentWidget(self.students_table_view_widget)

        elif entity_type == "program":

            current_model = self.programs_table_model
            current_table_view = self.programs_table_view

            self.reset_item_delegates.load_item_delegates_for_programs_table_view()
            self.entity_type_icon.setPixmap(QPixmap("../assets/images/book_icon.svg"))

            self.table_view_widgets.setCurrentWidget(self.programs_table_view_widget)

        elif entity_type == "college":

            current_model = self.colleges_table_model
            current_table_view = self.colleges_table_view

            self.entity_type_icon.setPixmap(QPixmap("../assets/images/building_icon.svg"))

            self.table_view_widgets.setCurrentWidget(self.colleges_table_view_widget)

        if self.mode == "viewer":
            current_model.set_mode("viewer")
            current_table_view.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
            self.buttons_frame.hide()
        else:
            current_model.set_mode("admin")
            current_table_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            self.buttons_frame.show()

        self.setWindowTitle(f"Sequence | {entity_type.capitalize()}s")

        self.entity_type_label.setText(f"{entity_type.capitalize()}s")
        self.add_entity_button.setText(f" Add {entity_type}")

        self.entity_page_layout.activate()

        self.entity_type_icon.setScaledContents(True)

        self.current_page_lineedit.setText("1")

        self.previous_page_button.setEnabled(True)

        SearchAndSortHeader.change_contents(entity_type, self.search_type_combobox, "search")
        SearchAndSortHeader.change_contents(entity_type, self.sort_type_combobox, "sort")

        SpecificButtonsEnabler.enable_save_and_undo_buttons(self.save_changes_button,
                                                            self.undo_all_changes_button,
                                                            self.students_table_model,
                                                            self.programs_table_model,
                                                            self.colleges_table_model)

        self.search_type_combobox.setCurrentIndex(0)
        self.search_input_lineedit.clear()

        self.sort_type_combobox.setCurrentIndex(0)
        self.sort_order_combobox.setCurrentIndex(0)

        self.entity_page_controls.add(entity_type)

        self.reset_item_delegates.reset(entity_type)

        self.previous_page_button.setEnabled(False)
        self.first_page_button.setEnabled(False)

        current_model.layoutChanged.emit()

        current_model.set_max_row_per_page(
            TableViewPageControls.get_max_visible_rows(current_table_view))

        current_model.initialize_data()

        self.setup_table_views_column_widths()

        current_model.update_page_view(current_table_view)

        if current_model.max_pages == 1:
            self.next_page_button.setEnabled(False)
            self.last_page_button.setEnabled(False)
        else:
            self.next_page_button.setEnabled(True)
            self.last_page_button.setEnabled(True)

        self.max_pages_label.setText(f"/ {current_model.max_pages}")

        self.reset_tracked_attributes_of_models(entity_type)

    def change_to_demographics_page(self):
        self.stackedWidget.setCurrentWidget(self.demographics_page)

        self.view_demographics_page_controls = ViewDemographicsPageControls(self)

    def change_to_about_this_app_page(self):
        self.stackedWidget.setCurrentWidget(self.about_this_app_page)
        self.setWindowTitle("Sequence | About this app")

    def change_mode(self):
        if self.mode == "admin":
            self.mode = "viewer"

            self.mode_button.setText("Viewer")

        elif self.mode == "viewer":
            self.mode = "admin"

            self.mode_button.setText("Admin")

    def reset_tracked_attributes_of_models(self, entity_type):

        if entity_type == "student":
            self.students_table_model.set_is_data_currently_filtered(False)
            self.students_table_model.reset_all_prev_search_and_sort_conditions()

        elif entity_type == "program":
            self.programs_table_model.set_is_data_currently_filtered(False)
            self.programs_table_model.reset_all_prev_search_and_sort_conditions()

        elif entity_type == "student":
            self.colleges_table_model.set_is_data_currently_filtered(False)
            self.colleges_table_model.reset_all_prev_search_and_sort_conditions()

    def update_table_views(self):

        current_model = None
        current_table_view = None

        if (self.stackedWidget.currentWidget() == self.entity_page and
                self.table_view_widgets.currentWidget() == self.students_table_view_widget):

            current_model = self.students_table_model
            current_table_view = self.students_table_view

        elif (self.stackedWidget.currentWidget() == self.entity_page and
                self.table_view_widgets.currentWidget() == self.programs_table_view_widget):

            current_model = self.programs_table_model
            current_table_view = self.programs_table_view

        elif (self.stackedWidget.currentWidget() == self.entity_page and
                self.table_view_widgets.currentWidget() == self.colleges_table_view_widget):

            current_model = self.colleges_table_model
            current_table_view = self.colleges_table_view

        if current_model and current_table_view:

            current_table_view.clearSelection()
            current_table_view.setCurrentIndex(QModelIndex())

            current_model.update_page_view(current_table_view)

            # Get the number of max_pages before it is updated
            old_max_pages = int(self.max_pages_label.text().replace("/", "").strip())

            self.max_pages_label.setText(f"/ {current_model.max_pages}")

            if (int(self.current_page_lineedit.text().strip()) > current_model.max_pages or
                    int(self.current_page_lineedit.text().strip()) == old_max_pages):

                self.current_page_lineedit.blockSignals(True)
                self.current_page_lineedit.setText(str(current_model.max_pages))
                self.current_page_lineedit.blockSignals(False)

    def resizeEvent(self, event):
        font = QFont()
        font.setFamily(self.cg_font_family)

        # 48 is an arbitrary number obtained from 561/11, 561 is the minimum width, 11 is the minimum font size
        font.setPointSize(int(self.height() / 48))

        font.setWeight(QFont.Weight.DemiBold)

        self.add_entity_button.setFont(font)
        self.save_changes_button.setFont(font)
        self.undo_all_changes_button.setFont(font)

        self.update_table_views()

    def closeEvent(self, event):
        self.database_handler.close_connection()

    def load_fonts(self):
        # Load fonts, they can be used in any part of the application
        QFontDatabase.addApplicationFont("../assets/fonts/ClashGroteskSemibold.otf")
        QFontDatabase.addApplicationFont("../assets/fonts/ClashGroteskMedium.otf")
        QFontDatabase.addApplicationFont("../assets/fonts/ClashGroteskRegular.otf")
        # Get font id
        cg_font_id = QFontDatabase.addApplicationFont("../assets/fonts/ClashGroteskRegular.otf")

        # Get font family
        self.cg_font_family = QFontDatabase.applicationFontFamilies(cg_font_id)[0]

        self.load_application_window_fonts = LoadApplicationWindowFonts(self)

        self.load_application_window_fonts.load_fonts()
