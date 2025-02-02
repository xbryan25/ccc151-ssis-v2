import csv


class GetExistingInformation:

    @staticmethod
    def from_students():
        students_information = {"ID Number": [], "Full Name": []}

        with open("databases/students.csv", 'r') as from_students_csv:
            reader = csv.reader(from_students_csv)

            for row in reader:
                students_information["ID Number"].append(row[0])
                students_information["Full Name"].append(f"{row[1].strip()} {row[2].strip()}")

        return students_information

    @staticmethod
    def from_programs():
        programs_information = {"Program Code": [], "Program Name": []}

        with open("databases/programs.csv", 'r') as from_programs_csv:
            reader = csv.reader(from_programs_csv)

            for row in reader:
                programs_information["Program Code"].append(row[0])
                programs_information["Program Name"].append(row[1].replace("_", ","))

        return programs_information

    @staticmethod
    def from_colleges():
        colleges_information = {"College Code": [], "College Name": []}

        with open("databases/colleges.csv", 'r') as from_colleges_csv:
            reader = csv.reader(from_colleges_csv)

            for row in reader:
                colleges_information["College Code"].append(row[0])
                colleges_information["College Name"].append(row[1].replace("_", ","))

        return colleges_information
