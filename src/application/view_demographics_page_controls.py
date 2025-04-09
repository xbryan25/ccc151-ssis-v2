from PyQt6.QtCore import QTimer, QObject

from application.open_dialogs import OpenDialogs
from application.search_and_sort_header import SearchAndSortHeader
from application.context_menu_setup import ContextMenuSetup

from utils.table_view_page_controls import TableViewPageControls


class ViewDemographicsPageControls:
    def __init__(self, view_demographics_page_elements):

        self.demographics_stacked_widget = view_demographics_page_elements[0]

        self.general_demographics_widget = view_demographics_page_elements[1]
        self.students_demographics_widget = view_demographics_page_elements[2]
        self.programs_demographics_widget = view_demographics_page_elements[3]
        self.colleges_demographics_widget = view_demographics_page_elements[4]

        self.students_table_model = view_demographics_page_elements[5]
        self.programs_table_model = view_demographics_page_elements[6]
        self.colleges_table_model = view_demographics_page_elements[7]

        self.gd_total_colleges_count_label = view_demographics_page_elements[8]
        self.gd_total_programs_count_label = view_demographics_page_elements[9]
        self.gd_total_students_count_label = view_demographics_page_elements[10]

        self.sd_total_students_count_label = view_demographics_page_elements[11]
        self.sd_gender_count_label = view_demographics_page_elements[12]
        self.sd_year_level_count_label = view_demographics_page_elements[13]

        self.pd_select_college_combobox = view_demographics_page_elements[14]
        self.pd_select_program_combobox = view_demographics_page_elements[15]
        self.pd_total_students_count_label = view_demographics_page_elements[16]
        self.pd_year_level_count_label = view_demographics_page_elements[17]
        self.pd_gender_count_label = view_demographics_page_elements[18]

        self.cd_select_college_combobox = view_demographics_page_elements[19]
        self.cd_total_programs_count_label = view_demographics_page_elements[20]
        self.cd_total_students_count_label = view_demographics_page_elements[21]
        self.cd_gender_count_label = view_demographics_page_elements[22]
        self.cd_year_level_count_label = view_demographics_page_elements[23]

        self.demographics_type_combobox = view_demographics_page_elements[24]

        self.application_window = view_demographics_page_elements[25]

        self.demographics_type_combobox.currentIndexChanged.connect(self.change_view_demographics)

        self.view_general_demographics()

        self.add_signals()

    def change_view_demographics(self, index):
        if index == 0:
            self.view_general_demographics()
        elif index == 1:
            self.view_students_demographics()
        elif index == 2:
            self.view_programs_demographics()
        elif index == 3:
            self.view_colleges_demographics()

    def view_general_demographics(self):
        self.application_window.setWindowTitle("Sequence | View General Demographics")

        self.demographics_stacked_widget.setCurrentWidget(self.general_demographics_widget)

        self.gd_total_colleges_count_label.setText(str(len(self.colleges_table_model.get_data())))
        self.gd_total_programs_count_label.setText(str(len(self.programs_table_model.get_data())))
        self.gd_total_students_count_label.setText(str(len(self.students_table_model.get_data())))

    def view_students_demographics(self):
        self.application_window.setWindowTitle("Sequence | View Students Demographics")

        self.demographics_stacked_widget.setCurrentWidget(self.students_demographics_widget)

        self.sd_total_students_count_label.setText(str(len(self.students_table_model.get_data())))

        self.set_gender_demographic("student")
        self.set_year_level_demographic("student")

    def view_programs_demographics(self):
        self.application_window.setWindowTitle("Sequence | View Programs Demographics")

        self.demographics_stacked_widget.setCurrentWidget(self.programs_demographics_widget)

        self.pd_select_college_combobox.clear()
        self.load_college_codes("program")

    def view_colleges_demographics(self):
        self.application_window.setWindowTitle("Sequence | View Colleges Demographics")

        self.demographics_stacked_widget.setCurrentWidget(self.colleges_demographics_widget)

        self.cd_select_college_combobox.clear()
        self.load_college_codes("college")

    def set_gender_demographic(self, view_demographic_type, identifier=None):
        total_students = len(self.students_table_model.get_data())
        gender_demographic = {"Male": 0, "Female": 0, "Others": 0, "Prefer not to say": 0}

        if view_demographic_type == "student":
            for student in self.students_table_model.get_data():
                gender_demographic[student[4]] += 1

            self.sd_gender_count_label.setText(f"Male: {gender_demographic['Male']} "
                                               f"({(gender_demographic['Male'] / total_students) * 100:.2f}%)"
                                               f"\nFemale: {gender_demographic['Female']} "
                                               f"({(gender_demographic['Female'] / total_students) * 100:.2f}%)"
                                               f"\nOthers: {gender_demographic['Others']} "
                                               f"({(gender_demographic['Others'] / total_students) * 100:.2f}%)"
                                               f"\nPrefer not to say: {gender_demographic['Prefer not to say']} "
                                               f"({(gender_demographic['Prefer not to say'] / total_students) * 100:.2f}%)")

        elif view_demographic_type == "program":
            program_to_student_connections = self.programs_table_model.db_handler.get_programs_and_students_connections()

            for student in self.students_table_model.get_data():
                if student[0] in program_to_student_connections[identifier]:
                    gender_demographic[student[4]] += 1

            self.pd_gender_count_label.setText(f"Male: {gender_demographic['Male']} "
                                               f"({(gender_demographic['Male'] / total_students) * 100:.2f}%)"
                                               f"\nFemale: {gender_demographic['Female']} "
                                               f"({(gender_demographic['Female'] / total_students) * 100:.2f}%)"
                                               f"\nOthers: {gender_demographic['Others']} "
                                               f"({(gender_demographic['Others'] / total_students) * 100:.2f}%)"
                                               f"\nPrefer not to say: {gender_demographic['Prefer not to say']} "
                                               f"({(gender_demographic['Prefer not to say'] / total_students) * 100:.2f}%)")

        elif view_demographic_type == "college":
            college_to_program_connections = self.programs_table_model.db_handler.get_colleges_and_programs_connections()
            program_to_student_connections = self.programs_table_model.db_handler.get_programs_and_students_connections()

            for program_code in college_to_program_connections[identifier]:
                for student in self.students_table_model.get_data():
                    if student[0] in program_to_student_connections[program_code]:
                        gender_demographic[student[4]] += 1

            self.cd_gender_count_label.setText(f"Male: {gender_demographic['Male']} "
                                               f"({(gender_demographic['Male'] / total_students) * 100:.2f}%)"
                                               f"\nFemale: {gender_demographic['Female']} "
                                               f"({(gender_demographic['Female'] / total_students) * 100:.2f}%)"
                                               f"\nOthers: {gender_demographic['Others']} "
                                               f"({(gender_demographic['Others'] / total_students) * 100:.2f}%)"
                                               f"\nPrefer not to say: {gender_demographic['Prefer not to say']} "
                                               f"({(gender_demographic['Prefer not to say'] / total_students) * 100:.2f}%)")

    def set_year_level_demographic(self, view_demographic_type, identifier=None):
        total_students = len(self.students_table_model.get_data())
        year_level_demographic = {"1st": 0, "2nd": 0, "3rd": 0, "4th": 0, "5th": 0}

        if view_demographic_type == "student":
            for student in self.students_table_model.get_data():
                year_level_demographic[student[3]] += 1

            self.sd_year_level_count_label.setText(f"1st Year: {year_level_demographic['1st']} "
                                                   f"({(year_level_demographic['1st'] / total_students) * 100:.2f}%)"
                                                   f"\n2nd Year: {year_level_demographic['2nd']} "
                                                   f"({(year_level_demographic['2nd'] / total_students) * 100:.2f}%)"
                                                   f"\n3rd Year: {year_level_demographic['3rd']} "
                                                   f"({(year_level_demographic['3rd'] / total_students) * 100:.2f}%)"
                                                   f"\n4th Year: {year_level_demographic['4th']} "
                                                   f"({(year_level_demographic['4th'] / total_students) * 100:.2f}%)"
                                                   f"\n5th Year: {year_level_demographic['5th']} "
                                                   f"({(year_level_demographic['5th'] / total_students) * 100:.2f}%)")

        elif view_demographic_type == "program":
            program_to_student_connections = self.programs_table_model.db_handler.get_programs_and_students_connections()

            for student in self.students_table_model.get_data():
                if student[0] in program_to_student_connections[identifier]:
                    year_level_demographic[student[3]] += 1

            self.pd_year_level_count_label.setText(f"1st Year: {year_level_demographic['1st']} "
                                                   f"({(year_level_demographic['1st'] / total_students) * 100:.2f}%)"
                                                   f"\n2nd Year: {year_level_demographic['2nd']} "
                                                   f"({(year_level_demographic['2nd'] / total_students) * 100:.2f}%)"
                                                   f"\n3rd Year: {year_level_demographic['3rd']} "
                                                   f"({(year_level_demographic['3rd'] / total_students) * 100:.2f}%)"
                                                   f"\n4th Year: {year_level_demographic['4th']} "
                                                   f"({(year_level_demographic['4th'] / total_students) * 100:.2f}%)"
                                                   f"\n5th Year: {year_level_demographic['5th']} "
                                                   f"({(year_level_demographic['5th'] / total_students) * 100:.2f}%)")

        elif view_demographic_type == "college":
            college_to_program_connections = self.programs_table_model.db_handler.get_colleges_and_programs_connections()
            program_to_student_connections = self.programs_table_model.db_handler.get_programs_and_students_connections()

            for program_code in college_to_program_connections[identifier]:
                for student in self.students_table_model.get_data():
                    if student[0] in program_to_student_connections[program_code]:
                        year_level_demographic[student[3]] += 1

            self.cd_year_level_count_label.setText(f"1st Year: {year_level_demographic['1st']} "
                                                   f"({(year_level_demographic['1st'] / total_students) * 100:.2f}%)"
                                                   f"\n2nd Year: {year_level_demographic['2nd']} "
                                                   f"({(year_level_demographic['2nd'] / total_students) * 100:.2f}%)"
                                                   f"\n3rd Year: {year_level_demographic['3rd']} "
                                                   f"({(year_level_demographic['3rd'] / total_students) * 100:.2f}%)"
                                                   f"\n4th Year: {year_level_demographic['4th']} "
                                                   f"({(year_level_demographic['4th'] / total_students) * 100:.2f}%)"
                                                   f"\n5th Year: {year_level_demographic['5th']} "
                                                   f"({(year_level_demographic['5th'] / total_students) * 100:.2f}%)")

    def clear_data_in_labels(self, view_demographic_type):
        if view_demographic_type == "program":
            self.pd_total_students_count_label.setText("-")
            self.pd_gender_count_label.setText(f"Male: -"
                                               f"\nFemale: -"
                                               f"\nOthers: -"
                                               f"\nPrefer not to say: -")

            self.pd_year_level_count_label.setText(f"1st Year: -"
                                                   f"\n2nd Year: -"
                                                   f"\n3rd Year: -"
                                                   f"\n4th Year: -"
                                                   f"\n5th Year: -")
        elif view_demographic_type == "college":
            self.cd_total_programs_count_label.setText("-")
            self.cd_total_students_count_label.setText("-")
            self.cd_gender_count_label.setText(f"Male: -"
                                               f"\nFemale: -"
                                               f"\nOthers: -"
                                               f"\nPrefer not to say: -")

            self.cd_year_level_count_label.setText(f"1st Year: -"
                                                   f"\n2nd Year: -"
                                                   f"\n3rd Year: -"
                                                   f"\n4th Year: -"
                                                   f"\n5th Year: -")

    def load_college_codes(self, view_demographic_type):
        college_codes = self.colleges_table_model.db_handler.get_all_entity_information_codes('college')

        if view_demographic_type == "program":
            self.pd_select_college_combobox.addItem("--Select a college--")
        elif view_demographic_type == "college":
            self.cd_select_college_combobox.addItem("--Select a college--")

        for college_code in college_codes:
            if view_demographic_type == "program":
                self.pd_select_college_combobox.addItem(college_code)
            elif view_demographic_type == "college":
                self.cd_select_college_combobox.addItem(college_code)

    def load_program_codes(self, selected_college_code):
        self.pd_select_program_combobox.clear()

        if selected_college_code == "--Select a college--" or selected_college_code == "":
            self.pd_select_program_combobox.addItem("-")
            self.clear_data_in_labels("program")

        else:
            self.pd_select_program_combobox.addItem("--Select a program--")

            program_codes = self.programs_table_model.db_handler.get_all_entity_information_codes('program')

            colleges_and_programs_connections = self.programs_table_model.db_handler.get_colleges_and_programs_connections()
            has_connection = False

            for program_code in program_codes:
                if program_code in colleges_and_programs_connections[selected_college_code]:
                    has_connection = True
                    self.pd_select_program_combobox.addItem(program_code)

            if not has_connection:
                self.pd_select_program_combobox.clear()
                self.pd_select_program_combobox.addItem("--No programs available--")

    def load_program_data(self, selected_program_code):
        if selected_program_code.strip() != "" and selected_program_code != "-" and selected_program_code != "--Select a program--":
            program_to_student_connections = self.programs_table_model.db_handler.get_programs_and_students_connections()

            self.pd_total_students_count_label.setText(str(len(program_to_student_connections[selected_program_code])))
            self.set_gender_demographic("program", selected_program_code)
            self.set_year_level_demographic("program", selected_program_code)
        else:
            self.clear_data_in_labels("program")

    def load_college_data(self, selected_college_code):
        if selected_college_code.strip() != "" and selected_college_code != "-" and selected_college_code != "--Select a college--":

            self.cd_total_programs_count_label.setText(
                str(self.get_number_of_programs_in_college(selected_college_code)))
            self.cd_total_students_count_label.setText(str(self.get_number_of_students_in_college(selected_college_code)))

            self.set_gender_demographic("college", selected_college_code)
            self.set_year_level_demographic("college", selected_college_code)
        else:
            self.clear_data_in_labels("college")

    def get_number_of_students_in_college(self, college_code):
        number_of_students = 0

        college_to_program_connections = self.colleges_table_model.db_handler.get_colleges_and_programs_connections()

        program_to_student_connections = self.colleges_table_model.db_handler.get_programs_and_students_connections()

        for program_code in college_to_program_connections[college_code]:
            for student in self.students_table_model.get_data():
                if student[0] in program_to_student_connections[program_code]:
                    number_of_students += 1

        return number_of_students

    def get_number_of_programs_in_college(self, college_code):
        college_to_program_connections = self.colleges_table_model.db_handler.get_colleges_and_programs_connections()

        return len(college_to_program_connections[college_code])

    def add_signals(self):
        self.pd_select_college_combobox.currentTextChanged.connect(self.load_program_codes)
        self.pd_select_program_combobox.currentTextChanged.connect(self.load_program_data)

        self.cd_select_college_combobox.currentTextChanged.connect(self.load_college_data)
