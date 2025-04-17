from PyQt6.QtCore import QTimer, QObject

from application.open_dialogs import OpenDialogs
from application.search_and_sort_header import SearchAndSortHeader
from application.context_menu_setup import ContextMenuSetup


class ViewDemographicsPageControls:
    def __init__(self, application_window):

        self.aw = application_window

        self.add_signals()

        self.view_general_demographics()

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
        self.aw.setWindowTitle("Sequence | View General Demographics")

        self.aw.demographics_stacked_widget.setCurrentWidget(self.aw.general_demographics_widget)

        self.aw.gd_total_colleges_count_label.setText(str(self.aw.colleges_table_model.get_total_num()))
        self.aw.gd_total_programs_count_label.setText(str(self.aw.programs_table_model.get_total_num()))
        self.aw.gd_total_students_count_label.setText(str(self.aw.students_table_model.get_total_num()))

    def view_students_demographics(self):
        self.aw.setWindowTitle("Sequence | View Students Demographics")

        self.aw.demographics_stacked_widget.setCurrentWidget(self.aw.students_demographics_widget)

        self.aw.sd_total_students_count_label.setText(str(self.aw.students_table_model.get_total_num()))

        self.set_gender_demographic("student")
        self.set_year_level_demographic("student")

    def view_programs_demographics(self):
        self.aw.setWindowTitle("Sequence | View Programs Demographics")

        self.aw.demographics_stacked_widget.setCurrentWidget(self.aw.programs_demographics_widget)

        self.aw.pd_select_college_combobox.clear()
        self.load_college_codes("program")

    def view_colleges_demographics(self):
        self.aw.setWindowTitle("Sequence | View Colleges Demographics")

        self.aw.demographics_stacked_widget.setCurrentWidget(self.aw.colleges_demographics_widget)

        self.aw.cd_select_college_combobox.clear()
        self.load_college_codes("college")

    def set_gender_demographic(self, view_demographic_type, identifier=None):
        total_students = self.aw.students_table_model.get_total_num()

        if view_demographic_type == "student":
            gender_demographic = self.aw.database_handler.get_count_of_gender()

            self.aw.sd_gender_count_label.setText(f"Male: {gender_demographic['Male']} "
                                               f"({(gender_demographic['Male'] / total_students) * 100:.2f}%)"
                                               f"\nFemale: {gender_demographic['Female']} "
                                               f"({(gender_demographic['Female'] / total_students) * 100:.2f}%)"
                                               f"\nOthers: {gender_demographic['Others']} "
                                               f"({(gender_demographic['Others'] / total_students) * 100:.2f}%)"
                                               f"\nPrefer not to say: {gender_demographic['Prefer not to say']} "
                                               f"({(gender_demographic['Prefer not to say'] / total_students) * 100:.2f}%)")

        elif view_demographic_type == "program":
            gender_demographic = self.aw.database_handler.get_count_of_gender(identifier=identifier,
                                                                                          entity_type="program")

            self.aw.pd_gender_count_label.setText(f"Male: {gender_demographic['Male']} "
                                               f"({(gender_demographic['Male'] / total_students) * 100:.2f}%)"
                                               f"\nFemale: {gender_demographic['Female']} "
                                               f"({(gender_demographic['Female'] / total_students) * 100:.2f}%)"
                                               f"\nOthers: {gender_demographic['Others']} "
                                               f"({(gender_demographic['Others'] / total_students) * 100:.2f}%)"
                                               f"\nPrefer not to say: {gender_demographic['Prefer not to say']} "
                                               f"({(gender_demographic['Prefer not to say'] / total_students) * 100:.2f}%)")

        elif view_demographic_type == "college":
            gender_demographic = self.aw.database_handler.get_count_of_gender(identifier=identifier,
                                                                                          entity_type="college")

            self.aw.cd_gender_count_label.setText(f"Male: {gender_demographic['Male']} "
                                               f"({(gender_demographic['Male'] / total_students) * 100:.2f}%)"
                                               f"\nFemale: {gender_demographic['Female']} "
                                               f"({(gender_demographic['Female'] / total_students) * 100:.2f}%)"
                                               f"\nOthers: {gender_demographic['Others']} "
                                               f"({(gender_demographic['Others'] / total_students) * 100:.2f}%)"
                                               f"\nPrefer not to say: {gender_demographic['Prefer not to say']} "
                                               f"({(gender_demographic['Prefer not to say'] / total_students) * 100:.2f}%)")

    def set_year_level_demographic(self, view_demographic_type, identifier=None):
        total_students = self.aw.students_table_model.get_total_num()

        if view_demographic_type == "student":

            year_level_demographic = self.aw.database_handler.get_count_of_year_level()

            self.aw.sd_year_level_count_label.setText(f"1st Year: {year_level_demographic['1st']} "
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
            year_level_demographic = self.aw.database_handler.get_count_of_year_level(identifier=identifier,
                                                                                                  entity_type="program")

            self.aw.pd_year_level_count_label.setText(f"1st Year: {year_level_demographic['1st']} "
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
            year_level_demographic = self.aw.database_handler.get_count_of_year_level(identifier=identifier,
                                                                                                  entity_type="college")

            self.aw.cd_year_level_count_label.setText(f"1st Year: {year_level_demographic['1st']} "
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
            self.aw.pd_total_students_count_label.setText("-")
            self.aw.pd_gender_count_label.setText(f"Male: -"
                                               f"\nFemale: -"
                                               f"\nOthers: -"
                                               f"\nPrefer not to say: -")

            self.aw.pd_year_level_count_label.setText(f"1st Year: -"
                                                   f"\n2nd Year: -"
                                                   f"\n3rd Year: -"
                                                   f"\n4th Year: -"
                                                   f"\n5th Year: -")
        elif view_demographic_type == "college":
            self.aw.cd_total_programs_count_label.setText("-")
            self.aw.cd_total_students_count_label.setText("-")
            self.aw.cd_gender_count_label.setText(f"Male: -"
                                               f"\nFemale: -"
                                               f"\nOthers: -"
                                               f"\nPrefer not to say: -")

            self.aw.cd_year_level_count_label.setText(f"1st Year: -"
                                                   f"\n2nd Year: -"
                                                   f"\n3rd Year: -"
                                                   f"\n4th Year: -"
                                                   f"\n5th Year: -")

    def load_college_codes(self, view_demographic_type):
        college_codes = self.aw.database_handler.get_all_entity_information_codes('college')

        if view_demographic_type == "program":
            self.aw.pd_select_college_combobox.addItem("--Select a college--")
        elif view_demographic_type == "college":
            self.aw.cd_select_college_combobox.addItem("--Select a college--")

        for college_code in college_codes:
            if view_demographic_type == "program":
                self.aw.pd_select_college_combobox.addItem(college_code)
            elif view_demographic_type == "college":
                self.aw.cd_select_college_combobox.addItem(college_code)

    def load_program_codes(self, selected_college_code):
        self.aw.pd_select_program_combobox.clear()

        if selected_college_code == "--Select a college--" or selected_college_code == "":
            self.aw.pd_select_program_combobox.addItem("-")
            self.clear_data_in_labels("program")

        else:
            self.aw.pd_select_program_combobox.addItem("--Select a program--")

            program_codes = self.aw.database_handler.get_all_entity_information_codes('program')

            colleges_and_programs_connections = self.aw.database_handler.get_colleges_and_programs_connections()
            has_connection = False

            for program_code in program_codes:
                if program_code in colleges_and_programs_connections[selected_college_code]:
                    has_connection = True
                    self.aw.pd_select_program_combobox.addItem(program_code)

            if not has_connection:
                self.aw.pd_select_program_combobox.clear()
                self.aw.pd_select_program_combobox.addItem("--No programs available--")

    def load_program_data(self, selected_program_code):
        if selected_program_code.strip() != "" and selected_program_code != "-" and selected_program_code != "--Select a program--":

            self.aw.pd_total_students_count_label.setText(str(self.get_number_of_students_in_program(selected_program_code)))
            self.set_gender_demographic("program", selected_program_code)
            self.set_year_level_demographic("program", selected_program_code)
        else:
            self.clear_data_in_labels("program")

    def load_college_data(self, selected_college_code):
        if selected_college_code.strip() != "" and selected_college_code != "-" and selected_college_code != "--Select a college--":

            self.aw.cd_total_programs_count_label.setText(
                str(self.get_number_of_programs_in_college(selected_college_code)))

            self.aw.cd_total_students_count_label.setText(str(self.get_number_of_students_in_college(selected_college_code)))

            self.set_gender_demographic("college", selected_college_code)
            self.set_year_level_demographic("college", selected_college_code)
        else:
            self.clear_data_in_labels("college")

    def get_number_of_students_in_program(self, program_code):
        return self.aw.database_handler.get_count_of_all_students_in_program(program_code)

    def get_number_of_students_in_college(self, college_code):
        return self.aw.database_handler.get_count_of_all_students_in_college(college_code)

    def get_number_of_programs_in_college(self, college_code):
        return self.aw.database_handler.get_count_of_all_programs_in_college(college_code)

    def add_signals(self):
        self.aw.demographics_type_combobox.currentIndexChanged.connect(self.change_view_demographics)

        self.aw.pd_select_college_combobox.currentTextChanged.connect(self.load_program_codes)
        self.aw.pd_select_program_combobox.currentTextChanged.connect(self.load_program_data)

        self.aw.cd_select_college_combobox.currentTextChanged.connect(self.load_college_data)
