from PyQt6.QtWidgets import QDialog

from student.add_student_design import Ui_Dialog as AddStudentUI


class AddStudentDialog(QDialog, AddStudentUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.pushButton.clicked.connect(self.add_student_to_csv)

    def add_student_to_csv(self):
        print("Student has been added")