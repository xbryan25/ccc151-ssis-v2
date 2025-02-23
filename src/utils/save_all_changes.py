import csv


class SaveAllChanges:
    def __init__(self, students_table_model, programs_table_model, colleges_table_model):

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
        if self.students_table_model.get_has_changes():
            self.students_table_model.set_has_changes(False)

            with open("../databases/students.csv", 'w', newline='') as from_students_csv:
                writer = csv.writer(from_students_csv)

                writer.writerows(self.students_table_model_data)

        if self.programs_table_model.get_has_changes():
            self.programs_table_model.set_has_changes(False)

            with open("../databases/programs.csv", 'w', newline='') as from_programs_csv:
                writer = csv.writer(from_programs_csv)

                writer.writerows(self.programs_table_model_data)

        if self.colleges_table_model.get_has_changes():
            self.colleges_table_model.set_has_changes(False)

            with open("../databases/colleges.csv", 'w', newline='') as from_colleges_csv:
                writer = csv.writer(from_colleges_csv)

                writer.writerows(self.colleges_table_model_data)
