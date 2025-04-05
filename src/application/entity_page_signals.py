from PyQt6.QtCore import QTimer, QObject

from application.open_dialogs import OpenDialogs
from application.search_and_sort_header import SearchAndSortHeader
from application.context_menu_setup import ContextMenuSetup

from utils.table_view_page_controls import TableViewPageControls


class EntityPageSignals:
    def __init__(self, entity_page_elements):

        self.students_table_view = entity_page_elements[0]
        self.programs_table_view = entity_page_elements[1]
        self.colleges_table_view = entity_page_elements[2]

        self.students_table_model = entity_page_elements[3]
        self.programs_table_model = entity_page_elements[4]
        self.colleges_table_model = entity_page_elements[5]

        self.students_sort_filter_proxy_model = entity_page_elements[6]
        self.programs_sort_filter_proxy_model = entity_page_elements[7]
        self.colleges_sort_filter_proxy_model = entity_page_elements[8]

        self.add_entity_button = entity_page_elements[9]
        self.view_demographics_button = entity_page_elements[10]
        self.sort_type_combobox = entity_page_elements[11]
        self.sort_order_combobox = entity_page_elements[12]
        self.search_input_lineedit = entity_page_elements[13]
        self.search_type_combobox = entity_page_elements[14]

        self.students_table_horizontal_header = entity_page_elements[15]
        self.programs_table_horizontal_header = entity_page_elements[16]
        self.colleges_table_horizontal_header = entity_page_elements[17]

        self.reset_item_delegates = entity_page_elements[18]

        self.previous_page_button = entity_page_elements[19]
        self.next_page_button = entity_page_elements[20]
        self.current_page_lineedit = entity_page_elements[21]
        self.max_pages_label = entity_page_elements[22]

        self.open_dialogs = OpenDialogs()

        self.students_table_view_context_menu = ContextMenuSetup(self.students_table_view,
                                                                 self.students_table_model,
                                                                 self.programs_table_model,
                                                                 self.colleges_table_model,
                                                                 self.reset_item_delegates.reset,
                                                                 'student')

        self.programs_table_view_context_menu = ContextMenuSetup(self.programs_table_view,
                                                                 self.students_table_model,
                                                                 self.programs_table_model,
                                                                 self.colleges_table_model,
                                                                 self.reset_item_delegates.reset,
                                                                 'program')

        self.colleges_table_view_context_menu = ContextMenuSetup(self.colleges_table_view,
                                                                 self.students_table_model,
                                                                 self.programs_table_model,
                                                                 self.colleges_table_model,
                                                                 self.reset_item_delegates.reset,
                                                                 'college')


        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)

    def add(self, entity_type):
        # self.remove()

        if entity_type == "student":

            self.students_table_view.doubleClicked.connect(self.reset_item_delegates.
                                                           show_combobox_delegate_students_table_view)

            self.students_table_view.customContextMenuRequested.connect(self.students_table_view_context_menu.show_context_menu)

            (self.add_entity_button.clicked.connect
             (lambda: self.open_dialogs.open_add_entity_dialog_for_students(self.students_table_view,
                                                                            self.students_table_model,
                                                                            self.view_demographics_button,
                                                                            self.reset_item_delegates.reset)))

            self.search_input_lineedit.textChanged.connect(self.on_text_changed_search_lineedit)

            self.search_timer.timeout.connect(lambda: SearchAndSortHeader.search_using_lineedit(entity_type,
                                                                                                self.search_type_combobox,
                                                                                                self.search_input_lineedit,
                                                                                                self.students_table_model,
                                                                                                self.reset_item_delegates.reset,
                                                                                                self.students_table_view,
                                                                                                self.current_page_lineedit,
                                                                                                self.max_pages_label,
                                                                                                self.previous_page_button,
                                                                                                self.next_page_button
                                                                                                ))

            self.sort_type_combobox.currentTextChanged.connect(
                lambda: SearchAndSortHeader.change_sort_type(entity_type,
                                                             self.sort_order_combobox,
                                                             self.students_table_model,
                                                             self.students_sort_filter_proxy_model,
                                                             self.reset_item_delegates.reset))

            self.sort_order_combobox.currentTextChanged.connect(
                lambda: SearchAndSortHeader.sort_using_combobox(entity_type,
                                                                self.sort_type_combobox,
                                                                self.sort_order_combobox,
                                                                self.students_table_model,
                                                                self.reset_item_delegates.reset,
                                                                self.students_table_view,
                                                                self.current_page_lineedit,
                                                                self.max_pages_label))

            self.previous_page_button.clicked.connect(
                lambda: TableViewPageControls.go_to_previous_page(self.students_table_model,
                                                                  self.current_page_lineedit))

            self.next_page_button.clicked.connect(
                lambda: TableViewPageControls.go_to_next_page(self.students_table_model,
                                                              self.current_page_lineedit))

        elif entity_type == "program":

            self.programs_table_view.doubleClicked.connect(self.reset_item_delegates.
                                                           show_combobox_delegate_programs_table_view)

            self.programs_table_view.customContextMenuRequested.connect(
                self.programs_table_view_context_menu.show_context_menu)

            (self.add_entity_button.clicked.connect
             (lambda: self.open_dialogs.open_add_entity_dialog_for_programs(self.programs_table_view,
                                                                            self.programs_table_model,
                                                                            self.view_demographics_button,
                                                                            self.reset_item_delegates.reset)))

            self.search_input_lineedit.textChanged.connect(self.on_text_changed_search_lineedit)

            self.search_timer.timeout.connect(
                lambda: SearchAndSortHeader.search_using_lineedit(entity_type,
                                                                  self.search_type_combobox,
                                                                  self.search_input_lineedit,
                                                                  self.programs_table_model,
                                                                  self.reset_item_delegates.reset,
                                                                  self.programs_table_view,
                                                                  self.current_page_lineedit,
                                                                  self.max_pages_label,
                                                                  self.previous_page_button,
                                                                  self.next_page_button
                                                                  ))

            self.sort_type_combobox.currentTextChanged.connect(
                lambda: SearchAndSortHeader.change_sort_type(entity_type,
                                                             self.sort_order_combobox,
                                                             self.programs_table_model,
                                                             self.programs_sort_filter_proxy_model,
                                                             self.reset_item_delegates.reset))

            self.sort_order_combobox.currentTextChanged.connect(
                lambda: SearchAndSortHeader.sort_using_combobox(entity_type,
                                                                self.sort_type_combobox,
                                                                self.sort_order_combobox,
                                                                self.programs_table_model,
                                                                self.reset_item_delegates.reset,
                                                                self.programs_table_view,
                                                                self.current_page_lineedit,
                                                                self.max_pages_label))

            self.previous_page_button.clicked.connect(
                lambda: TableViewPageControls.go_to_previous_page(self.programs_table_model,
                                                                  self.current_page_lineedit))

            self.next_page_button.clicked.connect(
                lambda: TableViewPageControls.go_to_next_page(self.programs_table_model,
                                                              self.current_page_lineedit))

        elif entity_type == "college":

            self.colleges_table_view.customContextMenuRequested.connect(
                self.colleges_table_view_context_menu.show_context_menu)

            (self.add_entity_button.clicked.connect
             (lambda: self.open_dialogs.open_add_entity_dialog_for_colleges(self.colleges_table_view,
                                                                            self.colleges_table_model,
                                                                            self.view_demographics_button,
                                                                            self.reset_item_delegates.reset)))

            self.search_input_lineedit.textChanged.connect(self.on_text_changed_search_lineedit)

            self.search_timer.timeout.connect(
                lambda: SearchAndSortHeader.search_using_lineedit(entity_type,
                                                                  self.search_type_combobox,
                                                                  self.search_input_lineedit,
                                                                  self.colleges_table_model,
                                                                  self.reset_item_delegates.reset,
                                                                  self.colleges_table_view,
                                                                  self.current_page_lineedit,
                                                                  self.max_pages_label,
                                                                  self.previous_page_button,
                                                                  self.next_page_button
                                                                  ))

            self.sort_type_combobox.currentTextChanged.connect(
                lambda: SearchAndSortHeader.change_sort_type(entity_type,
                                                             self.sort_order_combobox,
                                                             self.colleges_table_model,
                                                             self.colleges_sort_filter_proxy_model,
                                                             self.reset_item_delegates.reset))

            self.sort_order_combobox.currentTextChanged.connect(
                lambda: SearchAndSortHeader.sort_using_combobox(entity_type,
                                                                self.sort_type_combobox,
                                                                self.sort_order_combobox,
                                                                self.colleges_table_model,
                                                                self.reset_item_delegates.reset,
                                                                self.colleges_table_view,
                                                                self.current_page_lineedit,
                                                                self.max_pages_label))

            self.previous_page_button.clicked.connect(
                lambda: TableViewPageControls.go_to_previous_page(self.colleges_table_model,
                                                                  self.current_page_lineedit))

            self.next_page_button.clicked.connect(
                lambda: TableViewPageControls.go_to_next_page(self.colleges_table_model,
                                                              self.current_page_lineedit))

        self.search_type_combobox.currentIndexChanged.connect(
            lambda: SearchAndSortHeader.change_search_lineedit_placeholder(self.search_type_combobox,
                                                                           self.search_input_lineedit))

    def on_text_changed_search_lineedit(self):
        # So everytime a key gets entered in self.search_input_lineedit,
        #   the timer resets

        self.search_timer.stop()
        self.search_timer.start(500)

        # Once the timer reaches 500 milliseconds, the function connected to this timer will execute

    def remove(self):
        self.add_entity_button.disconnect()

        self.sort_type_combobox.disconnect()
        self.sort_order_combobox.disconnect()

        try:
            self.search_timer.timeout.disconnect()
            self.search_input_lineedit.textChanged.disconnect()

        except TypeError:
            pass

        self.previous_page_button.disconnect()
        self.next_page_button.disconnect()
