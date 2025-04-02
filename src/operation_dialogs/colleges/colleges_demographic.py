from PyQt6.QtWidgets import QDialog, QFrame, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QFontDatabase

from operation_dialogs.colleges.colleges_demographic_design import Ui_Dialog as CollegesDemographicUI

from helper_dialogs.add_item_state.fail_add_item import FailAddItemDialog
from helper_dialogs.add_item_state.success_add_item import SuccessAddItemDialog

import re
import csv


class CollegesDemographicDialog(QDialog, CollegesDemographicUI):
    def __init__(self, colleges_table_model):
        super().__init__()

        self.setupUi(self)

        self.set_external_stylesheet()
        self.load_fonts()

        self.colleges_table_model = colleges_table_model

        self.all_students = self.colleges_table_model.db_handler.get_all_entities('student')
        self.num_of_students = len(self.all_students)

        self.get_colleges_demographic()

    def get_year_level_demographic_in_colleges(self, college_code):
        year_level_demographic = {"1st": 0, "2nd": 0, "3rd": 0, "4th": 0, "5th": 0}

        college_to_program_connections = self.colleges_table_model.db_handler.get_colleges_and_programs_connections()

        program_to_student_connections = self.colleges_table_model.db_handler.get_programs_and_students_connections()

        for program_code in college_to_program_connections[college_code]:
            for student in self.all_students:
                if student[0] in program_to_student_connections[program_code]:
                    year_level_demographic[student[3]] += 1

        return (f"1st Year: {year_level_demographic['1st']} "
                f"({(year_level_demographic['1st'] / self.num_of_students) * 100:.2f}%)"
                f"\n2nd Year: {year_level_demographic['2nd']} "
                f"({(year_level_demographic['2nd'] / self.num_of_students) * 100:.2f}%)"
                f"\n3rd Year: {year_level_demographic['3rd']} "
                f"({(year_level_demographic['3rd'] / self.num_of_students) * 100:.2f}%)"
                f"\n4th Year: {year_level_demographic['4th']} "
                f"({(year_level_demographic['4th'] / self.num_of_students) * 100:.2f}%)"
                f"\n5th Year: {year_level_demographic['5th']} "
                f"({(year_level_demographic['5th'] / self.num_of_students) * 100:.2f}%)")

    def get_gender_demographic_in_colleges(self, college_code):
        gender_demographic = {"Male": 0, "Female": 0, "Others": 0, "Prefer not to say": 0}

        college_to_program_connections = self.colleges_table_model.db_handler.get_colleges_and_programs_connections()

        program_to_student_connections = self.colleges_table_model.db_handler.get_programs_and_students_connections()

        for program_code in college_to_program_connections[college_code]:
            for student in self.all_students:
                if student[0] in program_to_student_connections[program_code]:
                    gender_demographic[student[4]] += 1

        return (f"Male: {gender_demographic['Male']} "
                f"({(gender_demographic['Male'] / self.num_of_students) * 100:.2f}%)"
                f"\nFemale: {gender_demographic['Female']} "
                f"({(gender_demographic['Female'] / self.num_of_students) * 100:.2f}%)"
                f"\nOthers: {gender_demographic['Others']} "
                f"({(gender_demographic['Others'] / self.num_of_students) * 100:.2f}%)"
                f"\nPrefer not to say: {gender_demographic['Prefer not to say']} "
                f"({(gender_demographic['Prefer not to say'] / self.num_of_students) * 100:.2f}%)")

    def get_number_of_students_in_college(self, college_code):
        number_of_students = 0

        college_to_program_connections = self.colleges_table_model.db_handler.get_colleges_and_programs_connections()

        program_to_student_connections = self.colleges_table_model.db_handler.get_programs_and_students_connections()

        for program_code in college_to_program_connections[college_code]:
            for student in self.all_students:
                if student[0] in program_to_student_connections[program_code]:
                    number_of_students += 1

        return number_of_students

    def get_number_of_programs_in_college(self, college_code):
        college_to_program_connections = self.colleges_table_model.db_handler.get_colleges_and_programs_connections()

        return len(college_to_program_connections[college_code])

    def get_colleges_demographic(self):

        current_row = 0

        for college_code in self.get_college_codes():
            self.college_left_line = QFrame(parent=self.scrollAreaWidgetContents)
            self.college_left_line.setFrameShadow(QFrame.Shadow.Plain)
            self.college_left_line.setFrameShape(QFrame.Shape.HLine)
            self.college_left_line.setObjectName(f"{college_code}_left_line")
            self.gridLayout_2.addWidget(self.college_left_line, current_row, 0, 1, 1)

            self.college_right_line = QFrame(parent=self.scrollAreaWidgetContents)
            self.college_right_line.setFrameShadow(QFrame.Shadow.Plain)
            self.college_right_line.setFrameShape(QFrame.Shape.HLine)
            self.college_right_line.setObjectName(f"{college_code}_right_line")
            self.gridLayout_2.addWidget(self.college_right_line, current_row, 2, 1, 1)

            self.college_label = QLabel(parent=self.scrollAreaWidgetContents)
            self.college_label.setMaximumSize(QSize(16777215, 40))
            self.college_label.setFont(QFont(self.cg_font_family, 16, QFont.Weight.Medium))
            self.college_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.college_label.setObjectName(f"{college_code}_label")

            self.gridLayout_2.addWidget(self.college_label, current_row, 1, 1, 1)

            current_row += 1

            self.college_label.setText(f"{college_code}")

            self.college_contents_label = QLabel(parent=self.scrollAreaWidgetContents)
            self.college_contents_label.setMaximumSize(QSize(16777215, 16777215))
            self.college_contents_label.setFont(QFont(self.cg_font_family, 11, QFont.Weight.Normal))
            self.college_contents_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.college_contents_label.setObjectName(f"{college_code}_contents_label")

            self.gridLayout_2.addWidget(self.college_contents_label, current_row, 0, 1, 3)

            current_row += 1

            if self.get_number_of_programs_in_college(college_code) == 0:
                self.college_contents_label.setText("Number of programs: 0")

            elif self.get_number_of_students_in_college(college_code) == 0:
                self.college_contents_label.setText(
                    f"Number of programs: {self.get_number_of_programs_in_college(college_code)}"
                    "\n\n"
                    f"Number of students: 0")
            else:
                self.college_contents_label.setText(
                    f"Number of programs: {self.get_number_of_programs_in_college(college_code)}"
                    "\n\n"
                    f"Number of students: {self.get_number_of_students_in_college(college_code)}"
                    "\n\n"
                    f"{self.get_year_level_demographic_in_colleges(college_code)}"
                    "\n\n"
                    f"{self.get_gender_demographic_in_colleges(college_code)}")

    def get_existing_students(self):
        return self.colleges_table_model.db_handler.get_all_existing_students()

    def get_program_codes(self):
        return self.colleges_table_model.db_handler.get_all_entity_information_codes('program')

    def get_college_codes(self):
        return self.colleges_table_model.db_handler.get_all_entity_information_codes('college')

    def set_external_stylesheet(self):
        with open("../assets/qss_files/dialog_style.qss", "r") as file:
            self.setStyleSheet(file.read())

    def load_fonts(self):
        self.cg_font_family = QFontDatabase.applicationFontFamilies(0)[0]

        self.header_label.setFont(QFont(self.cg_font_family, 22, QFont.Weight.DemiBold))
