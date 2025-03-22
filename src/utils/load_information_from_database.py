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
