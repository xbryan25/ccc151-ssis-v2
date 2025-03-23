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

        result = self.cursor.fetchall()

        for row in result:
            list_row = list(row)

            if entity_type == 'student' and not list_row[5]:
                list_row[5] = "N/A"
            elif entity_type == 'program' and not list_row[2]:
                list_row[2] = "N/A"

            entities_data.append(list_row)

        return entities_data

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
