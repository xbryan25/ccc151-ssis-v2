from PyQt6.QtWidgets import QDialog, QFrame, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QFontDatabase

from operation_dialogs.students.students_demographic_design import Ui_Dialog as StudentsDemographicUI

from helper_dialogs.add_item_state.fail_add_item import FailAddItemDialog
from helper_dialogs.add_item_state.success_add_item import SuccessAddItemDialog

from utils.get_information_codes import GetInformationCodes
from utils.get_connections import GetConnections


class StudentsDemographicDialog(QDialog, StudentsDemographicUI):
    def __init__(self, students_table_model, programs_table_model, colleges_table_model):
        super().__init__()

        self.setupUi(self)

        self.set_external_stylesheet()
        self.load_fonts()

        self.students_table_model = students_table_model
        self.programs_table_model = programs_table_model
        self.colleges_table_model = colleges_table_model

        self.get_information_codes = GetInformationCodes()
        self.get_connections = GetConnections()

        self.get_year_level_demographic()
        self.get_gender_demographic()
        self.get_students_in_programs_demographic()

    def get_year_level_demographic(self):
        total_students = len(self.students_table_model.get_data())
        year_level_demographic = {"1st": 0, "2nd": 0, "3rd": 0, "4th": 0, "5th": 0}

        for student in self.students_table_model.get_data():
            year_level_demographic[student[3]] += 1

        self.year_level_demographic_label.setText(f"1st Year: {year_level_demographic['1st']} "
                                                  f"({(year_level_demographic['1st']/total_students) * 100:.2f}%)"
                                                  f"\n2nd Year: {year_level_demographic['2nd']} "
                                                  f"({(year_level_demographic['2nd']/total_students) * 100:.2f}%)"
                                                  f"\n3rd Year: {year_level_demographic['3rd']} "
                                                  f"({(year_level_demographic['3rd']/total_students) * 100:.2f}%)"
                                                  f"\n4th Year: {year_level_demographic['4th']} "
                                                  f"({(year_level_demographic['4th']/total_students) * 100:.2f}%)"
                                                  f"\n5th Year: {year_level_demographic['5th']} "
                                                  f"({(year_level_demographic['5th'] / total_students) * 100:.2f}%)")

    def get_gender_demographic(self):
        total_students = len(self.students_table_model.get_data())
        gender_demographic = {"Male": 0, "Female": 0, "Others": 0, "Prefer not to say": 0}

        for student in self.students_table_model.get_data():
            gender_demographic[student[4]] += 1

        self.gender_demographic_label.setText(f"Male: {gender_demographic['Male']} "
                                              f"({(gender_demographic['Male'] / total_students) * 100:.2f}%)"
                                              f"\nFemale: {gender_demographic['Female']} "
                                              f"({(gender_demographic['Female'] / total_students) * 100:.2f}%)"
                                              f"\nOthers: {gender_demographic['Others']} "
                                              f"({(gender_demographic['Others'] / total_students) * 100:.2f}%)"
                                              f"\nPrefer not to say: {gender_demographic['Prefer not to say']} "
                                              f"({(gender_demographic['Prefer not to say'] / total_students) * 100:.2f}%)")

    def get_students_in_programs_demographic(self):
        total_students = len(self.students_table_model.get_data())

        college_to_program_connections = self.get_connections.in_programs(self.programs_table_model.get_data(),
                                                                          self.colleges_table_model.get_data())

        program_to_student_connections = self.get_connections.in_students(self.students_table_model.get_data(),
                                                                         self.programs_table_model.get_data())

        for index, college_code in enumerate(self.get_college_codes()):
            if college_to_program_connections[college_code]:

                self.frame = QFrame(parent=self.scrollAreaWidgetContents)
                self.frame.setFrameShape(QFrame.Shape.StyledPanel)
                self.frame.setFrameShadow(QFrame.Shadow.Raised)
                self.frame.setObjectName(f"{college_code}_frame")
                self.verticalLayout_2 = QVBoxLayout(self.frame)
                self.verticalLayout_2.setContentsMargins(-1, 0, -1, 0)
                self.verticalLayout_2.setObjectName("verticalLayout_2")

                self.frame_title = QLabel(parent=self.frame)
                self.frame_title.setFont(QFont(self.cg_font_family, 15, QFont.Weight.Medium))
                self.frame_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.frame_title.setObjectName(f"{college_code}_frame_title")
                self.verticalLayout_2.addWidget(self.frame_title)

                self.frame_title.setText(f"{college_code}")

                self.frame_contents = QLabel(parent=self.frame)
                self.frame_contents.setFont(QFont(self.cg_font_family, 12, QFont.Weight.Normal))
                self.frame_contents.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.frame_contents.setObjectName("{college_code}_frame_contents")
                self.verticalLayout_2.addWidget(self.frame_contents)

                frame_contents_text = ""

                for program in self.get_program_codes():
                    if program in college_to_program_connections[college_code]:
                        frame_contents_text += (f"{program}: {len(program_to_student_connections[program])} "
                                                f"({(len(program_to_student_connections[program])/total_students) * 100:.2f}%)\n")

                self.frame_contents.setText(frame_contents_text)

                self.gridLayout_2.addWidget(self.frame, 5 + (index + 1), 0, 1, 3)

    def get_existing_students(self):
        return self.students_table_model.db_handler.get_all_existing_students()

    def get_program_codes(self):
        return self.get_information_codes.for_programs(self.programs_table_model.get_data())

    def get_college_codes(self):
        return self.get_information_codes.for_colleges(self.colleges_table_model.get_data())

    def set_external_stylesheet(self):
        with open("../assets/qss_files/dialog_style.qss", "r") as file:
            self.setStyleSheet(file.read())

    def load_fonts(self):
        self.cg_font_family = QFontDatabase.applicationFontFamilies(0)[0]

        self.header_label.setFont(QFont(self.cg_font_family, 22, QFont.Weight.DemiBold))

        self.year_level_label.setFont(QFont(self.cg_font_family, 18, QFont.Weight.Medium))
        self.year_level_demographic_label.setFont(QFont(self.cg_font_family, 10, QFont.Weight.Normal))
        self.gender_label.setFont(QFont(self.cg_font_family, 18, QFont.Weight.Medium))
        self.gender_demographic_label.setFont(QFont(self.cg_font_family, 10, QFont.Weight.Normal))
        self.students_label.setFont(QFont(self.cg_font_family, 18, QFont.Weight.Medium))

