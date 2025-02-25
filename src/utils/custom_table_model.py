from PyQt6.QtCore import QAbstractTableModel, Qt

from utils.get_existing_information import GetExistingInformation
from utils.is_valid_edit_value_for_cell import IsValidEditValueForCell
from utils.specific_buttons_enabler import SpecificButtonsEnabler

from helper_dialogs.edit_item_state.fail_to_edit_item import FailToEditItemDialog
from helper_dialogs.edit_item_state.confirm_edit import ConfirmEditDialog
from helper_dialogs.edit_item_state.success_edit_item import SuccessEditItemDialog


# Where I discovered QTableView:
# https://stackoverflow.com/questions/6785481/how-to-implement-a-filter-option-in-qtablewidget

# MVC PyQT6 Tutorial: https://www.pythonguis.com/tutorials/modelview-architecture/
# https://www.pythonguis.com/tutorials/pyqt6-qtableview-modelviews-numpy-pandas/


class CustomTableModel(QAbstractTableModel):
    def __init__(self, data_from_csv, information_type):
        super().__init__()

        self.has_changes = False

        self.data_from_csv = data_from_csv
        self.information_type = information_type

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

        self.model_data_is_empty()

        self.save_button = None

    def model_data_is_empty(self):
        if not self.get_data():
            if self.information_type == "student":
                self.data_from_csv.append(["", "", "", "", "", ""])
            elif self.information_type == "program":
                self.data_from_csv.append(["", "", ""])
            elif self.information_type == "college":
                self.data_from_csv.append(["", ""])

    def get_data(self):
        return self.data_from_csv

    def set_data(self, data_from_csv):
        self.data_from_csv = data_from_csv

    def set_has_changes(self, state):
        self.has_changes = state

    def get_has_changes(self):
        return self.has_changes

    def set_students_data(self, students_data):
        self.students_data = students_data

    def set_programs_data(self, programs_data):
        self.programs_data = programs_data

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
        issue = ""

        if role == Qt.ItemDataRole.EditRole:
            old_value = self.get_data()[index.row()][index.column()]

            print(old_value)

            if self.information_type == "student":
                self.students_information = GetExistingInformation.from_students(self.get_data())

                valid, issue = self.is_valid_edit_value.for_students_cell(index, value,
                                                                            self.students_information["ID Number"],
                                                                            self.students_information["Full Name"],
                                                                            self.data_from_csv)

            elif self.information_type == "program":
                self.programs_information = GetExistingInformation.from_programs(self.get_data())

                valid, issue = self.is_valid_edit_value.for_programs_cell(index, value,
                                                                            self.programs_information["Program Code"],
                                                                            self.programs_information["Program Name"])

            elif self.information_type == "college":
                self.colleges_information = GetExistingInformation.from_colleges(self.get_data())

                valid, issue = self.is_valid_edit_value.for_colleges_cell(index, value,
                                                                            self.colleges_information["College Code"],
                                                                            self.colleges_information["College Name"])

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
                    if self.information_type == "program" and index.column() == 0:

                        old_program_code = self.get_data()[index.row()][0]

                        # Edit the list of lists from the model
                        self.data_from_csv[index.row()][index.column()] = value.upper()

                        self.edit_program_code_of_students(old_program_code, self.get_data()[index.row()][0])

                    elif self.information_type == "college" and index.column() == 0:
                        old_college_code = self.get_data()[index.row()][0]

                        # Edit the list of lists from the model
                        self.data_from_csv[index.row()][index.column()] = value.upper()

                        self.edit_college_code_of_programs(old_college_code, self.get_data()[index.row()][0])

                    else:
                        self.data_from_csv[index.row()][index.column()] = value

                    self.has_changes = True

                    SpecificButtonsEnabler.enable_save_button(self.save_button, self)

                    self.success_edit_item = SuccessEditItemDialog(self.information_type)
                    self.success_edit_item.exec()

                else:
                    return False

            else:
                self.data_from_csv[index.row()][index.column()] = old_value

                if issue:
                    self.fail_to_edit_item_dialog = FailToEditItemDialog([issue], self.information_type)
                    self.fail_to_edit_item_dialog.exec()

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
