import pymysql


class DatabaseHandler:
    
    def __init__(self):
        self.db = pymysql.connect(
            host='localhost',
            user='root',
            password='root',
            database='ssis_db'
        )
        
        self.cursor = self.db.cursor()

    def get_all_entities(self, entity_type):
        entities_data = []

        if entity_type == "student":
            self.cursor.execute("SELECT * FROM students")
        elif entity_type == "program":
            self.cursor.execute("SELECT * FROM programs")
        elif entity_type == "college":
            self.cursor.execute("SELECT * FROM colleges")

        results = self.cursor.fetchall()

        for row in results:
            list_row = list(row)

            if entity_type == 'student' and not list_row[5]:
                list_row[5] = "N/A"
            elif entity_type == 'program' and not list_row[2]:
                list_row[2] = "N/A"

            entities_data.append(list_row)

        return entities_data

    def get_all_existing_students(self):
        sql = "SELECT id_number, first_name, last_name FROM students"

        self.cursor.execute(sql)

        results = self.cursor.fetchall()

        students_information = {"ID Number": [], "Full Name": []}

        for student_information in results:
            students_information["ID Number"].append(student_information[0])
            students_information["Full Name"].append(f"{student_information[1].strip()} {student_information[2].strip()}")

        return students_information

    def get_all_existing_programs(self):
        sql = "SELECT program_code, program_name FROM programs"

        self.cursor.execute(sql)

        results = self.cursor.fetchall()

        programs_information = {"Program Code": [], "Program Name": []}

        for program_information in results:
            programs_information["Program Code"].append(program_information[0])
            programs_information["Program Name"].append(program_information[1])

        return programs_information

    def get_all_existing_colleges(self):
        sql = "SELECT college_code, college_name FROM colleges"

        self.cursor.execute(sql)

        results = self.cursor.fetchall()

        colleges_information = {"College Code": [], "College Name": []}

        for college_information in results:
            colleges_information["College Code"].append(college_information[0])
            colleges_information["College Name"].append(college_information[1])

        return colleges_information

    def get_all_entity_information_codes(self, entity_type):
        sql = ""

        if entity_type == "student":
            sql = "SELECT id_number FROM students"
        elif entity_type == "program":
            sql = "SELECT program_code FROM programs"
        elif entity_type == "college":
            sql = "SELECT college_code FROM colleges"

        self.cursor.execute(sql)

        results = self.cursor.fetchall()

        entity_codes = []

        for entity_code in results:
            entity_codes.append(entity_code[0])

        return entity_codes

    def get_colleges_and_programs_connections(self):
        sql = ("SELECT colleges.college_code, programs.program_code "
               "FROM colleges LEFT JOIN programs ON colleges.college_code = programs.college_code")

        self.cursor.execute(sql)

        results = self.cursor.fetchall()

        college_to_program_connections = {}

        for college_to_program_connection in results:
            if college_to_program_connection[0] not in college_to_program_connections.keys():
                college_to_program_connections.update({college_to_program_connection[0]: []})

            if college_to_program_connection[1]:
                college_to_program_connections[college_to_program_connection[0]].append(
                    college_to_program_connection[1])

        return college_to_program_connections

    def get_programs_and_students_connections(self):
        sql = ("SELECT programs.program_code, students.id_number "
               "FROM programs LEFT JOIN students ON programs.program_code = students.program_code")

        self.cursor.execute(sql)

        results = self.cursor.fetchall()

        program_to_student_connections = {}

        for program_to_student_connection in results:
            if program_to_student_connection[0] not in program_to_student_connections.keys():
                program_to_student_connections.update({program_to_student_connection[0]: []})

            if program_to_student_connection[1]:
                program_to_student_connections[program_to_student_connection[0]].append(program_to_student_connection[1])

        return program_to_student_connections

    def get_sorted_entities(self, entity_type, sort_column, sort_order):
        sql = f"SELECT * FROM {entity_type + "s"} ORDER BY {sort_column} IS NULL, {sort_column}"

        if sort_order == "ascending":
            sql += " ASC"
        else:
            sql += " DESC"

        self.cursor.execute(sql)

        results = self.cursor.fetchall()

        entities_data = []

        for row in results:
            list_row = list(row)

            if entity_type == 'student' and not list_row[5]:
                list_row[5] = "N/A"
            elif entity_type == 'program' and not list_row[2]:
                list_row[2] = "N/A"

            entities_data.append(list_row)

        return entities_data

    def get_sorted_filtered_entities(self, entity_type, sort_column, sort_order, search_type, search_text):
        if search_type != "all":
            sql = f"SELECT * FROM {entity_type + "s"} WHERE {search_type} LIKE %s"
            values = (f"{search_text}%",)
        else:
            sql = ""
            values = ()

            if entity_type == "student":
                sql = ("SELECT * FROM students "
                       "WHERE id_number LIKE %s OR "
                       "first_name LIKE %s OR "
                       "last_name LIKE %s OR "
                       "year_level LIKE %s OR "
                       "gender LIKE %s OR "
                       "program_code LIKE %s")

                values = (f"{search_text}%",
                          f"{search_text}%",
                          f"{search_text}%",
                          f"{search_text}%",
                          f"{search_text}%",
                          f"{search_text}%")

            elif entity_type == "program":
                sql = ("SELECT * FROM programs "
                       "WHERE program_code LIKE %s OR "
                       "program_name LIKE %s OR "
                       "college_code LIKE %s")

                values = (f"{search_text}%",
                          f"{search_text}%",
                          f"{search_text}%")

            elif entity_type == "college":
                sql = ("SELECT * FROM colleges "
                       "WHERE college_code LIKE %s OR "
                       "college_name LIKE %s")

                values = (f"{search_text}%",
                          f"{search_text}%")

        if sort_column and sort_order:
            if sort_order == "ascending":
                sql += f" ORDER BY {sort_column} IS NULL, {sort_column} ASC"
            else:
                sql += f" ORDER BY {sort_column} IS NULL, {sort_column} DESC"

        self.cursor.execute(sql, values)
        results = self.cursor.fetchall()

        entities_data = []

        for row in results:
            list_row = list(row)

            if entity_type == 'student' and not list_row[5]:
                list_row[5] = "N/A"
            elif entity_type == 'program' and not list_row[2]:
                list_row[2] = "N/A"

            entities_data.append(list_row)

        return entities_data

    # def search_entities(self, entity_type, search_type, search_text):
    #     if search_type != "all":
    #         sql = ""
    #         values = (f"{search_text}%",)
    #
    #         if entity_type == "student":
    #             sql = f"SELECT * FROM students WHERE {search_type} LIKE %s"
    #         elif entity_type == "program":
    #             sql = f"SELECT * FROM programs WHERE {search_type} LIKE %s"
    #         elif entity_type == "college":
    #             sql = f"SELECT * FROM colleges WHERE {search_type} LIKE %s"
    #     else:
    #         sql = ""
    #         values = ()
    #
    #         if entity_type == "student":
    #             sql = ("SELECT * FROM students "
    #                    "WHERE id_number LIKE %s OR "
    #                    "first_name LIKE %s OR "
    #                    "last_name LIKE %s OR "
    #                    "year_level LIKE %s OR "
    #                    "gender LIKE %s OR "
    #                    "program_code LIKE %s")
    #
    #             values = (f"{search_text}%",
    #                       f"{search_text}%",
    #                       f"{search_text}%",
    #                       f"{search_text}%",
    #                       f"{search_text}%",
    #                       f"{search_text}%")
    #
    #     self.cursor.execute(sql, values)
    #     results = self.cursor.fetchall()
    #
    #     entities_data = []
    #
    #     for row in results:
    #         list_row = list(row)
    #
    #         if entity_type == 'student' and not list_row[5]:
    #             list_row[5] = "N/A"
    #         elif entity_type == 'program' and not list_row[2]:
    #             list_row[2] = "N/A"
    #
    #         entities_data.append(list_row)
    #
    #     return entities_data

    def add_entity(self, entity_data, entity_type):
        sql = ""
        values = ()

        if entity_type == 'student':
            sql = ("INSERT INTO students (id_number, first_name, last_name, year_level, gender, program_code)"
                   "VALUES (%s, %s, %s, %s, %s, %s)")

            values = (entity_data[0],
                      entity_data[1],
                      entity_data[2],
                      entity_data[3],
                      entity_data[4],
                      entity_data[5])

        elif entity_type == 'program':
            sql = ("INSERT INTO programs (program_code, program_name, college_code)"
                   "VALUES (%s, %s, %s)")

            values = (entity_data[0],
                      entity_data[1],
                      entity_data[2])

        elif entity_type == 'college':
            sql = ("INSERT INTO colleges (college_code, college_name)"
                   "VALUES (%s, %s)")

            values = (entity_data[0],
                      entity_data[1])

        self.cursor.execute(sql, values)

        self.db.commit()

    def update_entity(self, identifier, entity_to_edit, entity_type):
        # Identifier is the primary key of each table

        sql = ""
        values = ()

        if entity_type == 'student':
            sql = ("UPDATE students SET id_number=%s, first_name=%s, last_name=%s, "
                   "year_level=%s, gender=%s, program_code=%s WHERE id_number=%s")

            values = (entity_to_edit[0],
                      entity_to_edit[1],
                      entity_to_edit[2],
                      entity_to_edit[3],
                      entity_to_edit[4],
                      entity_to_edit[5],
                      identifier)

        elif entity_type == 'program':
            sql = ("UPDATE programs SET program_code=%s, program_name=%s, "
                   "college_code=%s WHERE program_code=%s")

            values = (entity_to_edit[0],
                      entity_to_edit[1],
                      entity_to_edit[2],
                      identifier)

        elif entity_type == 'college':
            sql = ("UPDATE colleges SET college_code=%s, college_name=%s "
                   "WHERE college_code=%s")

            values = (entity_to_edit[0],
                      entity_to_edit[1],
                      identifier)

        self.cursor.execute(sql, values)

        self.db.commit()

    def delete_entity(self, identifier, entity_type):
        # Identifier is the primary key of each table

        sql = ""
        values = ()

        if entity_type == 'student':
            sql = "DELETE FROM students WHERE id_number=%s"

            # Has an extra comma because this is a tuple
            values = (identifier,)

        elif entity_type == 'program':
            sql = "DELETE FROM programs WHERE program_code=%s"

            values = (identifier,)

        elif entity_type == 'college':
            sql = "DELETE FROM colleges WHERE college_code=%s"

            values = (identifier,)

        self.cursor.execute(sql, values)

        self.db.commit()
