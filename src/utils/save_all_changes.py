import csv


class SaveAllChanges:
    def __init__(self, edit_type, students_table_model_data=None, programs_table_model_data=None,
                 colleges_table_model_data=None):

        self.edit_type = edit_type

        if not students_table_model_data:
            self.students_table_model_data = []
        else:
            self.students_table_model_data = students_table_model_data

        if not programs_table_model_data:
            self.programs_table_model_data = []
        else:
            self.programs_table_model_data = programs_table_model_data

        if not colleges_table_model_data:
            self.colleges_table_model_data = []
        else:
            self.colleges_table_model_data = colleges_table_model_data

    def to_csv(self):
        if self.edit_type == "student":
            with open("../databases/students.csv", 'w', newline='') as from_students_csv:
                writer = csv.writer(from_students_csv)

                writer.writerows(self.students_table_model_data)

        if self.edit_type == "program":
            with open("../databases/students.csv", 'w', newline='') as from_students_csv:
                writer = csv.writer(from_students_csv)

                writer.writerows(self.students_table_model_data)

            with open("../databases/programs.csv", 'w', newline='') as from_programs_csv:
                writer = csv.writer(from_programs_csv)

                writer.writerows(self.programs_table_model_data)

        if self.edit_type == "college":
            with open("../databases/students.csv", 'w', newline='') as from_students_csv:
                writer = csv.writer(from_students_csv)

                writer.writerows(self.students_table_model_data)

            with open("../databases/programs.csv", 'w', newline='') as from_programs_csv:
                writer = csv.writer(from_programs_csv)

                writer.writerows(self.programs_table_model_data)

            with open("../databases/colleges.csv", 'w', newline='') as from_colleges_csv:
                writer = csv.writer(from_colleges_csv)

                writer.writerows(self.colleges_table_model_data)
