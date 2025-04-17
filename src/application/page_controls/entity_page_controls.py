from PyQt6.QtCore import QTimer, QObject

from application.open_dialogs import OpenDialogs
from application.search_and_sort_header import SearchAndSortHeader
from application.context_menu_setup import ContextMenuSetup

from application.page_controls.table_view_page_controls import TableViewPageControls


class EntityPageControls:
    def __init__(self, application_window):

        self.aw = application_window

        self.page_buttons = {"previous_page": self.aw.previous_page_button,
                             "next_page": self.aw.next_page_button,
                             "first_page": self.aw.first_page_button,
                             "last_page": self.aw.last_page_button}

        self.current_entity_type = None

        self.open_dialogs = OpenDialogs(self.aw)

        self.students_table_view_context_menu = ContextMenuSetup(self.aw.students_table_view,
                                                                 self.aw.students_table_model,
                                                                 self.aw.programs_table_model,
                                                                 self.aw.colleges_table_model,
                                                                 self.aw.current_page_lineedit,
                                                                 self.aw.max_pages_label,
                                                                 self.aw.save_changes_button,
                                                                 self.aw.undo_all_changes_button,
                                                                 self.aw.reset_item_delegates.reset,
                                                                 'student')

        self.programs_table_view_context_menu = ContextMenuSetup(self.aw.programs_table_view,
                                                                 self.aw.students_table_model,
                                                                 self.aw.programs_table_model,
                                                                 self.aw.colleges_table_model,
                                                                 self.aw.current_page_lineedit,
                                                                 self.aw.max_pages_label,
                                                                 self.aw.save_changes_button,
                                                                 self.aw.undo_all_changes_button,
                                                                 self.aw.reset_item_delegates.reset,
                                                                 'program')

        self.colleges_table_view_context_menu = ContextMenuSetup(self.aw.colleges_table_view,
                                                                 self.aw.students_table_model,
                                                                 self.aw.programs_table_model,
                                                                 self.aw.colleges_table_model,
                                                                 self.aw.current_page_lineedit,
                                                                 self.aw.max_pages_label,
                                                                 self.aw.save_changes_button,
                                                                 self.aw.undo_all_changes_button,
                                                                 self.aw.reset_item_delegates.reset,
                                                                 'college')

        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)

    def add(self, entity_type):
        # self.remove()

        if entity_type == "student":

            self.aw.students_table_view.doubleClicked.connect(self.aw.reset_item_delegates.
                                                           show_combobox_delegate_students_table_view)

            self.aw.students_table_view.customContextMenuRequested.connect(self.students_table_view_context_menu.show_context_menu)

            (self.aw.add_entity_button.clicked.connect
             (lambda: self.open_dialogs.open_add_entity_dialog_for_students()))

            self.aw.search_input_lineedit.textChanged.connect(self.on_text_changed_search_lineedit)
            self.aw.search_type_combobox.currentTextChanged.connect(self.on_text_changed_search_lineedit)
            self.aw.search_method_combobox.currentTextChanged.connect(self.on_text_changed_search_lineedit)

            self.search_timer.timeout.connect(lambda: SearchAndSortHeader.search_using_lineedit(entity_type,
                                                                                                self.aw.search_type_combobox,
                                                                                                self.aw.search_method_combobox,
                                                                                                self.aw.search_input_lineedit,
                                                                                                self.aw.students_table_model,
                                                                                                self.aw.reset_item_delegates.reset,
                                                                                                self.aw.students_table_view,
                                                                                                self.aw.current_page_lineedit,
                                                                                                self.aw.max_pages_label
                                                                                                ))

            self.aw.sort_type_combobox.currentTextChanged.connect(
                lambda: SearchAndSortHeader.change_sort_type(entity_type,
                                                             self.aw.sort_order_combobox,
                                                             self.aw.students_table_model,
                                                             self.aw.students_sort_filter_proxy_model,
                                                             self.aw.reset_item_delegates.reset))

            self.aw.sort_order_combobox.currentTextChanged.connect(
                lambda: SearchAndSortHeader.sort_using_combobox(entity_type,
                                                                self.aw.sort_type_combobox,
                                                                self.aw.sort_order_combobox,
                                                                self.aw.students_table_model,
                                                                self.aw.reset_item_delegates.reset,
                                                                self.aw.students_table_view,
                                                                self.aw.current_page_lineedit,
                                                                self.aw.max_pages_label))

            self.aw.current_page_lineedit.textChanged.connect(
                lambda: TableViewPageControls.go_to_specific_page(self.aw.students_table_view,
                                                                  self.aw.students_table_model,
                                                                  self.aw.current_page_lineedit,
                                                                  self.page_buttons))

            self.aw.previous_page_button.clicked.connect(
                lambda: TableViewPageControls.go_to_previous_page(self.aw.students_table_view,
                                                                  self.aw.students_table_model,
                                                                  self.aw.current_page_lineedit,
                                                                  self.page_buttons))

            self.aw.next_page_button.clicked.connect(
                lambda: TableViewPageControls.go_to_next_page(self.aw.students_table_view,
                                                              self.aw.students_table_model,
                                                              self.aw.current_page_lineedit,
                                                              self.page_buttons))

            self.aw.first_page_button.clicked.connect(
                lambda: TableViewPageControls.go_to_first_page(self.aw.students_table_view,
                                                               self.aw.students_table_model,
                                                               self.aw.current_page_lineedit,
                                                               self.page_buttons))

            self.aw.last_page_button.clicked.connect(
                lambda: TableViewPageControls.go_to_last_page(self.aw.students_table_view,
                                                              self.aw.students_table_model,
                                                              self.aw.current_page_lineedit,
                                                              self.page_buttons))

        elif entity_type == "program":

            self.aw.programs_table_view.doubleClicked.connect(self.aw.reset_item_delegates.
                                                           show_combobox_delegate_programs_table_view)

            self.aw.programs_table_view.customContextMenuRequested.connect(
                self.programs_table_view_context_menu.show_context_menu)

            (self.aw.add_entity_button.clicked.connect
             (lambda: self.open_dialogs.open_add_entity_dialog_for_programs()))

            self.aw.search_input_lineedit.textChanged.connect(self.on_text_changed_search_lineedit)
            self.aw.search_type_combobox.currentTextChanged.connect(self.on_text_changed_search_lineedit)
            self.aw.search_method_combobox.currentTextChanged.connect(self.on_text_changed_search_lineedit)

            self.search_timer.timeout.connect(
                lambda: SearchAndSortHeader.search_using_lineedit(entity_type,
                                                                  self.aw.search_type_combobox,
                                                                  self.aw.search_method_combobox,
                                                                  self.aw.search_input_lineedit,
                                                                  self.aw.programs_table_model,
                                                                  self.aw.reset_item_delegates.reset,
                                                                  self.aw.programs_table_view,
                                                                  self.aw.current_page_lineedit,
                                                                  self.aw.max_pages_label
                                                                  ))

            self.aw.sort_type_combobox.currentTextChanged.connect(
                lambda: SearchAndSortHeader.change_sort_type(entity_type,
                                                             self.aw.sort_order_combobox,
                                                             self.aw.programs_table_model,
                                                             self.aw.programs_sort_filter_proxy_model,
                                                             self.aw.reset_item_delegates.reset))

            self.aw.sort_order_combobox.currentTextChanged.connect(
                lambda: SearchAndSortHeader.sort_using_combobox(entity_type,
                                                                self.aw.sort_type_combobox,
                                                                self.aw.sort_order_combobox,
                                                                self.aw.programs_table_model,
                                                                self.aw.reset_item_delegates.reset,
                                                                self.aw.programs_table_view,
                                                                self.aw.current_page_lineedit,
                                                                self.aw.max_pages_label))

            self.aw.current_page_lineedit.textChanged.connect(
                lambda: TableViewPageControls.go_to_specific_page(self.aw.programs_table_view,
                                                                  self.aw.programs_table_model,
                                                                  self.aw.current_page_lineedit,
                                                                  self.page_buttons))

            self.aw.previous_page_button.clicked.connect(
                lambda: TableViewPageControls.go_to_previous_page(self.aw.programs_table_view,
                                                                  self.aw.programs_table_model,
                                                                  self.aw.current_page_lineedit,
                                                                  self.page_buttons))

            self.aw.next_page_button.clicked.connect(
                lambda: TableViewPageControls.go_to_next_page(self.aw.programs_table_view,
                                                              self.aw.programs_table_model,
                                                              self.aw.current_page_lineedit,
                                                              self.page_buttons))

            self.aw.first_page_button.clicked.connect(
                lambda: TableViewPageControls.go_to_first_page(self.aw.programs_table_view,
                                                               self.aw.programs_table_model,
                                                               self.aw.current_page_lineedit,
                                                               self.page_buttons))

            self.aw.last_page_button.clicked.connect(
                lambda: TableViewPageControls.go_to_last_page(self.aw.programs_table_view,
                                                              self.aw.programs_table_model,
                                                              self.aw.current_page_lineedit,
                                                              self.page_buttons))

        elif entity_type == "college":

            self.aw.colleges_table_view.customContextMenuRequested.connect(
                self.colleges_table_view_context_menu.show_context_menu)

            (self.aw.add_entity_button.clicked.connect
             (lambda: self.open_dialogs.open_add_entity_dialog_for_colleges()))

            self.aw.search_input_lineedit.textChanged.connect(self.on_text_changed_search_lineedit)
            self.aw.search_type_combobox.currentTextChanged.connect(self.on_text_changed_search_lineedit)
            self.aw.search_method_combobox.currentTextChanged.connect(self.on_text_changed_search_lineedit)

            self.search_timer.timeout.connect(
                lambda: SearchAndSortHeader.search_using_lineedit(entity_type,
                                                                  self.aw.search_type_combobox,
                                                                  self.aw.search_method_combobox,
                                                                  self.aw.search_input_lineedit,
                                                                  self.aw.colleges_table_model,
                                                                  self.aw.reset_item_delegates.reset,
                                                                  self.aw.colleges_table_view,
                                                                  self.aw.current_page_lineedit,
                                                                  self.aw.max_pages_label
                                                                  ))

            self.aw.sort_type_combobox.currentTextChanged.connect(
                lambda: SearchAndSortHeader.change_sort_type(entity_type,
                                                             self.aw.sort_order_combobox,
                                                             self.aw.colleges_table_model,
                                                             self.aw.colleges_sort_filter_proxy_model,
                                                             self.aw.reset_item_delegates.reset))

            self.aw.sort_order_combobox.currentTextChanged.connect(
                lambda: SearchAndSortHeader.sort_using_combobox(entity_type,
                                                                self.aw.sort_type_combobox,
                                                                self.aw.sort_order_combobox,
                                                                self.aw.colleges_table_model,
                                                                self.aw.reset_item_delegates.reset,
                                                                self.aw.colleges_table_view,
                                                                self.aw.current_page_lineedit,
                                                                self.aw.max_pages_label))

            self.aw.current_page_lineedit.textChanged.connect(
                lambda: TableViewPageControls.go_to_specific_page(self.aw.colleges_table_view,
                                                                  self.aw.colleges_table_model,
                                                                  self.aw.current_page_lineedit,
                                                                  self.page_buttons))

            self.aw.previous_page_button.clicked.connect(
                lambda: TableViewPageControls.go_to_previous_page(self.aw.colleges_table_view,
                                                                  self.aw.colleges_table_model,
                                                                  self.aw.current_page_lineedit,
                                                                  self.page_buttons))

            self.aw.next_page_button.clicked.connect(
                lambda: TableViewPageControls.go_to_next_page(self.aw.colleges_table_view,
                                                              self.aw.colleges_table_model,
                                                              self.aw.current_page_lineedit,
                                                              self.page_buttons))

            self.aw.first_page_button.clicked.connect(
                lambda: TableViewPageControls.go_to_first_page(self.aw.colleges_table_view,
                                                               self.aw.colleges_table_model,
                                                               self.aw.current_page_lineedit,
                                                               self.page_buttons))

            self.aw.last_page_button.clicked.connect(
                lambda: TableViewPageControls.go_to_last_page(self.aw.colleges_table_view,
                                                              self.aw.colleges_table_model,
                                                              self.aw.current_page_lineedit,
                                                              self.page_buttons))

        self.aw.search_type_combobox.currentIndexChanged.connect(
            lambda: SearchAndSortHeader.change_search_lineedit_placeholder(self.aw.search_type_combobox,
                                                                           self.aw.search_input_lineedit))

        (self.aw.save_changes_button.clicked.connect
         (lambda: self.open_dialogs.open_confirm_save_or_undo_dialog(entity_type, "save", self.aw.max_pages_label)))

        (self.aw.undo_all_changes_button.clicked.connect
         (lambda: self.open_dialogs.open_confirm_save_or_undo_dialog(entity_type, "undo", self.aw.max_pages_label)))

    def on_text_changed_search_lineedit(self):
        # So everytime a key gets entered in self.search_input_lineedit,
        #   the timer resets

        self.search_timer.stop()
        self.search_timer.start(500)

        # Once the timer reaches 500 milliseconds, the function connected to this timer will execute

    def remove(self):
        self.aw.add_entity_button.disconnect()
        self.aw.save_changes_button.disconnect()
        self.aw.undo_all_changes_button.disconnect()

        self.aw.sort_type_combobox.disconnect()
        self.aw.sort_order_combobox.disconnect()

        try:
            self.search_timer.timeout.disconnect()
            self.aw.search_input_lineedit.textChanged.disconnect()

        except TypeError:
            pass

        self.aw.previous_page_button.disconnect()
        self.aw.next_page_button.disconnect()
        self.aw.first_page_button.disconnect()
        self.aw.last_page_button.disconnect()

        self.aw.current_page_lineedit.disconnect()
