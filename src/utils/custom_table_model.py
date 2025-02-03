from PyQt6.QtCore import QAbstractTableModel, Qt

from utils.reset_sorting_state import ResetSortingState
from utils.get_existing_information import GetExistingInformation

import operator, csv

# Where I discovered QTableView:
# https://stackoverflow.com/questions/6785481/how-to-implement-a-filter-option-in-qtablewidget

# MVC PyQT6 Tutorial: https://www.pythonguis.com/tutorials/modelview-architecture/
# https://www.pythonguis.com/tutorials/pyqt6-qtableview-modelviews-numpy-pandas/


class CustomTableModel(QAbstractTableModel):
    def __init__(self, data_from_csv, columns, information_type):
        super().__init__()

        self.data_from_csv = data_from_csv
        self.columns = columns
        self.information_type = information_type

        if self.information_type == "students":
            self.students_information = GetExistingInformation.from_students()

        if self.information_type == "programs":
            self.programs_information = GetExistingInformation.from_programs()

        if self.information_type == "colleges":
            self.colleges_information = GetExistingInformation.from_colleges()

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
            return self.data_from_csv[index.row()][index.column()]

        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignCenter

    def setData(self, index, value, role):
        # Current approach, read through file, put in list, modify list, write list in file
        has_issues = False

        get_index = index

        if role == Qt.ItemDataRole.EditRole:
            old_value = self.data_from_csv[index.row()][index.column()]
            data_from_database = []

            if self.information_type == "students":
                with open("databases/students.csv", 'r') as from_students_csv:
                    reader = csv.reader(from_students_csv)

                    for row in reader:
                        data_from_database.append(row)

                has_issues = self.is_valid_edit_value_for_students(index, value)

            elif self.information_type == "programs":
                with open("databases/programs.csv", 'r') as from_programs_csv:
                    reader = csv.reader(from_programs_csv)

                    for row in reader:
                        data_from_database.append(row)

                has_issues = self.is_valid_edit_value_for_programs(index, value)

            elif self.information_type == "colleges":
                with open("databases/colleges.csv", 'r') as from_colleges_csv:
                    reader = csv.reader(from_colleges_csv)

                    for row in reader:
                        data_from_database.append(row)

                has_issues = self.is_valid_edit_value_for_colleges(index, value)

            if not has_issues:
                # Edit the list of lists from the model
                if (self.information_type == "programs" and index.column() == 0) or (self.information_type == "programs" and index.column() == 0):
                    # Edit the list of lists from the model
                    self.data_from_csv[index.row()][index.column()] = value.upper()

                    # Edit the list from csv to be written
                    data_from_database[index.row()][index.column()] = value.upper()

                else:
                    self.data_from_csv[index.row()][index.column()] = value
                    data_from_database[index.row()][index.column()] = value

                if self.information_type == "students":
                    with open("databases/students.csv", 'w', newline='') as from_students_csv:
                        writer = csv.writer(from_students_csv)

                        writer.writerows(data_from_database)

                elif self.information_type == "programs":
                    with open("databases/programs.csv", 'w', newline='') as from_programs_csv:
                        writer = csv.writer(from_programs_csv)

                        writer.writerows(data_from_database)

                elif self.information_type == "colleges":
                    with open("databases/colleges.csv", 'w', newline='') as from_colleges_csv:
                        writer = csv.writer(from_colleges_csv)

                        writer.writerows(data_from_database)

                print("Overwritten")
            else:
                self.data_from_csv[index.row()][index.column()] = old_value
                print(old_value)

            return True

    def is_valid_edit_value_for_students(self, index, value):
        has_issues = False

        if index.column() == 0 and value.strip() in self.students_information["ID Number"]:
            print("ID already exists")
            has_issues = True

        if index.column() == 1 and f"{value.strip()} {self.data_from_csv[index.row()][index.column() + 1]}" in \
                self.students_information["Full Name"]:
            print("Name combination exists")
            has_issues = True

        if index.column() == 2 and f"{self.data_from_csv[index.row()][index.column() - 1]} {value.strip()}" in \
                self.students_information["Full Name"]:
            print("Name combination exists")
            has_issues = True

        if index.column() == 3 and value.strip() not in ["1st", "2nd", "3rd", "4th", "5th"]:
            print("Not valid year level")
            has_issues = True

        if index.column() == 4 and value.strip() not in ["Male", "Female", "Others", "Prefer not to say"]:
            print("Not valid gender")
            has_issues = True

        return has_issues

    def is_valid_edit_value_for_programs(self, index, value):
        has_issues = False

        if index.column() == 0 and value.strip().upper() in self.programs_information["Program Code"]:
            print("Program code already exists")
            has_issues = True

        if index.column() == 1 and value.strip() in self.programs_information["Program Name"]:
            print("Program name already exists")
            has_issues = True

        return has_issues

    def is_valid_edit_value_for_colleges(self, index, value):
        has_issues = False

        if index.column() == 0 and value.strip().upper() in self.colleges_information["College Code"]:
            print("College code already exists")
            has_issues = True

        if index.column() == 1 and value.strip() in self.colleges_information["College Name"]:
            print("College name already exists")
            has_issues = True

        return has_issues

    def rowCount(self, index=None):
        # The length of the outer list.
        return len(self.data_from_csv)

    def columnCount(self, index=None):
        if not self.data_from_csv:
            return 0

        return len(self.data_from_csv[0])

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.columns[section]

        return super().headerData(section, orientation, role)

    def flags(self, index):
        return Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
