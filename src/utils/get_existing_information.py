

class GetExistingInformation:

    @staticmethod
    def from_students(students_table_model_data):
        students_information = {"ID Number": [], "Full Name": []}

        for student in students_table_model_data:
            students_information["ID Number"].append(student[0])
            students_information["Full Name"].append(f"{student[1].strip()} {student[2].strip()}")

        return students_information

    @staticmethod
    def from_programs(programs_table_model_data):
        programs_information = {"Program Code": [], "Program Name": []}

        for program in programs_table_model_data:
            programs_information["Program Code"].append(program[0])
            programs_information["Program Name"].append(program[1].replace("_", ","))

        return programs_information

    @staticmethod
    def from_colleges(colleges_table_model_data):
        colleges_information = {"College Code": [], "College Name": []}

        for college in colleges_table_model_data:
            colleges_information["College Code"].append(college[0])
            colleges_information["College Name"].append(college[1].replace("_", ","))

        return colleges_information
