

class InitializeDatabase:
    def __init__(self, db, cursor):

        self.db = db
        self.cursor = cursor

        self.create_database()

        self.db.select_db("ssis_db")

        self.create_relations()

    def create_database(self):
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS ssis_db")

    def create_relations(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS `students` (
                              `id_number` char(9) NOT NULL,
                              `first_name` varchar(50) NOT NULL,
                              `last_name` varchar(50) NOT NULL,
                              `year_level` varchar(4) NOT NULL,
                              `gender` varchar(20) NOT NULL,
                              `program_code` varchar(15) DEFAULT NULL,
                              PRIMARY KEY (`id_number`),
                              UNIQUE KEY `UC_name_combination` (`first_name`,`last_name`),
                              KEY `IDX_program_code` (`program_code`),
                              KEY `IDX_gender` (`gender`),
                              KEY `IDX_year_level` (`year_level`),
                              CONSTRAINT `fk_program_code` FOREIGN KEY (`program_code`) REFERENCES `programs` (`program_code`) ON DELETE SET NULL ON UPDATE CASCADE
                            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
                            """)

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS `programs` (
                              `program_code` varchar(15) NOT NULL,
                              `program_name` varchar(50) NOT NULL,
                              `college_code` varchar(15) DEFAULT NULL,
                              PRIMARY KEY (`program_code`),
                              UNIQUE KEY `UC_program_name` (`program_name`),
                              KEY `IDX_college_code` (`college_code`),
                              CONSTRAINT `college_code` FOREIGN KEY (`college_code`) REFERENCES `colleges` (`college_code`) ON DELETE SET NULL ON UPDATE CASCADE
                            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
                            """)

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS `colleges` (
                              `college_code` varchar(10) NOT NULL,
                              `college_name` varchar(50) NOT NULL,
                              PRIMARY KEY (`college_code`),
                              UNIQUE KEY `UC_college_code` (`college_code`),
                              UNIQUE KEY `UC_college_name` (`college_name`)
                            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
                            """)
