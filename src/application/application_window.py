from PyQt6.QtWidgets import QMainWindow, QHeaderView, QTableView, QMenu
from PyQt6.QtGui import QFont, QFontDatabase, QPixmap, QIcon, QGuiApplication
from PyQt6.QtCore import Qt, QEvent, QModelIndex

from application.application_window_design import Ui_MainWindow as ApplicationWindowDesign
from application.open_dialogs import OpenDialogs
from application.search_and_sort_header import SearchAndSortHeader
from application.reset_item_delegates import ResetItemDelegates
from application.entity_page_signals import EntityPageSignals
from application.view_demographics_page_controls import ViewDemographicsPageControls

from utils.custom_sort_filter_proxy_model import CustomSortFilterProxyModel
from utils.custom_table_model import CustomTableModel
from utils.specific_buttons_enabler import SpecificButtonsEnabler
from utils.table_view_page_controls import TableViewPageControls

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
        self.entity_page_signals = None

        self.view_demographics_button.clicked.connect(self.change_to_demographics_page)

        self.back_to_main_button.clicked.connect(self.change_to_landing_page)
        self.about_this_app_back_to_main_button.clicked.connect(self.change_to_landing_page)
        self.demographics_back_to_main_button.clicked.connect(self.change_to_landing_page)

        self.setup_table_views()

        self.students_button.clicked.connect(self.change_to_entity_page_student)
        self.programs_button.clicked.connect(self.change_to_entity_page_program)
        self.colleges_button.clicked.connect(self.change_to_entity_page_college)
        self.about_this_app_button.clicked.connect(self.change_to_about_this_app_page)
        self.mode_button.clicked.connect(self.change_mode)

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

    def change_to_landing_page(self):
        self.stackedWidget.setCurrentWidget(self.landing_page)
        self.setWindowTitle("Sequence")

    def change_to_demographics_page(self):
        self.stackedWidget.setCurrentWidget(self.demographics_page)

        self.view_demographics_page_controls = ViewDemographicsPageControls(self.for_view_demographics_page_controls())

    def setup_table_views(self):
        # Students table view
        self.students_table_view.setModel(self.students_sort_filter_proxy_model)
        self.students_table_view.setAlternatingRowColors(True)

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

        # Programs table view
        self.programs_table_view.setModel(self.programs_sort_filter_proxy_model)
        self.programs_table_view.setAlternatingRowColors(True)

        self.programs_table_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

        self.programs_table_horizontal_header = self.programs_table_view.horizontalHeader()

        self.programs_table_horizontal_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.programs_table_horizontal_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.programs_table_horizontal_header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)

        # Colleges table view
        self.colleges_table_view.setModel(self.colleges_sort_filter_proxy_model)
        self.colleges_table_view.setAlternatingRowColors(True)

        self.colleges_table_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

        self.colleges_table_horizontal_header = self.colleges_table_view.horizontalHeader()

        self.colleges_table_horizontal_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.colleges_table_horizontal_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

        self.reset_item_delegates = ResetItemDelegates(self.for_reset_item_delegates())

        self.entity_page_signals = EntityPageSignals(self.for_entity_page_signals())

    def change_to_entity_page_student(self):

        self.stackedWidget.setCurrentWidget(self.entity_page)

        if self.mode == "viewer":
            self.students_table_model.set_mode("viewer")
            self.students_table_view.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
            self.buttons_frame.hide()
        else:
            self.students_table_model.set_mode("admin")
            self.students_table_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            self.buttons_frame.show()

        self.entity_page_layout.activate()

        self.reset_item_delegates.load_item_delegates_for_students_table_view()

        self.entity_type_icon.setPixmap(QPixmap("../assets/images/student_icon.svg"))
        self.entity_type_icon.setScaledContents(True)

        self.entity_type_label.setText("Students")
        self.add_entity_button.setText(" Add student")

        # self.students_table_view.reset()
        self.students_table_model.layoutChanged.emit()

        self.table_view_widgets.setCurrentWidget(self.students_table_view_widget)

        self.current_page_lineedit.setText("1")

        self.previous_page_button.setEnabled(True)

        self.entity_page_signals.remove()

        SearchAndSortHeader.change_contents("student", self.search_type_combobox, "search")
        SearchAndSortHeader.change_contents("student", self.sort_type_combobox, "sort")

        self.search_type_combobox.setCurrentIndex(0)
        self.sort_type_combobox.setCurrentIndex(0)
        self.sort_order_combobox.setCurrentIndex(0)

        self.search_input_lineedit.clear()

        self.entity_page_signals.add("student")

        self.reset_item_delegates.reset("student")

        self.setWindowTitle("Sequence | Students")

        self.students_table_model.set_max_row_per_page(TableViewPageControls.get_max_visible_rows(self.students_table_view))
        self.students_table_model.initialize_data()

        self.students_table_model.update_page_view(self.students_table_view)

        self.previous_page_button.setEnabled(False)
        self.max_pages_label.setText(f"/ {self.students_table_model.max_pages}")

        self.reset_tracked_attributes_of_models("student")

    def change_to_entity_page_program(self):
        self.stackedWidget.setCurrentWidget(self.entity_page)

        if self.mode == "viewer":
            self.programs_table_model.set_mode("viewer")
            self.programs_table_view.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
            self.buttons_frame.hide()
        else:
            self.programs_table_model.set_mode("admin")
            self.programs_table_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            self.buttons_frame.show()

        self.entity_page_layout.activate()

        self.reset_item_delegates.load_item_delegates_for_programs_table_view()

        self.entity_type_icon.setPixmap(QPixmap("../assets/images/book_icon.svg"))
        self.entity_type_icon.setScaledContents(True)

        self.entity_type_label.setText("Programs")

        # self.programs_table_view.reset()
        self.programs_table_model.layoutChanged.emit()

        self.table_view_widgets.setCurrentWidget(self.programs_table_view_widget)

        self.current_page_lineedit.setText("1")

        self.previous_page_button.setEnabled(True)

        self.entity_page_signals.remove()

        SearchAndSortHeader.change_contents("program", self.search_type_combobox, "search")
        SearchAndSortHeader.change_contents("program", self.sort_type_combobox, "sort")

        SpecificButtonsEnabler.enable_save_and_undo_buttons(self.save_changes_button,
                                                            self.undo_all_changes_button,
                                                            self.students_table_model,
                                                            self.programs_table_model,
                                                            self.colleges_table_model)

        self.search_type_combobox.setCurrentIndex(0)
        self.sort_type_combobox.setCurrentIndex(0)
        self.sort_order_combobox.setCurrentIndex(0)

        self.search_input_lineedit.clear()

        self.entity_page_signals.add("program")

        self.reset_item_delegates.reset("program")

        self.setWindowTitle("Sequence | Programs")

        self.programs_table_model.set_max_row_per_page(
            TableViewPageControls.get_max_visible_rows(self.programs_table_view))
        self.programs_table_model.initialize_data()

        self.programs_table_model.update_page_view(self.programs_table_view)

        self.previous_page_button.setEnabled(False)
        self.max_pages_label.setText(f"/ {self.programs_table_model.max_pages}")

        self.reset_tracked_attributes_of_models("program")

    def change_to_entity_page_college(self):
        self.stackedWidget.setCurrentWidget(self.entity_page)

        if self.mode == "viewer":
            self.colleges_table_model.set_mode("viewer")
            self.colleges_table_view.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
            self.buttons_frame.hide()

        else:
            self.colleges_table_model.set_mode("admin")
            self.colleges_table_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            self.buttons_frame.show()

        self.entity_page_layout.activate()

        self.entity_type_label.setText("Colleges")

        self.entity_type_icon.setPixmap(QPixmap("../assets/images/building_icon.svg"))
        self.entity_type_icon.setScaledContents(True)

        self.add_entity_button.setText(" Add college")

        # Probably what fixed the college page issue
        # self.colleges_table_view.reset()
        self.colleges_table_model.layoutChanged.emit()

        self.table_view_widgets.setCurrentWidget(self.colleges_table_view_widget)

        self.current_page_lineedit.setText("1")

        self.previous_page_button.setEnabled(True)

        self.entity_page_signals.remove()

        SearchAndSortHeader.change_contents("college", self.search_type_combobox, "search")
        SearchAndSortHeader.change_contents("college", self.sort_type_combobox, "sort")

        SpecificButtonsEnabler.enable_save_and_undo_buttons(self.save_changes_button,
                                                            self.undo_all_changes_button,
                                                            self.students_table_model,
                                                            self.programs_table_model,
                                                            self.colleges_table_model)

        self.search_type_combobox.setCurrentIndex(0)
        self.sort_type_combobox.setCurrentIndex(0)
        self.sort_order_combobox.setCurrentIndex(0)

        self.search_input_lineedit.clear()

        self.entity_page_signals.add("college")

        self.setWindowTitle("Sequence | Colleges")

        self.colleges_table_model.set_max_row_per_page(
            TableViewPageControls.get_max_visible_rows(self.colleges_table_view))
        self.colleges_table_model.initialize_data()

        self.colleges_table_model.update_page_view(self.colleges_table_view)

        self.previous_page_button.setEnabled(False)
        self.max_pages_label.setText(f"/ {self.colleges_table_model.max_pages}")

        self.reset_tracked_attributes_of_models("college")

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
                self.save_changes_button,
                self.undo_all_changes_button,
                self.sort_type_combobox,
                self.sort_order_combobox,
                self.search_input_lineedit,
                self.search_type_combobox,
                self.search_method_combobox,
                self.students_table_horizontal_header,
                self.programs_table_horizontal_header,
                self.colleges_table_horizontal_header,
                self.reset_item_delegates,
                self.previous_page_button,
                self.next_page_button,
                self.current_page_lineedit,
                self.max_pages_label
                ]

    def for_view_demographics_page_controls(self):
        return [self.demographics_stacked_widget,
                self.general_demographics_widget,
                self.students_demographics_widget,
                self.programs_demographics_widget,
                self.colleges_demographics_widget,
                self.students_table_model,
                self.programs_table_model,
                self.colleges_table_model,
                self.gd_total_colleges_count_label,
                self.gd_total_programs_count_label,
                self.gd_total_students_count_label,
                self.sd_total_students_count_label,
                self.sd_gender_count_label,
                self.sd_year_level_count_label,
                self.pd_select_college_combobox,
                self.pd_select_program_combobox,
                self.pd_total_students_count_label,
                self.pd_year_level_count_label,
                self.pd_gender_count_label,
                self.cd_select_college_combobox,
                self.cd_total_programs_count_label,
                self.cd_total_students_count_label,
                self.cd_gender_count_label,
                self.cd_year_level_count_label,
                self.demographics_type_combobox,
                self]

    def update_table_views(self):

        if (self.stackedWidget.currentWidget() == self.entity_page and
                self.table_view_widgets.currentWidget() == self.students_table_view_widget):

            self.students_table_view.clearSelection()
            self.students_table_view.setCurrentIndex(QModelIndex())

            self.students_table_model.update_page_view(self.students_table_view)

            self.max_pages_label.setText(f"/ {self.students_table_model.max_pages}")

        elif (self.stackedWidget.currentWidget() == self.entity_page and
                self.table_view_widgets.currentWidget() == self.programs_table_view_widget):

            self.programs_table_view.clearSelection()
            self.programs_table_view.setCurrentIndex(QModelIndex())

            self.programs_table_model.update_page_view(self.programs_table_view)

            self.max_pages_label.setText(f"/ {self.programs_table_model.max_pages}")

        elif (self.stackedWidget.currentWidget() == self.entity_page and
                self.table_view_widgets.currentWidget() == self.colleges_table_view_widget):

            self.colleges_table_view.clearSelection()
            self.colleges_table_view.setCurrentIndex(QModelIndex())

            self.colleges_table_model.update_page_view(self.colleges_table_view)

            self.max_pages_label.setText(f"/ {self.colleges_table_model.max_pages}")

    def resizeEvent(self, event):
        font = QFont()
        font.setFamily(self.cg_font_family)

        # 48 is an arbitrary number obtained from 561/11, 561 is the minimum width, 11 is the minimum font size
        font.setPointSize(int(self.height() / 45))

        font.setWeight(QFont.Weight.DemiBold)

        self.add_entity_button.setFont(font)
        self.save_changes_button.setFont(font)
        self.undo_all_changes_button.setFont(font)

        self.update_table_views()

    def changeEvent(self, event):
        if event.type() == QEvent.Type.WindowStateChange:

            if self.windowState() == Qt.WindowState.WindowMinimized or self.windowState() == Qt.WindowState.WindowNoState:
                # Handle minimize state
                # pass
                # self.students_table_view.clearSelection()
                # self.students_table_view.setCurrentIndex(QModelIndex())
                print("Window is minimized")
                # self.students_table_view.setFocusPolicy(Qt.FocusPolicy.NoFocus)
                # self.students_sort_filter_proxy_model.invalidateFilter()
                # self.students_table_view.selectionModel().clear()
            elif self.windowState() == Qt.WindowState.WindowFullScreen or self.windowState() == Qt.WindowState.WindowMaximized:
                # Handle fullscreen state

                # self.students_table_view.clearSelection()
                # self.students_table_view.setCurrentIndex(QModelIndex())
                print("Window is fullscreen!")
        super().changeEvent(event)

    def is_window_fullscreen(self):
        screen_geometry = QGuiApplication.primaryScreen().geometry()
        return self.geometry() == screen_geometry

    def load_fonts(self):
        # Load fonts, they can be used in any part of the application
        QFontDatabase.addApplicationFont("../assets/fonts/ClashGroteskSemibold.otf")
        QFontDatabase.addApplicationFont("../assets/fonts/ClashGroteskMedium.otf")
        QFontDatabase.addApplicationFont("../assets/fonts/ClashGroteskRegular.otf")
        # Get font id
        cg_font_id = QFontDatabase.addApplicationFont("../assets/fonts/ClashGroteskRegular.otf")

        # Get font family
        self.cg_font_family = QFontDatabase.applicationFontFamilies(cg_font_id)[0]

        # Landing Page
        self.landing_subtitle_label.setFont(QFont(self.cg_font_family, 14, QFont.Weight.DemiBold))
        self.landing_title_label.setFont(QFont(self.cg_font_family, 48, QFont.Weight.DemiBold))
        self.mode_label.setFont(QFont(self.cg_font_family, 14, QFont.Weight.DemiBold))
        self.students_button.setFont(QFont(self.cg_font_family, 26, QFont.Weight.DemiBold))
        self.programs_button.setFont(QFont(self.cg_font_family, 26, QFont.Weight.DemiBold))
        self.colleges_button.setFont(QFont(self.cg_font_family, 26, QFont.Weight.DemiBold))
        self.view_demographics_button.setFont(QFont(self.cg_font_family, 26, QFont.Weight.DemiBold))
        self.about_this_app_button.setFont(QFont(self.cg_font_family, 16, QFont.Weight.DemiBold))
        self.mode_button.setFont(QFont(self.cg_font_family, 16, QFont.Weight.DemiBold))

        # About This App Page
        self.about_this_app_label.setFont(QFont(self.cg_font_family, 30, QFont.Weight.Medium))
        self.about_this_app_title_label.setFont(QFont(self.cg_font_family, 30, QFont.Weight.Medium))
        self.scroll_area_title_label.setFont(QFont(self.cg_font_family, 28, QFont.Weight.DemiBold))
        self.scroll_area_contents.setFont(QFont(self.cg_font_family, 13, QFont.Weight.Medium))

        self.about_this_app_back_to_main_button.setFont(QFont(self.cg_font_family, 14, QFont.Weight.DemiBold))

        # View Demographics Page

        self.demographics_label.setFont(QFont(self.cg_font_family, 30, QFont.Weight.Medium))
        self.demographics_title_label.setFont(QFont(self.cg_font_family, 30, QFont.Weight.Medium))

        self.demographics_center_label.setFont(QFont(self.cg_font_family, 28, QFont.Weight.DemiBold))

        self.gd_total_colleges_header_label.setFont(QFont(self.cg_font_family, 18, QFont.Weight.DemiBold))
        self.gd_total_colleges_count_label.setFont(QFont(self.cg_font_family, 28, QFont.Weight.DemiBold))
        self.gd_total_programs_header_label.setFont(QFont(self.cg_font_family, 18, QFont.Weight.DemiBold))
        self.gd_total_programs_count_label.setFont(QFont(self.cg_font_family, 28, QFont.Weight.DemiBold))
        self.gd_total_students_header_label.setFont(QFont(self.cg_font_family, 18, QFont.Weight.DemiBold))
        self.gd_total_students_count_label.setFont(QFont(self.cg_font_family, 28, QFont.Weight.DemiBold))

        self.sd_total_students_header_label.setFont(QFont(self.cg_font_family, 18, QFont.Weight.DemiBold))
        self.sd_total_students_count_label.setFont(QFont(self.cg_font_family, 28, QFont.Weight.DemiBold))
        self.sd_gender_header_label.setFont(QFont(self.cg_font_family, 18, QFont.Weight.DemiBold))
        self.sd_gender_count_label.setFont(QFont(self.cg_font_family, 14, QFont.Weight.DemiBold))
        self.sd_year_level_header_label.setFont(QFont(self.cg_font_family, 18, QFont.Weight.DemiBold))
        self.sd_year_level_count_label.setFont(QFont(self.cg_font_family, 14, QFont.Weight.DemiBold))

        self.pd_total_students_header_label.setFont(QFont(self.cg_font_family, 16, QFont.Weight.DemiBold))
        self.pd_total_students_count_label.setFont(QFont(self.cg_font_family, 28, QFont.Weight.DemiBold))
        self.pd_year_level_header_label.setFont(QFont(self.cg_font_family, 16, QFont.Weight.DemiBold))
        self.pd_year_level_count_label.setFont(QFont(self.cg_font_family, 16, QFont.Weight.DemiBold))
        self.pd_gender_header_label.setFont(QFont(self.cg_font_family, 16, QFont.Weight.DemiBold))
        self.pd_gender_count_label.setFont(QFont(self.cg_font_family, 16, QFont.Weight.DemiBold))

        self.cd_total_programs_header_label.setFont(QFont(self.cg_font_family, 16, QFont.Weight.DemiBold))
        self.cd_total_programs_count_label.setFont(QFont(self.cg_font_family, 28, QFont.Weight.DemiBold))
        self.cd_total_students_header_label.setFont(QFont(self.cg_font_family, 16, QFont.Weight.DemiBold))
        self.cd_total_students_count_label.setFont(QFont(self.cg_font_family, 28, QFont.Weight.DemiBold))
        self.cd_gender_header_label.setFont(QFont(self.cg_font_family, 16, QFont.Weight.DemiBold))
        self.cd_gender_count_label.setFont(QFont(self.cg_font_family, 16, QFont.Weight.DemiBold))
        self.cd_year_level_header_label.setFont(QFont(self.cg_font_family, 16, QFont.Weight.DemiBold))
        self.cd_year_level_count_label.setFont(QFont(self.cg_font_family, 16, QFont.Weight.DemiBold))

        self.demographics_type_combobox.setStyleSheet(f"""
                    QComboBox {{
                        font-family: {self.cg_font_family};
                        font-size: 32px;
                        font-weight: {QFont.Weight.DemiBold};
                    }}
                """)

        self.pd_select_college_combobox.setStyleSheet(f"""
                    QComboBox {{
                        font-family: {self.cg_font_family};
                        font-size: 18px;
                        font-weight: {QFont.Weight.Medium};
                    }}
                """)

        self.pd_select_program_combobox.setStyleSheet(f"""
                    QComboBox {{
                        font-family: {self.cg_font_family};
                        font-size: 18px;
                        font-weight: {QFont.Weight.Medium};
                    }}
                """)

        self.cd_select_college_combobox.setStyleSheet(f"""
                    QComboBox {{
                        font-family: {self.cg_font_family};
                        font-size: 18px;
                        font-weight: {QFont.Weight.Medium};
                    }}
                """)

        self.demographics_back_to_main_button.setFont(QFont(self.cg_font_family, 14, QFont.Weight.DemiBold))

        # Entity Page
        self.entity_type_label.setFont(QFont(self.cg_font_family, 30, QFont.Weight.Medium))
        self.title_label.setFont(QFont(self.cg_font_family, 30, QFont.Weight.Medium))
        self.sort_label.setFont(QFont(self.cg_font_family, 13, QFont.Weight.Medium))

        self.sort_type_combobox.setStyleSheet(f"""
                    QComboBox {{
                        font-family: {self.cg_font_family};
                        font-size: 16px;
                        font-weight: {QFont.Weight.Medium};
                    }}
                """)

        self.sort_order_combobox.setStyleSheet(f"""
                            QComboBox {{
                                font-family: {self.cg_font_family};
                                font-size: 16px;
                                font-weight: {QFont.Weight.Medium};
                            }}
                        """)

        self.search_label.setFont(QFont(self.cg_font_family, 13, QFont.Weight.Medium))

        self.search_type_combobox.setStyleSheet(f"""
                                    QComboBox {{
                                        font-family: {self.cg_font_family};
                                        font-size: 16px;
                                        font-weight: {QFont.Weight.Medium};
                                    }}
                                """)

        self.search_method_combobox.setStyleSheet(f"""
                                            QComboBox {{
                                                font-family: {self.cg_font_family};
                                                font-size: 16px;
                                                font-weight: {QFont.Weight.Medium};
                                            }}
                                        """)

        self.search_input_lineedit.setFont(QFont(self.cg_font_family, 13, QFont.Weight.Medium))

        self.students_table_view.setStyleSheet(f"""
                                            QHeaderView::section {{
                                                font-family: {self.cg_font_family};
                                                font-size: 17px;
                                                font-weight: {QFont.Weight.DemiBold};
                                            }}
                                        """)

        self.programs_table_view.setStyleSheet(f"""
                                                    QHeaderView::section {{
                                                        font-family: {self.cg_font_family};
                                                        font-size: 17px;
                                                        font-weight: {QFont.Weight.DemiBold};
                                                    }}
                                                """)

        self.colleges_table_view.setStyleSheet(f"""
                                                    QHeaderView::section {{
                                                        font-family: {self.cg_font_family};
                                                        font-size: 17px;
                                                        font-weight: {QFont.Weight.DemiBold};
                                                    }}
                                                """)

        self.back_to_main_button.setFont(QFont(self.cg_font_family, 14, QFont.Weight.DemiBold))
