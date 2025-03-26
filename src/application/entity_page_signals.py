from application.open_dialogs import OpenDialogs
from application.search_and_sort_header import SearchAndSortHeader
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
        self.delete_entity_button = entity_page_elements[10]
        self.edit_entity_button = entity_page_elements[11]
        self.save_changes_button = entity_page_elements[12]
        self.view_demographics_button = entity_page_elements[13]
        self.sort_type_combobox = entity_page_elements[14]
        self.sort_order_combobox = entity_page_elements[15]
        self.search_input_lineedit = entity_page_elements[16]
        self.search_type_combobox = entity_page_elements[17]

        self.students_table_horizontal_header = entity_page_elements[18]
        self.programs_table_horizontal_header = entity_page_elements[19]
        self.colleges_table_horizontal_header = entity_page_elements[20]

        self.reset_item_delegates = entity_page_elements[21]

        self.previous_page_button = entity_page_elements[22]
        self.next_page_button = entity_page_elements[23]
        self.current_page_lineedit = entity_page_elements[24]
        self.max_pages_label = entity_page_elements[25]

        self.open_dialogs = OpenDialogs()

    def add(self, entity_type):
        # self.remove()

        if entity_type == "student":

            self.students_table_view.doubleClicked.connect(self.reset_item_delegates.
                                                           show_combobox_delegate_students_table_view)

            (self.add_entity_button.clicked.connect
             (lambda: self.open_dialogs.open_add_entity_dialog_for_students(self.students_table_view,
                                                                            self.students_table_model,
                                                                            self.programs_table_model,
                                                                            self.colleges_table_model,
                                                                            self.delete_entity_button,
                                                                            self.edit_entity_button,
                                                                            self.save_changes_button,
                                                                            self.view_demographics_button,
                                                                            self.reset_item_delegates.reset)))

            self.edit_entity_button.clicked.connect(
                lambda: self.open_dialogs.open_edit_entity_dialog_for_students(self.students_table_view,
                                                                               self.students_table_model,
                                                                               self.programs_table_model,
                                                                               self.colleges_table_model,
                                                                               self.save_changes_button,
                                                                               self.reset_item_delegates.reset))

            self.delete_entity_button.clicked.connect(
                lambda: self.open_dialogs.open_delete_entity_dialog_for_students(self.students_table_view,
                                                                                 self.students_table_model,
                                                                                 self.delete_entity_button,
                                                                                 self.edit_entity_button,
                                                                                 self.save_changes_button,
                                                                                 self.view_demographics_button,
                                                                                 self.reset_item_delegates.reset,
                                                                                 self.students_table_horizontal_header))

            self.view_demographics_button.clicked.connect(
                lambda: self.open_dialogs.open_students_demographic_dialog(self.students_table_model,
                                                                           self.programs_table_model,
                                                                           self.colleges_table_model))

            self.search_input_lineedit.textChanged.connect(
                lambda: SearchAndSortHeader.search_using_lineedit(entity_type,
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

            (self.add_entity_button.clicked.connect
             (lambda: self.open_dialogs.open_add_entity_dialog_for_programs(self.programs_table_view,
                                                                            self.programs_table_model,
                                                                            self.colleges_table_model,
                                                                            self.delete_entity_button,
                                                                            self.edit_entity_button,
                                                                            self.save_changes_button,
                                                                            self.view_demographics_button,
                                                                            self.reset_item_delegates.reset)))

            self.edit_entity_button.clicked.connect(
                lambda: self.open_dialogs.open_edit_entity_dialog_for_programs(self.programs_table_view,
                                                                               self.programs_table_model,
                                                                               self.students_table_model,
                                                                               self.colleges_table_model,
                                                                               self.save_changes_button,
                                                                               self.reset_item_delegates.reset))

            self.delete_entity_button.clicked.connect(
                lambda: self.open_dialogs.open_delete_entity_dialog_for_programs(self.programs_table_view,
                                                                                 self.programs_table_model,
                                                                                 self.students_table_model,
                                                                                 self.colleges_table_model,
                                                                                 self.delete_entity_button,
                                                                                 self.edit_entity_button,
                                                                                 self.save_changes_button,
                                                                                 self.view_demographics_button,
                                                                                 self.reset_item_delegates.reset,
                                                                                 self.programs_table_horizontal_header))

            self.view_demographics_button.clicked.connect(
                lambda: self.open_dialogs.open_programs_demographic_dialog(self.students_table_model,
                                                                           self.programs_table_model,
                                                                           self.colleges_table_model))

            self.search_input_lineedit.textChanged.connect(
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
            (self.add_entity_button.clicked.connect
             (lambda: self.open_dialogs.open_add_entity_dialog_for_colleges(self.colleges_table_view,
                                                                            self.colleges_table_model,
                                                                            self.delete_entity_button,
                                                                            self.edit_entity_button,
                                                                            self.save_changes_button,
                                                                            self.view_demographics_button,
                                                                            self.reset_item_delegates.reset)))

            self.edit_entity_button.clicked.connect(
                lambda: self.open_dialogs.open_edit_entity_dialog_for_colleges(self.colleges_table_view,
                                                                               self.programs_table_model,
                                                                               self.colleges_table_model,
                                                                               self.save_changes_button,
                                                                               self.reset_item_delegates.reset))

            self.delete_entity_button.clicked.connect(
                lambda: self.open_dialogs.open_delete_entity_dialog_for_colleges(self.colleges_table_view,
                                                                                 self.colleges_table_model,
                                                                                 self.students_table_model,
                                                                                 self.programs_table_model,
                                                                                 self.delete_entity_button,
                                                                                 self.edit_entity_button,
                                                                                 self.save_changes_button,
                                                                                 self.view_demographics_button,
                                                                                 self.reset_item_delegates.reset,
                                                                                 self.colleges_table_horizontal_header))

            self.view_demographics_button.clicked.connect(
                lambda: self.open_dialogs.open_colleges_demographic_dialog(self.students_table_model,
                                                                           self.programs_table_model,
                                                                           self.colleges_table_model))

            self.search_input_lineedit.textChanged.connect(
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
                                                                  self.current_page_lineedit,
                                                                  self.previous_page_button,
                                                                  self.next_page_button))

            self.next_page_button.clicked.connect(
                lambda: TableViewPageControls.go_to_next_page(self.colleges_table_model,
                                                              self.current_page_lineedit,
                                                              self.previous_page_button,
                                                              self.next_page_button))


        self.save_changes_button.clicked.connect(
            lambda: self.open_dialogs.open_confirm_save_dialog(self.students_table_model,
                                                               self.programs_table_model,
                                                               self.colleges_table_model,
                                                               self.save_changes_button))

        self.search_type_combobox.currentIndexChanged.connect(
            lambda: SearchAndSortHeader.change_search_lineedit_placeholder(self.search_type_combobox,
                                                                           self.search_input_lineedit))

    def remove(self):
        self.add_entity_button.disconnect()
        self.edit_entity_button.disconnect()
        self.delete_entity_button.disconnect()
        self.save_changes_button.disconnect()
        self.view_demographics_button.disconnect()

        self.sort_type_combobox.disconnect()
        self.sort_order_combobox.disconnect()

        self.previous_page_button.disconnect()
        self.next_page_button.disconnect()
