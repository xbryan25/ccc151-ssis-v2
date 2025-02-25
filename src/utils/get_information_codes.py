

class GetInformationCodes:

    @staticmethod
    def for_students(student_table_model_data):
        student_codes = []

        for student in student_table_model_data:
            student_codes.append(student[0])

        return student_codes

    @staticmethod
    def for_programs(program_table_model_data):
        program_codes = []

        for program in program_table_model_data:
            program_codes.append(program[0])

        return program_codes

    @staticmethod
    def for_colleges(colleges_table_model_data):
        college_codes = []

        for college in colleges_table_model_data:
            college_codes.append(college[0])

        return college_codes
