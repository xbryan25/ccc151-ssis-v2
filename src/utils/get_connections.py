from utils.get_information_codes import GetInformationCodes

import csv


# Convert this from reading into the database to reading from model


class GetConnections:

    @staticmethod
    def in_students(students_table_model_data, programs_table_model_data):
        program_to_student_connections = {}

        for program_code in GetInformationCodes.for_programs(programs_table_model_data):
            program_to_student_connections.update({program_code: []})

        for student in students_table_model_data:
            if student[5] in program_to_student_connections.keys():
                program_to_student_connections[student[5]].append(student[0])

        return program_to_student_connections

    @staticmethod
    def in_programs(programs_table_model_data, colleges_table_model_data):
        college_to_program_connections = {}

        for college_code in GetInformationCodes.for_colleges(colleges_table_model_data):
            college_to_program_connections.update({college_code: []})

        for program in programs_table_model_data:
            if program[2] in college_to_program_connections.keys():
                college_to_program_connections[program[2]].append(program[0])

        return college_to_program_connections
