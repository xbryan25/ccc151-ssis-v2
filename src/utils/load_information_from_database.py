import pymysql


class LoadInformationFromDatabase:
    
    def __init__(self):
        self.db = pymysql.connect(
            host='localhost',
            user='root',
            password='root',
            database='ssis_db'
        )
        
        self.cursor = self.db.cursor()
    
    def get_students(self):
        students_data = []

        self.cursor.execute("SELECT * FROM students")
        result = self.cursor.fetchall()

        for row in result:
            students_data.append(list(row))

        return students_data

    def get_programs(self):
        programs_data = []

        self.cursor.execute("SELECT * FROM programs")
        result = self.cursor.fetchall()

        for row in result:
            programs_data.append(list(row))

        return programs_data

    def get_colleges(self):
        colleges_data = []

        self.cursor.execute("SELECT * FROM colleges")
        result = self.cursor.fetchall()

        for row in result:
            colleges_data.append(list(row))

        return colleges_data

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
