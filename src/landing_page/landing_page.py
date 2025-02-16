from PyQt6.QtWidgets import QMainWindow

from landing_page.landing_page_design import Ui_MainWindow as LandingPageUI

from students.students_page import StudentsPage
from programs.programs_page import ProgramsPage
from colleges.colleges_page import CollegesPage

from utils.load_information_from_database import LoadInformationFromDatabase
from utils.custom_table_model import CustomTableModel
from utils.save_all_changes import SaveAllChanges
from utils.adjust_horizontal_header import AdjustHorizontalHeader

from helper_dialogs.save_item_state.confirm_save import ConfirmSaveDialog
from helper_dialogs.save_item_state.success_save_changes import SuccessSaveChangesDialog


class LandingPage(QMainWindow, LandingPageUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.adjust_horizontal_header = AdjustHorizontalHeader()

        # Load information from database upon entering the landing page for the first time
        self.students_data = LoadInformationFromDatabase.get_students()
        self.programs_data = LoadInformationFromDatabase.get_programs()
        self.colleges_data = LoadInformationFromDatabase.get_colleges()

        # Generate table models in landing page so that it can be accessed in different pages
        self.students_table_model = CustomTableModel(self.students_data, "student")

        self.programs_table_model = CustomTableModel(self.programs_data, "program")
        self.programs_table_model.set_students_data(self.students_table_model.get_data())

        self.colleges_table_model = CustomTableModel(self.colleges_data, "college")
        self.colleges_table_model.set_students_data(self.students_table_model.get_data())
        self.colleges_table_model.set_programs_data(self.programs_table_model.get_data())


        # ---Undo stack here---
        # self.undo_stack = UndoStack()

        # Create pages
        self.students_page = StudentsPage(self, self.students_table_model, self.programs_table_model,
                                          self.colleges_table_model)
        self.programs_page = ProgramsPage(self, self.students_table_model, self.programs_table_model,
                                          self.colleges_table_model)
        self.colleges_page = CollegesPage(self, self.students_table_model, self.programs_table_model,
                                          self.colleges_table_model)

        self.add_signals()

    def open_students_page(self):
        self.adjust_horizontal_header.for_students_table_view(self.students_page.horizontal_header)

        self.students_page.reset_item_delegates()

        self.students_page.show()

        self.hide()

    def open_programs_page(self):
        self.adjust_horizontal_header.for_programs_table_view(self.programs_page.horizontal_header)

        self.programs_page.reset_item_delegates()

        self.programs_page.show()

        self.hide()

    def open_colleges_page(self):
        self.adjust_horizontal_header.for_colleges_table_view(self.colleges_page.horizontal_header)
        self.colleges_page.show()
        self.hide()

    def open_confirm_save_dialog(self, save_type):
        self.confirm_save_dialog = ConfirmSaveDialog()
        self.confirm_save_dialog.exec()

        if self.confirm_save_dialog.get_confirm_edit_decision():
            self.save_all_changes = SaveAllChanges(save_type, self.students_table_model.get_data())

            self.save_all_changes.to_csv()

            self.success_save_changes = SuccessSaveChangesDialog()
            self.success_save_changes.exec()

    def add_signals(self):
        self.students_button.clicked.connect(self.open_students_page)
        self.programs_button.clicked.connect(self.open_programs_page)
        self.colleges_button.clicked.connect(self.open_colleges_page)

    def closeEvent(self, event):

        if self.colleges_table_model.get_has_changes():
            self.open_confirm_save_dialog("college")

        elif self.programs_table_model.get_has_changes():
            self.open_confirm_save_dialog("program")

        elif self.students_table_model.get_has_changes():
            self.open_confirm_save_dialog("student")

        event.accept()
