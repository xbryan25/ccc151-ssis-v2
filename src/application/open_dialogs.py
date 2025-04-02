from utils.specific_buttons_enabler import SpecificButtonsEnabler
from utils.save_all_changes import SaveAllChanges

from helper_dialogs.input_prerequisite.input_prerequisite import InputPrerequisiteDialog
from helper_dialogs.save_item_state.confirm_save import ConfirmSaveDialog
from helper_dialogs.save_item_state.success_save_changes import SuccessSaveChangesDialog

from operation_dialogs.students.add_student import AddStudentDialog
from operation_dialogs.students.edit_student import EditStudentDialog
from operation_dialogs.students.delete_student import DeleteStudentDialog
from operation_dialogs.students.students_demographic import StudentsDemographicDialog

from operation_dialogs.programs.add_program import AddProgramDialog
from operation_dialogs.programs.edit_program import EditProgramDialog
from operation_dialogs.programs.delete_program import DeleteProgramDialog
from operation_dialogs.programs.programs_demographic import ProgramsDemographicDialog

from operation_dialogs.colleges.add_college import AddCollegeDialog
from operation_dialogs.colleges.edit_college import EditCollegeDialog
from operation_dialogs.colleges.delete_college import DeleteCollegeDialog
from operation_dialogs.colleges.colleges_demographic import CollegesDemographicDialog


class OpenDialogs:

    @staticmethod
    def open_add_entity_dialog_for_students(students_table_view, students_table_model, view_demographics_button,
                                            reset_item_delegates_func):

        if len(students_table_model.db_handler.get_all_entities('program')) > 0:

            add_student_dialog = AddStudentDialog(students_table_view, students_table_model, reset_item_delegates_func)
            add_student_dialog.exec()

            SpecificButtonsEnabler.enable_buttons([view_demographics_button],
                                                  students_table_model)

            # SpecificButtonsEnabler.enable_save_button(save_changes_button,
            #                                           students_table_model=students_table_model)

        else:
            input_programs_dialog = InputPrerequisiteDialog("programs")
            input_programs_dialog.exec()

    @staticmethod
    def open_add_entity_dialog_for_programs(programs_table_view, programs_table_model, view_demographics_button,
                                            reset_item_delegates_func):

        if len(programs_table_model.db_handler.get_all_entities('colleges')) > 0:
            # Note: reset_item_delegates is a function

            add_program_dialog = AddProgramDialog(programs_table_view, programs_table_model, reset_item_delegates_func)
            add_program_dialog.exec()

            SpecificButtonsEnabler.enable_buttons([view_demographics_button],
                                                  programs_table_model)

            # SpecificButtonsEnabler.enable_save_button(save_changes_button,
            #                                           programs_table_model=programs_table_model)

        else:
            input_college_dialog = InputPrerequisiteDialog("college")
            input_college_dialog.exec()

    @staticmethod
    def open_add_entity_dialog_for_colleges(colleges_table_view, colleges_table_model, view_demographics_button,
                                            reset_item_delegates_func):

        add_college_dialog = AddCollegeDialog(colleges_table_view, colleges_table_model, reset_item_delegates_func)
        add_college_dialog.exec()

        SpecificButtonsEnabler.enable_buttons([view_demographics_button],
                                              colleges_table_model)

        # SpecificButtonsEnabler.enable_save_button(save_changes_button,
        #                                           colleges_table_model=colleges_table_model)

    @staticmethod
    def open_students_demographic_dialog(students_table_model):

        students_demographic_dialog = StudentsDemographicDialog(students_table_model)

        students_demographic_dialog.exec()

    @staticmethod
    def open_programs_demographic_dialog(programs_table_model):

        programs_demographic_dialog = ProgramsDemographicDialog(programs_table_model)

        programs_demographic_dialog.exec()

    @staticmethod
    def open_colleges_demographic_dialog(colleges_table_model):

        colleges_demographic_dialog = CollegesDemographicDialog(colleges_table_model)

        colleges_demographic_dialog.exec()
