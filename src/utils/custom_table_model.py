from PyQt6.QtCore import QAbstractTableModel, Qt, QTimer, QMetaObject

from utils.is_valid_edit_value_for_cell import IsValidEditValueForCell
from utils.specific_buttons_enabler import SpecificButtonsEnabler
from utils.table_view_page_controls import TableViewPageControls

from helper_dialogs.edit_item_state.fail_to_edit_item import FailToEditItemDialog
from helper_dialogs.edit_item_state.confirm_edit import ConfirmEditDialog
from helper_dialogs.edit_item_state.success_edit_item import SuccessEditItemDialog


# Where I discovered QTableView:
# https://stackoverflow.com/questions/6785481/how-to-implement-a-filter-option-in-qtablewidget

# MVC PyQT6 Tutorial: https://www.pythonguis.com/tutorials/modelview-architecture/
# https://www.pythonguis.com/tutorials/pyqt6-qtableview-modelviews-numpy-pandas/


class CustomTableModel(QAbstractTableModel):
    def __init__(self, information_type, db_handler):
        super().__init__()

        self.has_changes = False

        # Use when sorting filtered data
        self.data_is_currently_filtered = True

        self.data_from_db = []
        self.information_type = information_type
        self.db_handler = db_handler

        self.total_num = None

        self.current_page_number = 1

        # Arbitrary values, will just be updated
        self.max_row_per_page = 1
        self.max_pages = 1

        self.is_valid_edit_value = IsValidEditValueForCell()

        self.columns = []

        if self.information_type == "student":
            self.columns = ["ID Number", "First Name", "Last Name", "Year Level", "Gender", "Program Code"]

        if self.information_type == "program":
            self.columns = ["Program Code", "Program Name", "College Code"]
            self.students_data = []

        if self.information_type == "college":
            self.columns = ["College Code", "College Name"]
            self.students_data = []
            self.programs_data = []

        self.initialize_data()

        self.model_data_is_empty()

        self.is_loading = False

        self.save_button = None

    def model_data_is_empty(self):
        if not self.get_data():
            if self.information_type == "student":
                self.data_from_db.append(["", "", "", "", "", ""])
            elif self.information_type == "program":
                self.data_from_db.append(["", "", ""])
            elif self.information_type == "college":
                self.data_from_db.append(["", ""])

    def get_data(self):
        return self.data_from_db

    def set_data(self, data_from_db):
        self.data_from_db = data_from_db

    def set_has_changes(self, state):
        self.has_changes = state

    def get_has_changes(self):
        return self.has_changes

    def set_students_data(self, students_data):
        self.students_data = students_data

    def set_programs_data(self, programs_data):
        self.programs_data = programs_data

    def initialize_data(self):
        self.data_from_db = self.db_handler.get_all_entities(self.information_type)
        self.total_num = len(self.data_from_db)
        self.current_page_number = 1

    def update_page_view(self, table_view):
        self.max_row_per_page = TableViewPageControls.get_max_visible_rows(table_view)
        self.max_pages = (self.total_num // self.max_row_per_page) + 1

        # if self.current_page_number == 1:
        #     prev_button.setEnabled(False)
        # else:
        #     prev_button.setEnabled(True)
        #
        # if self.current_page_number == self.max_pages:
        #     next_button.setEnabled(False)
        # else:
        #     next_button.setEnabled(True)

        self.layoutChanged.emit()

    def update_after_search(self, row_count):
        print(row_count)

    def connect_to_save_button(self, save_button):
        self.save_button = save_button

    def len_of_students_under_program_code(self, old_program_code):
        length = 0

        for student in self.students_data:
            if student[5] == old_program_code:
                length += 1

        return length

    def edit_program_code_of_students(self, old_program_code, new_program_code):
        for student in self.students_data:
            if student[5] == old_program_code:
                student[5] = new_program_code

    def len_of_programs_under_college_code(self, old_college_code):
        length = 0

        for program in self.programs_data:
            if program[2] == old_college_code:
                length += 1

        return length

    def edit_college_code_of_programs(self, old_college_code, new_college_code):
        for program in self.programs_data:
            if program[2] == old_college_code:
                program[2] = new_college_code

    def add_entity(self, entity_to_add, entity_type):
        self.data_from_db.append(entity_to_add)
        self.db_handler.add_entity(entity_to_add, entity_type)

    def update_entity(self, identifier, entity_to_edit, entity_type, row_to_edit=None, edit_type="from_dialog"):

        if edit_type == "from_dialog":
            self.data_from_db[row_to_edit] = entity_to_edit

        # If edited 'from_model', no need to update the internal list

        self.db_handler.update_entity(identifier, entity_to_edit, entity_type)

    def delete_entity(self, entity_to_delete, entity_type):
        identifier = entity_to_delete[0]

        self.data_from_db.remove(entity_to_delete)

        self.model_data_is_empty()

        self.db_handler.delete_entity(identifier, entity_type)

    def search_entities(self, search_type, search_text):
        self.data_from_db = self.db_handler.search_entities(self.information_type, search_type, search_text)
        self.total_num = len(self.data_from_db)
        self.current_page_number = 1

        self.layoutChanged.emit()

    def sort_entities(self, sort_column, sort_order):
        if sort_order != "-":
            self.data_from_db = self.db_handler.get_sorted_entities(self.information_type, sort_column, sort_order)
            self.total_num = len(self.data_from_db)
            self.current_page_number = 1

            self.layoutChanged.emit()
        else:
            self.initialize_data()

    def set_next_page(self):
        if self.current_page_number + 1 <= self.max_pages:
            self.current_page_number += 1
            self.layoutChanged.emit()

    def set_previous_page(self):
        if self.current_page_number - 1 >= 1:
            self.current_page_number -= 1
            self.layoutChanged.emit()

    # Override
    def data(self, index, role):

        if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
            if index.row() < self.max_row_per_page and index.row() + ((self.current_page_number - 1) * self.max_row_per_page) < len(self.data_from_db):
                return self.data_from_db[index.row() + ((self.current_page_number - 1) * self.max_row_per_page)][
                    index.column()]

        if role == Qt.ItemDataRole.TextAlignmentRole:
            if index.row() < self.max_row_per_page:
                return Qt.AlignmentFlag.AlignCenter

    # Override
    def setData(self, index, value, role):
        # Current approach, read through file, put in list, modify list, write list in file
        valid = True
        issue = ""

        if role == Qt.ItemDataRole.EditRole:
            old_value = self.get_data()[index.row()][index.column()]

            if old_value == value:
                self.data_from_db[index.row()][index.column()] = old_value
                return True

            if self.information_type == "student":
                self.existing_students_information = self.db_handler.get_all_existing_students()

                valid, issue = self.is_valid_edit_value.for_students_cell(index, value,
                                                                            self.existing_students_information["ID Number"],
                                                                            self.existing_students_information["Full Name"],
                                                                            self.data_from_db)

            elif self.information_type == "program":
                self.existing_programs_information = self.db_handler.get_all_existing_programs()

                valid, issue = self.is_valid_edit_value.for_programs_cell(index, value,
                                                                            self.existing_programs_information["Program Code"],
                                                                            self.existing_programs_information["Program Name"])

            elif self.information_type == "college":
                self.existing_colleges_information = self.db_handler.get_all_existing_colleges()

                valid, issue = self.is_valid_edit_value.for_colleges_cell(index,
                                                                          value,
                                                                          self.existing_colleges_information["College Code"],
                                                                          self.existing_colleges_information["College Name"])

            if valid:
                # If program code is not changed, a different confirm edit dialog will show
                if ((self.information_type == "program" or self.information_type == "college")
                        and index.column() == 0 and old_value == value):

                    self.confirm_to_edit_dialog = ConfirmEditDialog(self.information_type,
                                                                    self.get_data()[index.row()][0])

                elif self.information_type == "program" and index.column() == 0  and old_value != value:
                    len_of_students_under_program_code = self.len_of_students_under_program_code(self.get_data()
                                                                                                 [index.row()][0])

                    self.confirm_to_edit_dialog = ConfirmEditDialog("program",
                                                                    old_value,
                                                                    num_of_affected=len_of_students_under_program_code,
                                                                    information_code_affected=True)

                elif self.information_type == "college" and index.column() == 0 and old_value != value:
                    len_of_programs_under_college_code = self.len_of_programs_under_college_code(self.get_data()
                                                                                                 [index.row()][0])

                    self.confirm_to_edit_dialog = ConfirmEditDialog("college",
                                                                    old_value,
                                                                    num_of_affected=len_of_programs_under_college_code,
                                                                    information_code_affected=True)
                else:
                    self.confirm_to_edit_dialog = ConfirmEditDialog(self.information_type, self.get_data()[index.row()][0])

                self.confirm_to_edit_dialog.exec()

                confirm_edit_decision = self.confirm_to_edit_dialog.get_confirm_edit_decision()

                if confirm_edit_decision:
                    # If program code is edited
                    if self.information_type == "program" and index.column() == 0:

                        old_program_code = self.get_data()[index.row()][0]

                        # Edit the list of lists from the model
                        self.data_from_db[index.row()][index.column()] = value.upper()

                        self.update_entity(old_program_code,
                                           self.data_from_db[index.row()],
                                           self.information_type,
                                           edit_type='from_model')

                        self.edit_program_code_of_students(old_program_code, self.get_data()[index.row()][0])

                    # If college code is edited
                    elif self.information_type == "college" and index.column() == 0:
                        old_college_code = self.get_data()[index.row()][0]

                        # Edit the list of lists from the model
                        self.data_from_db[index.row()][index.column()] = value.upper()

                        self.update_entity(old_college_code,
                                           self.data_from_db[index.row()],
                                           self.information_type,
                                           edit_type='from_model')

                        self.edit_college_code_of_programs(old_college_code, self.get_data()[index.row()][0])

                    # If everything else is edited
                    else:
                        identifier = self.data_from_db[index.row()][0]
                        self.data_from_db[index.row()][index.column()] = value

                        self.update_entity(identifier,
                                           self.data_from_db[index.row()],
                                           self.information_type,
                                           edit_type='from_model')

                    self.has_changes = True

                    SpecificButtonsEnabler.enable_save_button(self.save_button, self)

                    self.success_edit_item = SuccessEditItemDialog(self.information_type)
                    self.success_edit_item.exec()

                else:
                    return False

            else:
                self.data_from_db[index.row()][index.column()] = old_value

                if issue:
                    self.fail_to_edit_item_dialog = FailToEditItemDialog([issue], self.information_type)
                    self.fail_to_edit_item_dialog.exec()

            return True

    # Override
    def rowCount(self, index=None):
        # The length of the outer list.
        return self.max_row_per_page

    # Override
    def columnCount(self, index=None):
        if not self.data_from_db:
            return 0

        return len(self.data_from_db[0])

    # Override
    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:

            return self.columns[section]

        # print(self.columns)
        return super().headerData(section, orientation, role)

    # Override
    def flags(self, index):
        # Check if the first element of the empty string list is empty
        # If so, disable cells

        if self.get_data()[0][0] != "":
            return Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
        else:
            return Qt.ItemFlag.NoItemFlags
