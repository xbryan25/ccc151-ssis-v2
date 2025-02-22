
from application.open_dialogs import OpenDialogs
from application.search_header import SearchHeader

# Put this in a list

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
        self.search_input_lineedit = entity_page_elements[14]
        self.search_type_combobox = entity_page_elements[15]

        self.students_table_horizontal_header = entity_page_elements[16]
        self.programs_table_horizontal_header = entity_page_elements[17]
        self.colleges_table_horizontal_header = entity_page_elements[18]

        self.students_table_reset_sorting_state = entity_page_elements[19]
        self.programs_table_reset_sorting_state = entity_page_elements[20]
        self.colleges_table_reset_sorting_state = entity_page_elements[21]

        self.reset_item_delegates = entity_page_elements[22]

        self.open_dialogs = OpenDialogs()

    def add(self, entity_type):
        self.remove()

        if entity_type == "student":

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
                lambda: SearchHeader.search_using_lineedit(entity_type,
                                                           self.search_type_combobox,
                                                           self.search_input_lineedit,
                                                           self.students_table_model,
                                                           self.students_sort_filter_proxy_model,
                                                           self.reset_item_delegates.reset))


            self.students_table_horizontal_header.sectionClicked.connect(
                self.students_table_reset_sorting_state.reset_sorting_state)

        elif entity_type == "program":
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
                lambda: SearchHeader.search_using_lineedit(entity_type,
                                                           self.search_type_combobox,
                                                           self.search_input_lineedit,
                                                           self.programs_table_model,
                                                           self.programs_sort_filter_proxy_model,
                                                           self.reset_item_delegates.reset))

            self.programs_table_horizontal_header.sectionClicked.connect(
                self.programs_table_reset_sorting_state.reset_sorting_state)

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
                lambda: SearchHeader.search_using_lineedit(entity_type,
                                                           self.search_type_combobox,
                                                           self.search_input_lineedit,
                                                           self.colleges_table_model,
                                                           self.colleges_sort_filter_proxy_model,
                                                           self.reset_item_delegates.reset))

            self.colleges_table_horizontal_header.sectionClicked.connect(
                self.colleges_table_reset_sorting_state.reset_sorting_state)

        self.save_changes_button.clicked.connect(
            lambda: self.open_dialogs.open_confirm_save_dialog(entity_type,
                                                               self.students_table_model,
                                                               self.programs_table_model,
                                                               self.colleges_table_model,
                                                               self.save_changes_button))

        self.search_type_combobox.currentIndexChanged.connect(
            lambda: SearchHeader.change_search_lineedit_placeholder(self.search_type_combobox,
                                                                    self.search_input_lineedit))

    def remove(self):
        self.add_entity_button.disconnect()
        self.edit_entity_button.disconnect()
        self.delete_entity_button.disconnect()
        self.save_changes_button.disconnect()
        self.view_demographics_button.disconnect()