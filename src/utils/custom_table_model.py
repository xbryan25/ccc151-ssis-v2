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
        self.mode = "viewer"

        self.sort_type_combobox = None
        self.search_input_lineedit = None

        # Use when sorting filtered data
        self.is_data_currently_filtered = False
        self.is_data_currently_sorted = False

        self.prev_search_type = None
        self.prev_search_method = None
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

        self.set_total_num()
        self.initialize_data()

        self.model_data_is_empty()

    def get_data(self):
        return self.data_from_db

    def set_data(self, data_from_db):
        self.data_from_db = data_from_db

    def set_mode(self, mode):
        self.mode = mode

    def set_has_changes(self, state):
        self.has_changes = state

    def get_has_changes(self):
        return self.has_changes

    def get_is_data_currently_filtered(self):
        return self.is_data_currently_filtered

    def set_is_data_currently_filtered(self, is_data_currently_filtered):
        self.is_data_currently_filtered = is_data_currently_filtered

    def get_is_data_currently_sorted(self):
        return self.is_data_currently_sorted

    def set_is_data_currently_sorted(self, is_data_currently_sorted):
        self.is_data_currently_sorted = is_data_currently_sorted

    def model_data_is_empty(self):
        if not self.get_data():

            self.beginResetModel()

            if self.information_type == "student":
                self.data_from_db.append(["", "", "", "", "", ""])
            elif self.information_type == "program":
                self.data_from_db.append(["", "", ""])
            elif self.information_type == "college":
                self.data_from_db.append(["", ""])

            self.total_num = 1
            self.endResetModel()

    def get_identifiers_of_selected_rows(self, selected_rows):

        return [row[0] for i, row in enumerate(self.get_data()) if i in selected_rows]

    def set_search_and_sort_fields(self, sort_order_combobox, search_input_lineedit):
        self.sort_order_combobox = sort_order_combobox
        self.search_input_lineedit = search_input_lineedit

    def set_total_num(self):
        self.total_num = self.db_handler.get_count_of_all_entities(self.information_type)

    def get_total_num(self):
        return self.total_num

    def set_max_row_per_page(self, max_row_per_page):
        self.max_row_per_page = max_row_per_page

    def reset_search_and_sort_fields(self):
        if self.sort_order_combobox and self.search_input_lineedit:
            self.sort_order_combobox.setCurrentIndex(0)
            self.search_input_lineedit.setText("")

    def reset_all_prev_search_and_sort_conditions(self):
        self.prev_search_type = None
        self.prev_search_method = None
        self.prev_search_text = None
        self.prev_sort_column = None
        self.prev_sort_order = None

    def initialize_data(self):

        self.beginResetModel()

        self.data_from_db = self.db_handler.get_entities(self.max_row_per_page, self.current_page_number, self.information_type)

        self.max_pages = (self.total_num + self.max_row_per_page - 1) // self.max_row_per_page

        self.endResetModel()

        self.layoutChanged.emit()

    def update_page_view(self, table_view):
        new_max_row_per_page = max(1, TableViewPageControls.get_max_visible_rows(table_view))

        # Only refresh data when new_max_row_per_page is different from self.max_row_per_page
        if self.max_row_per_page != new_max_row_per_page:
            self.max_row_per_page = new_max_row_per_page
            self.max_pages = (self.total_num + self.max_row_per_page - 1) // self.max_row_per_page

            if self.current_page_number > self.max_pages:
                self.current_page_number = self.max_pages

            self.initialize_data()

    def add_entity(self, entity_to_add, entity_type):
        # Add data to database (although it is only staged)
        self.db_handler.add_entity(entity_to_add, entity_type)

        # Then select all students from database
        # This ensures that the added student will be sorted
        self.initialize_data()

        self.reset_search_and_sort_fields()

    def update_entity(self, entity_replacement, entity_type, row_to_edit, edit_mode="single"):

        entity_to_edit = self.get_data()[row_to_edit]

        identifier = entity_to_edit[0]

        if edit_mode == "multiple" and entity_type == "student":
            # Copy old values before replacing value in internal list
            entity_replacement[0] = self.data_from_db[row_to_edit][0]
            entity_replacement[1] = self.data_from_db[row_to_edit][1]
            entity_replacement[2] = self.data_from_db[row_to_edit][2]

            if entity_replacement[3] == "--Select year level--":
                entity_replacement[3] = self.data_from_db[row_to_edit][3]

            if entity_replacement[4] == "--Select gender--":
                entity_replacement[4] = self.data_from_db[row_to_edit][4]

            if entity_replacement[5] == "--Select a program--":
                entity_replacement[5] = self.data_from_db[row_to_edit][5]

        elif edit_mode == "multiple" and entity_type == "program":
            # Copy old values before replacing value in internal list
            entity_replacement[0] = self.data_from_db[row_to_edit][0]
            entity_replacement[1] = self.data_from_db[row_to_edit][1]

            if entity_replacement[2] == "--Select a college--":
                entity_replacement[2] = self.data_from_db[row_to_edit][2]

        self.data_from_db[row_to_edit] = entity_replacement

        top_left = self.index(row_to_edit, 0)
        bottom_right = self.index(row_to_edit, self.columnCount())
        self.dataChanged.emit(top_left, bottom_right, [Qt.ItemDataRole.DisplayRole])

        # If edited 'from_model', no need to update the internal list

        self.db_handler.update_entity(identifier, self.data_from_db[row_to_edit], entity_type)

        # Then select all students from database
        # This ensures that the edit student will be sorted
        self.initialize_data()

        self.reset_search_and_sort_fields()

    def delete_entity_from_db(self, entity_relative_row, entity_type):
        # This method deletes entities from the database

        entity_to_delete = self.get_data()[entity_relative_row]

        identifier = entity_to_delete[0]

        # Delete from DB
        self.db_handler.delete_entity(identifier, entity_type)

    def search_entities(self, search_type, search_method, search_text):
        # Connected to self.sort_filtered_entities()

        if search_text.strip() != "":
            self.is_data_currently_filtered = True

            self.total_num = self.db_handler.get_count_of_sorted_filtered_entities(self.information_type,
                                                                                   search_type,
                                                                                   search_method,
                                                                                   search_text)

            self.beginResetModel()

            self.data_from_db = self.db_handler.get_sorted_filtered_entities(self.max_row_per_page,
                                                                             self.current_page_number,
                                                                             self.information_type,
                                                                             self.prev_sort_column,
                                                                             self.prev_sort_order,
                                                                             search_type,
                                                                             search_method,
                                                                             search_text)

            self.max_pages = (self.total_num + self.max_row_per_page - 1) // self.max_row_per_page

            self.endResetModel()

            self.model_data_is_empty()

        else:
            self.is_data_currently_filtered = False

            self.set_total_num()
            self.initialize_data()

        self.prev_search_type = search_type
        self.prev_search_method = search_method
        self.prev_search_text = search_text

        self.layoutChanged.emit()
        self.dataChanged.emit(self.index(0, 0), self.index(self.rowCount() - 1, self.columnCount() - 1))

    def sort_filtered_entities(self, sort_column, sort_order):
        # Connected to self.search_entities()

        print("Yo")

        self.beginResetModel()

        self.data_from_db = self.db_handler.get_sorted_filtered_entities(self.max_row_per_page,
                                                                         self.current_page_number,
                                                                         self.information_type,
                                                                         sort_column,
                                                                         sort_order,
                                                                         self.prev_search_type,
                                                                         self.prev_search_method,
                                                                         self.prev_search_text)

        self.endResetModel()

        if sort_order != "-":
            self.is_data_currently_sorted = True

        else:
            self.is_data_currently_sorted = False

        self.layoutChanged.emit()

        self.prev_sort_column = sort_column
        self.prev_sort_order = sort_order

    def sort_entities(self, sort_column, sort_order):
        if sort_order != "-":

            self.beginResetModel()
            self.data_from_db = self.db_handler.get_sorted_entities(self.max_row_per_page,
                                                                    self.current_page_number,
                                                                    self.information_type,
                                                                    sort_column,
                                                                    sort_order)
            self.endResetModel()

            # self.total_num = len(self.data_from_db)
            # self.current_page_number = 1

            self.layoutChanged.emit()

            self.is_data_currently_sorted = True
        else:
            self.initialize_data()

            self.is_data_currently_sorted = False

        self.prev_sort_column = sort_column
        self.prev_sort_order = sort_order

    def set_specific_page(self, page_number, current_page_lineedit, previous_page_button, next_page_button):

        if page_number < 1:
            self.current_page_number = 1
            previous_page_button.setEnabled(False)
            #
            # current_page_lineedit.blockSignals(True)
            # current_page_lineedit.setText("1")
            # current_page_lineedit.blockSignals(False)

        elif page_number == 1:
            self.current_page_number = 1
            previous_page_button.setEnabled(False)

            current_page_lineedit.blockSignals(True)
            current_page_lineedit.setText("1")
            current_page_lineedit.blockSignals(False)

        elif page_number >= self.max_pages:
            self.current_page_number = self.max_pages
            next_page_button.setEnabled(False)

            current_page_lineedit.blockSignals(True)
            current_page_lineedit.setText(f"{self.max_pages}")
            current_page_lineedit.blockSignals(False)
        else:
            self.current_page_number = page_number

            previous_page_button.setEnabled(True)
            next_page_button.setEnabled(True)

        if self.get_is_data_currently_filtered():
            self.search_entities(self.prev_search_type, self.prev_search_method, self.prev_search_text)
        elif self.get_is_data_currently_sorted():
            self.sort_entities(self.prev_sort_column, self.prev_sort_order)
        else:
            self.initialize_data()

    def set_next_page(self, previous_page_button, next_page_button):
        if self.current_page_number + 1 <= self.max_pages:
            previous_page_button.setEnabled(True)

            self.current_page_number += 1

            if self.get_is_data_currently_filtered():
                self.search_entities(self.prev_search_type, self.prev_search_method, self.prev_search_text)
            elif self.get_is_data_currently_sorted():
                self.sort_entities(self.prev_sort_column, self.prev_sort_order)
            else:
                self.initialize_data()

        if self.current_page_number == self.max_pages:
            next_page_button.setEnabled(False)

    def set_previous_page(self, previous_page_button, next_page_button):
        if self.current_page_number - 1 >= 1:
            next_page_button.setEnabled(True)

            self.current_page_number -= 1

            if self.get_is_data_currently_filtered() and self.get_is_data_currently_sorted():
                self.search_entities(self.prev_search_type, self.prev_search_method, self.prev_search_text)
            elif self.get_is_data_currently_sorted():
                self.sort_entities(self.prev_sort_column, self.prev_sort_order)
            else:
                self.initialize_data()

        if self.current_page_number == 1:
            previous_page_button.setEnabled(False)

    # Override
    def data(self, index, role):

        if not index.isValid():
            return None

        if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
            return self.data_from_db[index.row()][index.column()]

        if role == Qt.ItemDataRole.TextAlignmentRole:
            if index.row() < self.max_row_per_page:
                return Qt.AlignmentFlag.AlignCenter

        return None

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
                # self.existing_students_information = self.db_handler.get_all_existing_students()

                valid, issue = self.is_valid_edit_value.for_students_cell(index,
                                                                          value,
                                                                          self.db_handler,
                                                                          self.data_from_db)

            elif self.information_type == "program":

                valid, issue = self.is_valid_edit_value.for_programs_cell(index,
                                                                          value,
                                                                          self.db_handler)

            elif self.information_type == "college":
                valid, issue = self.is_valid_edit_value.for_colleges_cell(index,
                                                                          value,
                                                                          self.db_handler)

            if valid:
                # If program code is not changed, a different confirm edit dialog will show
                # if ((self.information_type == "program" or self.information_type == "college")
                #         and index.column() == 0 and old_value == value):
                #
                #     self.confirm_to_edit_dialog = ConfirmEditDialog(self.information_type,
                #                                                     [self.get_data()[index.row()][0]])

                if self.information_type == "program" and index.column() == 0 and old_value != value:
                    len_of_students_under_program_code = self.db_handler.get_count_of_all_students_in_program(self.get_data()[index.row()][0])

                    self.confirm_to_edit_dialog = ConfirmEditDialog("program",
                                                                    [old_value],
                                                                    num_of_affected=len_of_students_under_program_code,
                                                                    entity_code_affected=True)

                elif self.information_type == "college" and index.column() == 0 and old_value != value:
                    len_of_programs_under_college_code = self.db_handler.get_count_of_all_programs_in_college(self.get_data()[index.row()][0])

                    self.confirm_to_edit_dialog = ConfirmEditDialog("college",
                                                                    [old_value],
                                                                    num_of_affected=len_of_programs_under_college_code,
                                                                    entity_code_affected=True)
                else:
                    self.confirm_to_edit_dialog = ConfirmEditDialog(self.information_type, [self.get_data()[index.row()][0]])

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
                                       row_to_edit=index.row())

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
        return len(self.data_from_db)

        # total_rows = len(self.data_from_db)
        #
        # # If the current page is not the last page, return max rows per page
        # if self.current_page_number == 1 or self.current_page_number < self.max_pages:
        #     return min(self.max_row_per_page, total_rows)
        #
        # # For the last page, calculate the number of remaining rows
        # remaining_rows = total_rows % self.max_row_per_page
        # if remaining_rows == 0:  # If the last page is full
        #     return self.max_row_per_page
        # else:
        #     return remaining_rows

    # Override
    def columnCount(self, index=None):
        if not self.data_from_db:
            return 0

        return len(self.data_from_db[0])

    # Override
    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:

            return self.columns[section]

        return super().headerData(section, orientation, role)

    # Override
    def flags(self, index):
        # Check if the first element of the empty string list is empty
        # If so, disable cells

        first_element_of_data = self.get_data()[0][0]

        if first_element_of_data != "" and self.mode == "admin":
            return Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
        elif first_element_of_data != "" and self.mode == "viewer":
            return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
        else:
            return Qt.ItemFlag.NoItemFlags
