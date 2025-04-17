from PyQt6.QtWidgets import QHeaderView

from utils.combobox_item_delegate import ComboboxItemDelegate

# For the comboboxes in the student and program tables


class ResetItemDelegates:

    def __init__(self, application_window):

        self.aw = application_window

    def load_item_delegates_for_students_table_view(self):

        # For Year Level
        self.year_level_delegate = ComboboxItemDelegate(self.aw.students_table_view,
                                                        ["1st", "2nd", "3rd",
                                                         "4th", "5th"])

        self.aw.students_table_view.setItemDelegateForColumn(3, self.year_level_delegate)

        # For Gender
        self.gender_delegate = ComboboxItemDelegate(self.aw.students_table_view,
                                                    ["Male", "Female", "Others",
                                                     "Prefer not to say"])

        self.aw.students_table_view.setItemDelegateForColumn(4, self.gender_delegate)

        # For Program Codes
        self.program_code_delegate = ComboboxItemDelegate(self.aw.students_table_view, self.get_program_codes())

        self.aw.students_table_view.setItemDelegateForColumn(5, self.program_code_delegate)

    def load_item_delegates_for_programs_table_view(self):

        # For College Codes
        self.program_code_delegate = ComboboxItemDelegate(self.aw.programs_table_view, self.get_college_codes())

        self.aw.programs_table_view.setItemDelegateForColumn(2, self.program_code_delegate)

    def show_combobox_delegate_students_table_view(self, index):
        self.aw.students_table_view.edit(index)

    def show_combobox_delegate_programs_table_view(self, index):
        self.aw.programs_table_view.edit(index)

    # Dynamic change of combobox
    # https://www.pythonguis.com/faq/how-to-clear-remove-combobox-delegate-data-from-qtableview/

    def reset(self, state=None):

        if state in ["student", "add_student", "delete_student", "edit_student"]:
            self.aw.students_sort_filter_proxy_model.beginResetModel()
            self.aw.students_sort_filter_proxy_model.endResetModel()

            self.aw.students_table_horizontal_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
            self.aw.students_table_horizontal_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            self.aw.students_table_horizontal_header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
            self.aw.students_table_horizontal_header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
            self.aw.students_table_horizontal_header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
            self.aw.students_table_horizontal_header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)

        elif state in ["program", "add_program", "delete_program", "edit_program"]:
            self.aw.programs_sort_filter_proxy_model.beginResetModel()
            self.aw.programs_sort_filter_proxy_model.endResetModel()

            self.aw.students_table_horizontal_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
            self.aw.students_table_horizontal_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            self.aw.students_table_horizontal_header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
            self.aw.students_table_horizontal_header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
            self.aw.students_table_horizontal_header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
            self.aw.students_table_horizontal_header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)

            self.aw.programs_table_horizontal_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
            self.aw.programs_table_horizontal_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            self.aw.programs_table_horizontal_header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)

        elif state in ["add_college", "delete_college", "edit_college"]:
            self.aw.colleges_sort_filter_proxy_model.beginResetModel()
            self.aw.colleges_sort_filter_proxy_model.endResetModel()

            self.aw.students_table_horizontal_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
            self.aw.students_table_horizontal_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            self.aw.students_table_horizontal_header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
            self.aw.students_table_horizontal_header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
            self.aw.students_table_horizontal_header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
            self.aw.students_table_horizontal_header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)

            self.aw.programs_table_horizontal_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
            self.aw.programs_table_horizontal_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            self.aw.programs_table_horizontal_header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)

            self.aw.colleges_table_horizontal_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
            self.aw.colleges_table_horizontal_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

    def get_program_codes(self):
        return self.aw.database_handler.get_all_entity_information_codes('program')

    def get_college_codes(self):
        return self.aw.database_handler.get_all_entity_information_codes('college')
