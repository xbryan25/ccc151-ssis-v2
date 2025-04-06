from PyQt6.QtCore import QAbstractTableModel, Qt, QTimer, QMetaObject, QModelIndex

from utils.is_valid_edit_value_for_cell import IsValidEditValueForCell
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
        self.is_data_currently_filtered = False
        self.prev_search_type = None
        self.prev_search_text = None
        self.prev_sort_column = None
        self.prev_sort_order = None

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

        if self.information_type == "college":
            self.columns = ["College Code", "College Name"]

        self.initialize_data()

        self.model_data_is_empty()

        # self.save_button = None

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

    def get_is_data_currently_filtered(self):
        return self.is_data_currently_filtered

    def set_is_data_currently_filtered(self, is_data_currently_filtered):
        self.is_data_currently_filtered = is_data_currently_filtered

    def get_identifiers_of_selected_rows(self, selected_rows):
        actual_selected_rows = [(self.max_row_per_page * (self.current_page_number - 1)) + selected_row
                                for selected_row in selected_rows]

        return [row[0] for i, row in enumerate(self.get_data()) if i in actual_selected_rows]

    def reset_all_prev_search_and_sort_conditions(self):
        self.prev_search_type = None
        self.prev_search_text = None
        self.prev_sort_column = None
        self.prev_sort_order = None

    def initialize_data(self):
        self.data_from_db = self.db_handler.get_all_entities(self.information_type)
        self.total_num = len(self.data_from_db)
        self.current_page_number = 1

    def update_page_view(self, table_view):
        self.max_row_per_page = TableViewPageControls.get_max_visible_rows(table_view)
        self.max_pages = (self.total_num // self.max_row_per_page) + 1

        self.layoutChanged.emit()

    def add_entity(self, entity_to_add, entity_type):
        self.data_from_db.append(entity_to_add)
        self.db_handler.add_entity(entity_to_add, entity_type)

    def update_entity(self, entity_replacement, entity_type, actual_row_to_edit, edit_type="from_dialog",
                      edit_mode="single"):

        entity_to_edit = self.get_data()[actual_row_to_edit]

        identifier = entity_to_edit[0]

        if edit_mode == "multiple" and entity_type == "student":
            # Copy old values before replacing value in internal list
            entity_replacement[0] = self.data_from_db[actual_row_to_edit][0]
            entity_replacement[1] = self.data_from_db[actual_row_to_edit][1]
            entity_replacement[2] = self.data_from_db[actual_row_to_edit][2]

            if entity_replacement[3] == "--Select year level--":
                entity_replacement[3] = self.data_from_db[actual_row_to_edit][3]

            if entity_replacement[4] == "--Select gender--":
                entity_replacement[4] = self.data_from_db[actual_row_to_edit][4]

            if entity_replacement[5] == "--Select a program--":
                entity_replacement[5] = self.data_from_db[actual_row_to_edit][5]

        elif edit_mode == "multiple" and entity_type == "program":
            # Copy old values before replacing value in internal list
            entity_replacement[0] = self.data_from_db[actual_row_to_edit][0]
            entity_replacement[1] = self.data_from_db[actual_row_to_edit][1]

            if entity_replacement[2] == "--Select a college--":
                entity_replacement[2] = self.data_from_db[actual_row_to_edit][2]

        else:
            self.data_from_db[actual_row_to_edit] = entity_replacement

        # If edited 'from_model', no need to update the internal list

        self.db_handler.update_entity(identifier, self.data_from_db[actual_row_to_edit], entity_type)

    def delete_entity_from_db(self, entity_relative_row, entity_type):

        actual_row = (self.max_row_per_page * (self.current_page_number - 1)) + entity_relative_row
        entity_to_delete = self.get_data()[actual_row]

        identifier = entity_to_delete[0]

        # Delete from DB
        self.db_handler.delete_entity(identifier, entity_type)

        # # Delete from internal data structure of model
        # self.removeRow(actual_row)

    def update_data_from_db_after_deleting(self, selected_rows):

        actual_selected_rows = [(self.max_row_per_page * (self.current_page_number - 1)) + selected_row
                                for selected_row in selected_rows]

        self.beginResetModel()

        # Instead of deleting values one by one in self.data_from_db,
        # make another list that doesn't contain the affected rows and overwrite
        # self.data_from_db instead
        self.data_from_db = [row for i, row in enumerate(self.get_data()) if i not in actual_selected_rows]
        self.total_num = len(self.data_from_db)

        self.endResetModel()

        self.model_data_is_empty()

    def search_entities(self, search_type, search_text):

        self.data_from_db = self.db_handler.get_sorted_filtered_entities(self.information_type,
                                                                         self.prev_sort_column,
                                                                         self.prev_sort_order,
                                                                         search_type,
                                                                         search_text)

        self.total_num = len(self.data_from_db)
        self.current_page_number = 1

        self.model_data_is_empty()

        if search_text.strip() != "":
            self.is_data_currently_filtered = True
        else:
            self.is_data_currently_filtered = False

        self.prev_search_type = search_type
        self.prev_search_text = search_text

        self.layoutChanged.emit()

    def sort_filtered_entities(self, sort_column, sort_order):
        if sort_order != "-":
            self.data_from_db = self.db_handler.get_sorted_filtered_entities(self.information_type,
                                                                             sort_column,
                                                                             sort_order,
                                                                             self.prev_search_type,
                                                                             self.prev_search_text)

            self.total_num = len(self.data_from_db)
            self.current_page_number = 1

            self.layoutChanged.emit()
        else:
            self.initialize_data()

        self.prev_sort_column = sort_column
        self.prev_sort_order = sort_order

    def sort_entities(self, sort_column, sort_order):
        if sort_order != "-":
            self.data_from_db = self.db_handler.get_sorted_entities(self.information_type, sort_column, sort_order)
            self.total_num = len(self.data_from_db)
            self.current_page_number = 1

            self.layoutChanged.emit()
        else:
            self.initialize_data()

        self.prev_sort_column = sort_column
        self.prev_sort_order = sort_order

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
            else:
                return None

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
                    len_of_students_under_program_code = len(
                        self.db_handler.get_programs_and_students_connections()[self.get_data()][index.row()][0])



                    self.confirm_to_edit_dialog = ConfirmEditDialog("program",
                                                                    old_value,
                                                                    num_of_affected=len_of_students_under_program_code,
                                                                    information_code_affected=True)

                elif self.information_type == "college" and index.column() == 0 and old_value != value:

                    len_of_programs_under_college_code = len(
                        self.db_handler.get_colleges_and_programs_connections()[self.get_data()][index.row()][0])

                    self.confirm_to_edit_dialog = ConfirmEditDialog("college",
                                                                    old_value,
                                                                    num_of_affected=len_of_programs_under_college_code,
                                                                    information_code_affected=True)
                else:
                    self.confirm_to_edit_dialog = ConfirmEditDialog(self.information_type, self.get_data()[index.row()][0])

                self.confirm_to_edit_dialog.exec()

                confirm_edit_decision = self.confirm_to_edit_dialog.get_confirm_edit_decision()

                if confirm_edit_decision:

                    temp_list = list(self.data_from_db[index.row()])

                    # If program code is edited
                    if self.information_type == "program" and index.column() == 0:
                        # Edit the list of lists from the model
                        temp_list[index.column()] = value.upper()

                        # self.edit_program_code_of_students(old_program_code, self.get_data()[index.row()][0])

                    # If college code is edited
                    elif self.information_type == "college" and index.column() == 0:
                        # Edit the list of lists from the model
                        temp_list[index.column()] = value.upper()

                        # self.edit_college_code_of_programs(old_college_code, self.get_data()[index.row()][0])

                    # If everything else is edited
                    else:
                        temp_list[index.column()] = value

                    self.update_entity(temp_list,
                                       self.information_type,
                                       actual_row_to_edit=index.row(),
                                       edit_type='from_model')

                    self.success_edit_item = SuccessEditItemDialog(self.information_type, [self.data_from_db[index.row()][0]])
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

        if (self.current_page_number == 1 or self.current_page_number < self.max_pages) and len(self.get_data()) > self.max_row_per_page:
            return self.max_row_per_page

        else:

            current_page_row_count = len(self.data_from_db) % self.max_row_per_page

            return current_page_row_count

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
