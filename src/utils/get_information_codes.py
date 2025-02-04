import csv


class GetInformationCodes:

    @staticmethod
    def for_students():
        student_codes = []

        with open("databases/students.csv", 'r') as from_students_csv:
            reader = csv.reader(from_students_csv)

            for row in reader:
                student_codes.append(row[0])

        return student_codes

    @staticmethod
    def for_programs():
        program_codes = []

        with open("databases/programs.csv", 'r') as from_programs_csv:
            reader = csv.reader(from_programs_csv)

            for row in reader:
                program_codes.append(row[0])

        return program_codes

    @staticmethod
    def for_colleges():
        college_codes = []

        with open("databases/colleges.csv", 'r') as from_colleges_csv:
            reader = csv.reader(from_colleges_csv)

            for row in reader:
                college_codes.append(row[0])

        return college_codes
