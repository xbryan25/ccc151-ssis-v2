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

    def get_count_of_all_entities(self, entity_type):

        if entity_type == "student":
            self.cursor.execute("SELECT COUNT(*) FROM students;")
        elif entity_type == "program":
            self.cursor.execute("SELECT COUNT(*) FROM programs")
        elif entity_type == "college":
            self.cursor.execute("SELECT COUNT(*) FROM colleges")

        results = self.cursor.fetchall()

        return results[0][0]

    def get_count_of_all_students_in_program(self, program_code):

        self.cursor.execute(f"SELECT COUNT(*) FROM students WHERE program_code='{program_code}';")
        results = self.cursor.fetchall()

        return results[0][0]

    def get_count_of_all_students_in_college(self, college_code):
        self.cursor.execute(f"""SELECT COUNT(*) AS student_count
                            FROM students
                            JOIN programs ON students.program_code = programs.program_code
                            JOIN colleges ON programs.college_code = colleges.college_code
                            WHERE colleges.college_code = '{college_code}';
                            """)

        results = self.cursor.fetchall()

        return results[0][0]

    def get_count_of_all_programs_in_college(self, college_code):

        self.cursor.execute(f"SELECT COUNT(*) FROM programs WHERE college_code='{college_code}';")
        results = self.cursor.fetchall()

        return results[0][0]

    def get_count_of_gender(self, identifier=None, entity_type="student"):

        gender_count = {"Male": 0, "Female": 0, "Others": 0, "Prefer not to say": 0}

        if entity_type == "student":
            self.cursor.execute("""
                    SELECT gender, COUNT(*) 
                    FROM students 
                    GROUP BY gender;""")

        elif entity_type == "program":
            self.cursor.execute("""
                    SELECT gender, COUNT(*) 
                    FROM students 
                    WHERE program_code = %s 
                    GROUP BY gender;
                """, (identifier,))

        elif entity_type == "college":
            self.cursor.execute("""
                                SELECT gender, COUNT(*)
                                FROM students
                                JOIN programs ON students.program_code = programs.program_code
                                JOIN colleges ON programs.college_code = colleges.college_code
                                WHERE colleges.college_code = %s
                                GROUP BY gender;
                                """, (identifier,))

        results = self.cursor.fetchall()

        for gender, count in results:
            gender_count[gender] += count

        return gender_count

    def get_count_of_year_level(self, identifier=None, entity_type="student"):

        year_level_count = {"1st": 0, "2nd": 0, "3rd": 0, "4th": 0, "5th": 0}

        if entity_type == "student":
            self.cursor.execute("""
                    SELECT year_level, COUNT(*) 
                    FROM students 
                    GROUP BY year_level;""")

        elif entity_type == "program":
            self.cursor.execute("""
                                SELECT year_level, COUNT(*) 
                                FROM students 
                                WHERE program_code = %s 
                                GROUP BY year_level;
                                """, (identifier,))

        elif entity_type == "college":
            self.cursor.execute("""
                               SELECT year_level, COUNT(*)
                               FROM students
                               JOIN programs ON students.program_code = programs.program_code
                               JOIN colleges ON programs.college_code = colleges.college_code
                               WHERE colleges.college_code = %s
                               GROUP BY year_level;
                               """, (identifier,))

        results = self.cursor.fetchall()

        for year_level, count in results:
            year_level_count[year_level] += count

        return year_level_count

    def get_entities(self, max_row_per_page, current_page_number, entity_type):

        print(f"------Query - max_row_per_page: {max_row_per_page}, current_page_number: {current_page_number}------")

        entities_data = []

        sql = ""
        values = (max_row_per_page, (current_page_number - 1) * max_row_per_page)

        if entity_type == "student":
            sql = "SELECT * FROM students LIMIT %s OFFSET %s"
        elif entity_type == "program":
            sql = "SELECT * FROM programs LIMIT %s OFFSET %s"
        elif entity_type == "college":
            sql = "SELECT * FROM colleges LIMIT %s OFFSET %s"

        self.cursor.execute(sql, values)
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

    def get_sorted_entities(self, max_row_per_page, current_page_number, entity_type, sort_column, sort_order):
        sql = f"SELECT * FROM {entity_type + "s"} ORDER BY {sort_column} IS NULL, {sort_column}"

        if sort_order == "ascending":
            sql += " ASC"
        else:
            sql += " DESC"

        sql += f" LIMIT {max_row_per_page} OFFSET {(current_page_number - 1) * max_row_per_page}"

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

    def get_sorted_filtered_entities(self, max_row_per_page, current_page_number, entity_type, sort_column, sort_order,
                                     search_type, search_method, search_text):

        like_or_equals = "LIKE"
        left_percent_sign = ""
        right_percent_sign = ""

        if search_method == "contains":
            left_percent_sign = "%"
            right_percent_sign = "%"
        elif search_method == "starts_with":
            left_percent_sign = ""
            right_percent_sign = "%"
        elif search_method == "ends_with":
            left_percent_sign = "%"
            right_percent_sign = ""
        elif search_method == "exactly_match":
            like_or_equals = "="
            left_percent_sign = ""
            right_percent_sign = ""

        if search_type != "all":
            sql = f"SELECT * FROM {entity_type + "s"} WHERE {search_type} {like_or_equals} %s"
            values = (f"{left_percent_sign}{search_text}{right_percent_sign}", max_row_per_page,
                      (current_page_number - 1) * max_row_per_page)
        else:
            sql = ""
            values = ()

            if entity_type == "student":
                sql = ("SELECT * FROM students "
                       f"WHERE id_number {like_or_equals} %s OR "
                       f"first_name {like_or_equals} %s OR "
                       f"last_name {like_or_equals} %s OR "
                       f"year_level {like_or_equals} %s OR "
                       f"gender {like_or_equals} %s OR "
                       f"program_code {like_or_equals} %s")

                values = (f"{left_percent_sign}{search_text}{right_percent_sign}",
                          f"{left_percent_sign}{search_text}{right_percent_sign}",
                          f"{left_percent_sign}{search_text}{right_percent_sign}",
                          f"{left_percent_sign}{search_text}{right_percent_sign}",
                          f"{left_percent_sign}{search_text}{right_percent_sign}",
                          f"{left_percent_sign}{search_text}{right_percent_sign}",
                          max_row_per_page,
                          (current_page_number - 1) * max_row_per_page)

            elif entity_type == "program":
                sql = ("SELECT * FROM programs "
                       f"WHERE program_code {like_or_equals} %s OR "
                       f"program_name {like_or_equals} %s OR "
                       f"college_code {like_or_equals} %s")

                values = (f"{left_percent_sign}{search_text}{right_percent_sign}",
                          f"{left_percent_sign}{search_text}{right_percent_sign}",
                          f"{left_percent_sign}{search_text}{right_percent_sign}",
                          max_row_per_page,
                          (current_page_number - 1) * max_row_per_page)

            elif entity_type == "college":
                sql = ("SELECT * FROM colleges "
                       f"WHERE college_code {like_or_equals} %s OR "
                       f"college_name {like_or_equals} %s")

                values = (f"{left_percent_sign}{search_text}{right_percent_sign}",
                          f"{left_percent_sign}{search_text}{right_percent_sign}",
                          max_row_per_page,
                          (current_page_number - 1) * max_row_per_page)

        if sort_column and sort_order and sort_order != "-":
            if sort_order == "ascending":
                sql += f" ORDER BY {sort_column} IS NULL, {sort_column} ASC"
            elif sort_order == "descending":
                sql += f" ORDER BY {sort_column} IS NULL, {sort_column} DESC"

        sql += f" LIMIT %s OFFSET %s"

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

    def get_count_of_sorted_filtered_entities(self, entity_type, search_type, search_method,  search_text):

        like_or_equals = "LIKE"
        left_percent_sign = ""
        right_percent_sign = ""

        if search_method == "contains":
            left_percent_sign = "%"
            right_percent_sign = "%"
        elif search_method == "starts_with":
            left_percent_sign = ""
            right_percent_sign = "%"
        elif search_method == "ends_with":
            left_percent_sign = "%"
            right_percent_sign = ""
        elif search_method == "exactly_match":
            like_or_equals = "="
            left_percent_sign = ""
            right_percent_sign = ""

        if search_type != "all":
            sql = f"SELECT COUNT(*) AS total FROM {entity_type + "s"} WHERE {search_type} {like_or_equals} %s"
            values = (f"{left_percent_sign}{search_text}{right_percent_sign}",)
        else:
            sql = ""
            values = ()

            if entity_type == "student":
                sql = ("SELECT COUNT(*) AS total FROM students "
                       f"WHERE id_number {like_or_equals} %s OR "
                       f"first_name {like_or_equals} %s OR "
                       f"last_name {like_or_equals} %s OR "
                       f"year_level {like_or_equals} %s OR "
                       f"gender {like_or_equals} %s OR "
                       f"program_code {like_or_equals} %s")

                values = (f"{left_percent_sign}{search_text}{right_percent_sign}",
                          f"{left_percent_sign}{search_text}{right_percent_sign}",
                          f"{left_percent_sign}{search_text}{right_percent_sign}",
                          f"{left_percent_sign}{search_text}{right_percent_sign}",
                          f"{left_percent_sign}{search_text}{right_percent_sign}",
                          f"{left_percent_sign}{search_text}{right_percent_sign}")

            elif entity_type == "program":
                sql = ("SELECT COUNT(*) AS total FROM programs "
                       f"WHERE program_code {like_or_equals} %s OR "
                       f"program_name {like_or_equals} %s OR "
                       f"college_code {like_or_equals} %s")

                values = (f"{left_percent_sign}{search_text}{right_percent_sign}",
                          f"{left_percent_sign}{search_text}{right_percent_sign}",
                          f"{left_percent_sign}{search_text}{right_percent_sign}")

            elif entity_type == "college":
                sql = ("SELECT COUNT(*) AS total FROM colleges "
                       f"WHERE college_code {like_or_equals} %s OR "
                       f"college_name {like_or_equals} %s")

                values = (f"{left_percent_sign}{search_text}{right_percent_sign}",
                          f"{left_percent_sign}{search_text}{right_percent_sign}")

        self.cursor.execute(sql, values)
        results = self.cursor.fetchone()[0]

        return results

    def check_if_id_number_exists(self, id_number):
        sql = "SELECT 1 FROM students WHERE id_number = %s LIMIT 1;"
        self.cursor.execute(sql, (id_number,))
        result = self.cursor.fetchone()

        if result:
            return True
        else:
            return False

    def check_if_name_combination_exists(self, first_name, last_name):
        sql = "SELECT 1 FROM students WHERE first_name = %s and last_name = %s LIMIT 1;"
        self.cursor.execute(sql, (first_name, last_name))
        result = self.cursor.fetchone()

        if result:
            return True
        else:
            return False

    def check_if_program_code_exists(self, program_code):
        sql = "SELECT 1 FROM programs WHERE program_code = %s LIMIT 1;"
        self.cursor.execute(sql, (program_code,))
        result = self.cursor.fetchone()

        if result:
            return True
        else:
            return False

    def check_if_program_name_exists(self, program_name):
        sql = "SELECT 1 FROM programs WHERE program_name = %s LIMIT 1;"
        self.cursor.execute(sql, (program_name,))
        result = self.cursor.fetchone()

        if result:
            return True
        else:
            return False

    def check_if_college_code_exists(self, college_code):
        sql = "SELECT 1 FROM colleges WHERE college_code = %s LIMIT 1;"
        self.cursor.execute(sql, (college_code,))
        result = self.cursor.fetchone()

        if result:
            return True
        else:
            return False

    def check_if_college_name_exists(self, college_name):
        sql = "SELECT 1 FROM colleges WHERE college_name = %s LIMIT 1;"
        self.cursor.execute(sql, (college_name,))
        result = self.cursor.fetchone()

        if result:
            return True
        else:
            return False

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

        # self.db.commit()

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

        # self.db.commit()

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

        # self.db.commit()

    def commit_changes(self):
        self.db.commit()

    def rollback_changes(self):
        self.db.rollback()
