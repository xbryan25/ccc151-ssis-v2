from PyQt6.QtCore import QAbstractTableModel, Qt

from utils.reset_sorting_state import ResetSortingState
from utils.get_existing_information import GetExistingInformation
from utils.is_valid_edit_value import IsValidEditValue

import operator, csv

# Where I discovered QTableView:
# https://stackoverflow.com/questions/6785481/how-to-implement-a-filter-option-in-qtablewidget

# MVC PyQT6 Tutorial: https://www.pythonguis.com/tutorials/modelview-architecture/
# https://www.pythonguis.com/tutorials/pyqt6-qtableview-modelviews-numpy-pandas/


class CustomTableModel(QAbstractTableModel):
    def __init__(self, data_from_csv, columns, information_type):
        super().__init__()

        self.has_changes = False

        self.data_from_csv = data_from_csv
        self.columns = columns
        self.information_type = information_type

        self.is_valid_edit_value = IsValidEditValue()

        if self.information_type == "students":
            self.students_information = GetExistingInformation.from_students(self.get_data())

        if self.information_type == "programs":
            self.programs_information = GetExistingInformation.from_programs(self.get_data())

        if self.information_type == "colleges":
            self.colleges_information = GetExistingInformation.from_colleges(self.get_data())

    def get_data(self):
        return self.data_from_csv

    def set_data(self, data_from_csv):
        self.data_from_csv = data_from_csv

    def set_has_changes(self, state):
        self.has_changes = state

    def get_has_changes(self):
        return self.has_changes

    # Override
    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
            return self.data_from_csv[index.row()][index.column()]

        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignCenter

    # Override
    def setData(self, index, value, role):
        # Current approach, read through file, put in list, modify list, write list in file
        valid = True

        if role == Qt.ItemDataRole.EditRole:
            old_value = self.data_from_csv[index.row()][index.column()]

            if self.information_type == "students":
                valid = self.is_valid_edit_value.for_students_cell(index, value,
                                                                   self.students_information["ID Number"],
                                                                   self.students_information["Full Name"],
                                                                   self.data_from_csv)

            elif self.information_type == "programs":
                valid = self.is_valid_edit_value.for_programs_cell(index, value,
                                                                   self.programs_information["Program Code"],
                                                                   self.programs_information["Program Name"])

            elif self.information_type == "colleges":
                valid = self.is_valid_edit_value.for_colleges_cell(index, value,
                                                                   self.colleges_information["College Code"],
                                                                   self.colleges_information["College Name"])

            if valid:
                # Edit the list of lists from the model
                if (self.information_type == "programs" and index.column() == 0) or (self.information_type == "programs" and index.column() == 0):
                    # Edit the list of lists from the model
                    self.data_from_csv[index.row()][index.column()] = value.upper()

                    # Edit the list from csv to be written
                    # data_from_database[index.row()][index.column()] = value.upper()

                else:
                    self.data_from_csv[index.row()][index.column()] = value
                    # data_from_database[index.row()][index.column()] = value

                if self.information_type == "students":
                    with open("../databases/students.csv", 'w', newline='') as from_students_csv:
                        writer = csv.writer(from_students_csv)

                        writer.writerows(self.data_from_csv)

                elif self.information_type == "programs":
                    with open("../databases/programs.csv", 'w', newline='') as from_programs_csv:
                        writer = csv.writer(from_programs_csv)

                        writer.writerows(self.data_from_csv)

                elif self.information_type == "colleges":
                    with open("../databases/colleges.csv", 'w', newline='') as from_colleges_csv:
                        writer = csv.writer(from_colleges_csv)

                        writer.writerows(self.data_from_csv)

                print("Overwritten")
            else:
                self.data_from_csv[index.row()][index.column()] = old_value
                print(old_value)

            return True

    # Override
    def rowCount(self, index=None):
        # The length of the outer list.
        return len(self.data_from_csv)

    # Override
    def columnCount(self, index=None):
        if not self.data_from_csv:
            return 0

        return len(self.data_from_csv[0])

    # Override
    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.columns[section]

        return super().headerData(section, orientation, role)

    # Override
    def flags(self, index):
        return Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
