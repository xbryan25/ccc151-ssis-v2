from PyQt6.QtWidgets import QHeaderView

from utils.combobox_item_delegate import ComboboxItemDelegate
from utils.get_information_codes import GetInformationCodes

# For the comboboxes in the student and program tables


class ResetItemDelegates:

    def __init__(self, reset_item_delegates_elements):

        self.students_table_view = reset_item_delegates_elements[0]
        self.programs_table_view = reset_item_delegates_elements[1]
        self.colleges_table_view = reset_item_delegates_elements[2]

        self.students_table_view_header = self.students_table_view.horizontalHeader()
        self.programs_table_view_header = self.programs_table_view.horizontalHeader()
        self.colleges_table_view_header = self.colleges_table_view.horizontalHeader()

        self.students_table_model = reset_item_delegates_elements[3]
        self.programs_table_model = reset_item_delegates_elements[4]

        self.students_sort_filter_proxy_model = reset_item_delegates_elements[5]
        self.programs_sort_filter_proxy_model = reset_item_delegates_elements[6]
        self.colleges_sort_filter_proxy_model = reset_item_delegates_elements[7]

        self.colleges_table_model = reset_item_delegates_elements[8]


    # Dynamic change of combobox
    # https://www.pythonguis.com/faq/how-to-clear-remove-combobox-delegate-data-from-qtableview/

    def reset(self, state=None):

        if state in ["student", "add_student", "delete_student", "edit_student"]:
            self.students_sort_filter_proxy_model.beginResetModel()
            self.students_sort_filter_proxy_model.endResetModel()

            self.students_table_view_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
            self.students_table_view_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            self.students_table_view_header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
            self.students_table_view_header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
            self.students_table_view_header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
            self.students_table_view_header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)

            self.load_item_delegates_program_codes()
            self.load_item_delegates_year_and_gender()

        elif state in ["program", "add_program", "delete_program", "edit_program"]:
            self.programs_sort_filter_proxy_model.beginResetModel()
            self.programs_sort_filter_proxy_model.endResetModel()

            self.students_table_view_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
            self.students_table_view_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            self.students_table_view_header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
            self.students_table_view_header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
            self.students_table_view_header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
            self.students_table_view_header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)

            self.programs_table_view_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
            self.programs_table_view_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            self.programs_table_view_header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)

            self.load_item_delegates_college_codes()

        elif state in ["add_college", "delete_college", "edit_college"]:
            self.colleges_sort_filter_proxy_model.beginResetModel()
            self.colleges_sort_filter_proxy_model.endResetModel()

            self.students_table_view_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
            self.students_table_view_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            self.students_table_view_header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
            self.students_table_view_header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
            self.students_table_view_header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
            self.students_table_view_header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)

            self.programs_table_view_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
            self.programs_table_view_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            self.programs_table_view_header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)

            self.colleges_table_view_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
            self.colleges_table_view_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)


    def load_item_delegates_year_and_gender(self):
        # Check if self.students_table_model is empty, if so, disable combobox item delegate

        if self.students_table_model.get_data()[0][3] != "" and self.students_table_model.get_data()[0][4] != "":
            # For Year Level
            self.students_table_view.setItemDelegateForColumn(3, ComboboxItemDelegate(self.students_table_view,
                                                                                      ["1st", "2nd", "3rd",
                                                                                       "4th", "5th"]))
            for row in range(0, self.students_sort_filter_proxy_model.rowCount()):
                self.students_table_view.openPersistentEditor(self.students_sort_filter_proxy_model.index(row, 3))

            # For Gender
            self.students_table_view.setItemDelegateForColumn(4, ComboboxItemDelegate(self.students_table_view,
                                                                                      ["Male", "Female", "Others",
                                                                                       "Prefer not to say"]))

            for row in range(0, self.students_sort_filter_proxy_model.rowCount()):
                self.students_table_view.openPersistentEditor(self.students_sort_filter_proxy_model.index(row, 4))

    def load_item_delegates_program_codes(self):
        # Check if self.students_table_model is empty, if so, disable combobox item delegate

        if self.students_table_model.get_data()[0][5] != "":
            # For Program Codes

            combobox_item_delegate = ComboboxItemDelegate(self.students_table_view, self.get_program_codes())

            self.students_table_view.setItemDelegateForColumn(5, combobox_item_delegate)

            for row in range(0, self.students_sort_filter_proxy_model.rowCount()):
                self.students_table_view.openPersistentEditor(self.students_sort_filter_proxy_model.index(row, 5))

    def load_item_delegates_college_codes(self):

        # Check if self.programs_table_model is empty, if so, disable combobox item delegate

        if self.programs_table_model.get_data()[0][2] != "":
            # For College Codes

            combobox_item_delegate = ComboboxItemDelegate(self.programs_table_view, self.get_college_codes())

            self.programs_table_view.setItemDelegateForColumn(2, combobox_item_delegate)

            for row in range(0, self.programs_sort_filter_proxy_model.rowCount()):
                self.programs_table_view.openPersistentEditor(self.programs_sort_filter_proxy_model.index(row, 2))

    def get_program_codes(self):
        return GetInformationCodes.for_programs(self.programs_table_model.get_data())

    def get_college_codes(self):
        return GetInformationCodes.for_colleges(self.colleges_table_model.get_data())
