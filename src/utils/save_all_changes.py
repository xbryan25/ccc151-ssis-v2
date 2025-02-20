import csv


class SaveAllChanges:
    def __init__(self, edit_type, students_table_model=None, programs_table_model=None,
                 colleges_table_model=None):

        self.edit_type = edit_type

        self.students_table_model = students_table_model
        self.programs_table_model = programs_table_model
        self.colleges_table_model = colleges_table_model

        if not self.students_table_model or not self.students_table_model.get_data():
            self.students_table_model_data = []
        else:
            self.students_table_model_data = self.students_table_model.get_data()

        if not self.programs_table_model or not programs_table_model.get_data():
            self.programs_table_model_data = []
        else:
            self.programs_table_model_data = self.programs_table_model.get_data()

        if not self.colleges_table_model or not colleges_table_model.get_data():
            self.colleges_table_model_data = []
        else:
            self.colleges_table_model_data = self.colleges_table_model.get_data()

    def to_csv(self):
        if self.edit_type == "student":
            self.students_table_model.set_has_changes(True)

            with open("../databases/students.csv", 'w', newline='') as from_students_csv:
                writer = csv.writer(from_students_csv)

                writer.writerows(self.students_table_model_data)

        if self.edit_type == "program":
            self.students_table_model.set_has_changes(False)
            self.programs_table_model.set_has_changes(False)

            with open("../databases/students.csv", 'w', newline='') as from_students_csv:
                writer = csv.writer(from_students_csv)

                writer.writerows(self.students_table_model_data)

            with open("../databases/programs.csv", 'w', newline='') as from_programs_csv:
                writer = csv.writer(from_programs_csv)

                writer.writerows(self.programs_table_model_data)

        if self.edit_type == "college":
            self.students_table_model.set_has_changes(False)
            self.programs_table_model.set_has_changes(False)
            self.colleges_table_model.set_has_changes(False)

            print("reach here")

            with open("../databases/students.csv", 'w', newline='') as from_students_csv:
                writer = csv.writer(from_students_csv)

                writer.writerows(self.students_table_model_data)

            with open("../databases/programs.csv", 'w', newline='') as from_programs_csv:
                writer = csv.writer(from_programs_csv)

                writer.writerows(self.programs_table_model_data)

            with open("../databases/colleges.csv", 'w', newline='') as from_colleges_csv:
                writer = csv.writer(from_colleges_csv)

                writer.writerows(self.colleges_table_model_data)
