from helper_dialogs.input_prerequisite.input_prerequisite import InputPrerequisiteDialog

from operation_dialogs.students.add_student import AddStudentDialog
from operation_dialogs.programs.add_program import AddProgramDialog
from operation_dialogs.colleges.add_college import AddCollegeDialog


class OpenDialogs:

    @staticmethod
    def open_add_entity_dialog_for_students(students_table_view, students_table_model, view_demographics_button,
                                            reset_item_delegates_func):

        if len(students_table_model.db_handler.get_all_entities('program')) > 0:

            add_student_dialog = AddStudentDialog(students_table_view, students_table_model, reset_item_delegates_func)
            add_student_dialog.exec()

        else:
            input_programs_dialog = InputPrerequisiteDialog("programs")
            input_programs_dialog.exec()

    @staticmethod
    def open_add_entity_dialog_for_programs(programs_table_view, programs_table_model, view_demographics_button,
                                            reset_item_delegates_func):

        if len(programs_table_model.db_handler.get_all_entities('college')) > 0:
            # Note: reset_item_delegates is a function

            add_program_dialog = AddProgramDialog(programs_table_view, programs_table_model, reset_item_delegates_func)
            add_program_dialog.exec()


        else:
            input_college_dialog = InputPrerequisiteDialog("college")
            input_college_dialog.exec()

    @staticmethod
    def open_add_entity_dialog_for_colleges(colleges_table_view, colleges_table_model, view_demographics_button,
                                            reset_item_delegates_func):

        add_college_dialog = AddCollegeDialog(colleges_table_view, colleges_table_model, reset_item_delegates_func)
        add_college_dialog.exec()


