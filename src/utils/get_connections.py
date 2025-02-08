from utils.get_information_codes import GetInformationCodes

import csv


# Convert this from reading into the database to reading from model


class GetConnections:

    @staticmethod
    def in_students():
        program_to_student_connections = {}

        for program_code in GetInformationCodes.for_programs():
            program_to_student_connections.update({program_code: []})

        with open("../databases/students.csv", 'r') as from_students_csv:
            reader = csv.reader(from_students_csv)

            for row in reader:
                if row[5] in program_to_student_connections.keys():
                    program_to_student_connections[row[5]].append(row[0])

        return program_to_student_connections

    @staticmethod
    def in_programs():
        college_to_program_connections = {}

        for college_code in GetInformationCodes.for_colleges():
            college_to_program_connections.update({college_code: []})

        with open("../databases/programs.csv", 'r') as from_programs_csv:
            reader = csv.reader(from_programs_csv)

            for row in reader:
                if row[2] in college_to_program_connections.keys():
                    college_to_program_connections[row[2]].append(row[0])

        return college_to_program_connections
