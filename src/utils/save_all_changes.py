import csv


class SaveAllChanges:
    def __init__(self, students_table_model, programs_table_model, colleges_table_model):

        self.students_table_model = students_table_model
        self.programs_table_model = programs_table_model
        self.colleges_table_model = colleges_table_model

        if not self.students_table_model or self.students_table_model.get_data()[0][0] == "":
            self.students_table_model_data = []
        else:
            self.students_table_model_data = self.students_table_model.get_data()

        if not self.programs_table_model or programs_table_model.get_data()[0][0] == "":
            self.programs_table_model_data = []
        else:
            self.programs_table_model_data = self.programs_table_model.get_data()

        if not self.colleges_table_model or colleges_table_model.get_data()[0][0] == "":
            self.colleges_table_model_data = []
        else:
            self.colleges_table_model_data = self.colleges_table_model.get_data()

    def to_csv(self):
        print("Null")

