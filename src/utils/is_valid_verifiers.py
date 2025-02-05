import re

# When edit_state is True, blank inputs (^$) are allowed because it means that the placeholder text will be
#   used when saving


class IsValidVerifiers:
    @staticmethod
    def id_number(id_number, edit_state=False):
        # valid_id_number = True

        if not edit_state:
            valid_id_number = re.match(r'^[0-9]{4}-[0-9]{4}$', id_number)
        else:
            valid_id_number = re.match(r'^[0-9]{4}-[0-9]{4}$|^$', id_number)

        return True if valid_id_number else False

    @staticmethod
    def first_name(first_name, edit_state=False):

        if not edit_state:
            valid_first_name = re.match(r'^[a-zA-Z ]+$', first_name)
        else:
            valid_first_name = re.match(r'^[a-zA-Z ]+$|^$', first_name)

        return True if valid_first_name else False

    @staticmethod
    def last_name(last_name, edit_state=False):
        if not edit_state:
            valid_last_name = re.match(r'^[a-zA-Z ]+$', last_name)
        else:
            valid_last_name = re.match(r'^[a-zA-Z ]+$|^$', last_name)

        return True if valid_last_name else False

    @staticmethod
    def program_code(program_code):
        valid_program_code = re.match(r'^[a-zA-Z]{3,}$', program_code)

        return True if valid_program_code else False

    @staticmethod
    def program_name(program_name):
        valid_program_name = re.match(r'^[a-zA-Z, ]+$', program_name)

        return True if valid_program_name else False

    @staticmethod
    def college_code(college_code):
        valid_college_code = re.match(r'^[a-zA-Z]{3,}$', college_code)

        return True if valid_college_code else False

    @staticmethod
    def college_name(college_name):
        valid_college_name = re.match(r'^[a-zA-Z, ]+$', college_name)

        return True if valid_college_name else False
