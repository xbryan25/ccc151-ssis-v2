
# The methods in this class checks if the new value that will overwrite the old value in the table is valid

class IsValidEditValue:

    @staticmethod
    def for_students_cell(index, value, id_numbers, full_names, data_from_csv):
        valid = True

        if index.column() == 0 and value.strip() in id_numbers:
            print("ID already exists")
            valid = False

        if index.column() == 1 and value.strip() == "":
            print("first name is blank")
        elif index.column() == 1 and f"{value.strip().upper()} {data_from_csv[index.row()][index.column() + 1].upper()}" in \
                [full_name.upper() for full_name in full_names]:
            print("Name combination exists")
            valid = False

        if index.column() == 2 and value.strip() == "":
            print("last name is blank")
        elif index.column() == 2 and f"{data_from_csv[index.row()][index.column() - 1].upper()} {value.strip().upper()}" in \
                [full_name.upper() for full_name in full_names]:
            print("Name combination exists")
            valid = False

        if index.column() == 3 and value.strip() not in ["1st", "2nd", "3rd", "4th", "5th"]:
            print("Not valid year level")
            valid = False

        if index.column() == 4 and value.strip() not in ["Male", "Female", "Others", "Prefer not to say"]:
            print("Not valid gender")
            valid = False

        return valid

    @staticmethod
    def for_programs_cell(index, value, program_codes, program_names):
        valid = True

        if index.column() == 0 and value.strip().upper() in program_codes:
            print("Program code already exists")
            valid = False

        if index.column() == 1 and value.strip().upper() in \
                [program_name.upper() for program_name in program_names]:
            print("Program name already exists")
            valid = False

        return valid

    @staticmethod
    def for_colleges_cell(index, value, college_codes, college_names):
        valid = True

        if index.column() == 0 and value.strip().upper() in college_codes:
            print("College code already exists")
            valid = False

        if index.column() == 1 and value.strip().upper() in \
                [college_name.upper() for college_name in college_names]:
            print("College name already exists")
            valid = False

        return valid
