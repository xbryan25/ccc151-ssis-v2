

from PyQt6.QtWidgets import QDialog, QTableWidget, QTableWidgetItem, QFrame, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont

from programs.programs_demographic_design import Ui_Dialog as ProgramsDemographicUI

from helper_dialogs.add_item_state.fail_add_item import FailAddItemDialog
from helper_dialogs.add_item_state.success_add_item import SuccessAddItemDialog

from utils.is_valid_verifiers import IsValidVerifiers
from utils.get_information_codes import GetInformationCodes
from utils.get_existing_information import GetExistingInformation
from utils.get_connections import GetConnections

import re
import csv


class ProgramsDemographicDialog(QDialog, ProgramsDemographicUI):
    def __init__(self, students_table_model, programs_table_model, colleges_table_model):
        super().__init__()

        self.setupUi(self)

        self.set_external_stylesheet()

        self.students_table_model = students_table_model
        self.programs_table_model = programs_table_model
        self.colleges_table_model = colleges_table_model

        self.get_information_codes = GetInformationCodes()
        self.get_connections = GetConnections()

        # self.get_year_level_demographic()
        # self.get_gender_demographic()
        self.get_programs_demographic()

    def get_year_level_demographic_in_programs(self, program_code):
        total_students = len(self.students_table_model.get_data())
        year_level_demographic = {"1st": 0, "2nd": 0, "3rd": 0, "4th": 0, "5th": 0}

        program_to_student_connections = self.get_connections.in_students(self.students_table_model.get_data(),
                                                                          self.programs_table_model.get_data())
        for student in self.students_table_model.get_data():
            if student[0] in program_to_student_connections[program_code]:
                year_level_demographic[student[3]] += 1

        return (f"1st Year: {year_level_demographic["1st"]} "
                f"({(year_level_demographic["1st"]/total_students) * 100:.2f}%)"
                f"\n2nd Year: {year_level_demographic["2nd"]} "
                f"({(year_level_demographic["2nd"]/total_students) * 100:.2f}%)"
                f"\n3rd Year: {year_level_demographic["3rd"]} "
                f"({(year_level_demographic["3rd"]/total_students) * 100:.2f}%)"
                f"\n4th Year: {year_level_demographic["4th"]} "
                f"({(year_level_demographic["4th"]/total_students) * 100:.2f}%)"
                f"\n5th Year: {year_level_demographic["5th"]} "
                f"({(year_level_demographic["5th"] / total_students) * 100:.2f}%)")

    def get_gender_demographic_in_programs(self, program_code):
        total_students = len(self.students_table_model.get_data())
        gender_demographic = {"Male": 0, "Female": 0, "Others": 0, "Prefer not to say": 0}

        program_to_student_connections = self.get_connections.in_students(self.students_table_model.get_data(),
                                                                          self.programs_table_model.get_data())

        for student in self.students_table_model.get_data():
            if student[0] in program_to_student_connections[program_code]:
                gender_demographic[student[4]] += 1

        return (f"Male: {gender_demographic["Male"]} "
                f"({(gender_demographic["Male"] / total_students) * 100:.2f}%)"
                f"\nFemale: {gender_demographic["Female"]} "
                f"({(gender_demographic["Female"] / total_students) * 100:.2f}%)"
                f"\nOthers: {gender_demographic["Others"]} "
                f"({(gender_demographic["Others"] / total_students) * 100:.2f}%)"
                f"\nPrefer not to say: {gender_demographic["Prefer not to say"]} "
                f"({(gender_demographic["Prefer not to say"] / total_students) * 100:.2f}%)")

    def get_programs_demographic(self):

        college_to_program_connections = self.get_connections.in_programs(self.programs_table_model.get_data(),
                                                                          self.colleges_table_model.get_data())

        program_to_student_connections = self.get_connections.in_students(self.students_table_model.get_data(),
                                                                         self.programs_table_model.get_data())

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
            font = QFont()
            font.setFamily("Segoe UI Semibold")
            font.setPointSize(16)
            font.setBold(True)
            font.setWeight(75)
            self.college_label.setFont(font)
            self.college_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.college_label.setObjectName(f"{college_code}_label")

            self.gridLayout_2.addWidget(self.college_label, current_row, 1, 1, 1)

            current_row += 1

            self.college_label.setText(f"{college_code}")

            for index, program in enumerate(college_to_program_connections[college_code]):
                self.program_frame = QFrame(parent=self.scrollAreaWidgetContents)
                self.program_frame.setFrameShape(QFrame.Shape.StyledPanel)
                self.program_frame.setFrameShadow(QFrame.Shadow.Raised)
                self.program_frame.setObjectName(f"{college_code}_{program}_frame")
                self.verticalLayout = QVBoxLayout(self.program_frame)
                self.verticalLayout.setObjectName("verticalLayout")

                self.program_label = QLabel(parent=self.program_frame)
                font = QFont()
                font.setFamily("Segoe UI Semibold")
                font.setPointSize(13)
                font.setBold(True)
                font.setWeight(75)
                self.program_label.setFont(font)
                self.program_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.program_label.setObjectName(f"{college_code}_{program}_label")
                self.verticalLayout.addWidget(self.program_label)

                self.program_label.setText(f"{program}")

                self.program_contents_label = QLabel(parent=self.program_frame)
                font = QFont()
                font.setFamily("Segoe UI Semibold")
                font.setBold(True)
                font.setWeight(75)
                self.program_contents_label.setFont(font)
                self.program_contents_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.program_contents_label.setObjectName(f"{college_code}_{program}_contents_label")
                self.verticalLayout.addWidget(self.program_contents_label)

                number_of_students = len(program_to_student_connections[program])

                if number_of_students == 0:
                    self.program_contents_label.setText(f"Number of students: 0")
                else:
                    self.program_contents_label.setText(f"Number of students: {number_of_students}"
                                                        "\n\n"
                                                        f"{self.get_year_level_demographic_in_programs(program)}"
                                                        "\n\n"
                                                        f"{self.get_gender_demographic_in_programs(program)}")

                self.gridLayout_2.addWidget(self.program_frame, current_row, 0, 1, 3)

                current_row += 1

    def get_existing_students(self):
        return self.get_existing_information.from_students(self.students_table_model.get_data())

    def get_program_codes(self):
        return self.get_information_codes.for_programs(self.programs_table_model.get_data())

    def get_college_codes(self):
        return self.get_information_codes.for_colleges(self.colleges_table_model.get_data())

    def set_external_stylesheet(self):

        with open("../assets/qss_files/dialog_style.qss", "r") as file:
            self.setStyleSheet(file.read())