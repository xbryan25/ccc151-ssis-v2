import csv


class LoadInformationFromDatabase:

    @staticmethod
    def get_students():
        students_data = []

        with open("../databases/students.csv", 'r') as from_students_csv:
            reader = csv.reader(from_students_csv)

            for index, row in enumerate(reader):
                students_data.append(row)

        return students_data

    @staticmethod
    def get_programs():
        programs_data = []

        with open("../databases/programs.csv", 'r') as from_programs_csv:
            reader = csv.reader(from_programs_csv)

            for row in reader:
                programs_data.append(row)

        return programs_data

    @staticmethod
    def get_colleges():
        colleges_data = []

        with open("../databases/colleges.csv", 'r') as from_colleges_csv:
            reader = csv.reader(from_colleges_csv)

            for row in reader:
                colleges_data.append(row)

        return colleges_data
