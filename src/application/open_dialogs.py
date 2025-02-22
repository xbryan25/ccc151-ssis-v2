from utils.specific_buttons_enabler import SpecificButtonsEnabler
from utils.save_all_changes import SaveAllChanges

from helper_dialogs.input_prerequisite.input_prerequisite import InputPrerequisiteDialog
from helper_dialogs.save_item_state.confirm_save import ConfirmSaveDialog
from helper_dialogs.save_item_state.success_save_changes import SuccessSaveChangesDialog

from students.add_student import AddStudentDialog
from students.edit_student import EditStudentDialog
from students.delete_student import DeleteStudentDialog
from students.students_demographic import StudentsDemographicDialog

from programs.add_program import AddProgramDialog
from programs.edit_program import EditProgramDialog
from programs.delete_program import DeleteProgramDialog
from programs.programs_demographic import ProgramsDemographicDialog

from colleges.add_college import AddCollegeDialog
from colleges.edit_college import EditCollegeDialog
from colleges.delete_college import DeleteCollegeDialog
from colleges.colleges_demographic import CollegesDemographicDialog


class OpenDialogs:

    @staticmethod
    def open_add_entity_dialog_for_students(students_table_view, students_table_model, programs_table_model,
                                            colleges_table_model, delete_entity_button, edit_entity_button,
                                            save_changes_button, view_demographics_button, reset_item_delegates_func):

        if programs_table_model.get_data()[0][0] != "":

            add_student_dialog = AddStudentDialog(students_table_view, students_table_model,
                                                  programs_table_model, colleges_table_model, reset_item_delegates_func)
            add_student_dialog.exec()

            SpecificButtonsEnabler.enable_delete_and_edit_buttons([delete_entity_button,
                                                                  edit_entity_button,
                                                                  view_demographics_button],
                                                                  students_table_model)

            SpecificButtonsEnabler.enable_save_button(save_changes_button,
                                                      students_table_model)

        else:
            input_programs_dialog = InputPrerequisiteDialog("programs")
            input_programs_dialog.exec()

    @staticmethod
    def open_add_entity_dialog_for_programs(programs_table_view, programs_table_model,
                                            colleges_table_model, delete_entity_button, edit_entity_button,
                                            save_changes_button, view_demographics_button, reset_item_delegates_func):

        if colleges_table_model.get_data()[0][0] != "":
            # Note: reset_item_delegates is a function

            add_program_dialog = AddProgramDialog(programs_table_view, programs_table_model,
                                                  colleges_table_model, reset_item_delegates_func)
            add_program_dialog.exec()

            SpecificButtonsEnabler.enable_delete_and_edit_buttons([delete_entity_button,
                                                                   edit_entity_button,
                                                                   view_demographics_button],
                                                                  programs_table_model)

            SpecificButtonsEnabler.enable_save_button(save_changes_button,
                                                      programs_table_model)

        else:
            input_college_dialog = InputPrerequisiteDialog("college")
            input_college_dialog.exec()

    @staticmethod
    def open_add_entity_dialog_for_colleges(colleges_table_view, colleges_table_model, delete_entity_button,
                                            edit_entity_button, save_changes_button, view_demographics_button):

        add_college_dialog = AddCollegeDialog(colleges_table_view, colleges_table_model)
        add_college_dialog.exec()

        SpecificButtonsEnabler.enable_delete_and_edit_buttons([delete_entity_button,
                                                               edit_entity_button,
                                                               view_demographics_button],
                                                              students_table_model)

        SpecificButtonsEnabler.enable_save_button(save_changes_button, colleges_table_model)

    @staticmethod
    def open_edit_entity_dialog_for_students(students_table_view, students_table_model, programs_table_model,
                                            colleges_table_model, save_changes_button, reset_item_delegates_func):

        edit_student_dialog = EditStudentDialog(students_table_view, students_table_model, programs_table_model,
                                                colleges_table_model, reset_item_delegates_func)
        edit_student_dialog.exec()

        SpecificButtonsEnabler.enable_save_button(save_changes_button, students_table_model)

    @staticmethod
    def open_edit_entity_dialog_for_programs(programs_table_view, programs_table_model, students_table_model,
                                             colleges_table_model, save_changes_button, reset_item_delegates_func):

        edit_program_dialog = EditProgramDialog(programs_table_view, programs_table_model, students_table_model,
                                                colleges_table_model, reset_item_delegates_func)
        edit_program_dialog.exec()

        SpecificButtonsEnabler.enable_save_button(save_changes_button,
                                                  programs_table_model)

    @staticmethod
    def open_edit_entity_dialog_for_colleges(colleges_table_view, programs_table_model,
                                             colleges_table_model, save_changes_button):

        edit_college_dialog = EditCollegeDialog(colleges_table_view, colleges_table_model, programs_table_model)
        edit_college_dialog.exec()

        SpecificButtonsEnabler.enable_save_button(save_changes_button, colleges_table_model)

    @staticmethod
    def open_delete_entity_dialog_for_students(students_table_view, students_table_model, delete_entity_button,
                                               edit_entity_button, save_changes_button, view_demographics_button,
                                               reset_item_delegates_func, horizontal_header):

        # Pass tableview here, and just import adjust horizontal header

        delete_student_dialog = DeleteStudentDialog(students_table_view, students_table_model,
                                                    reset_item_delegates_func, horizontal_header)
        delete_student_dialog.exec()

        SpecificButtonsEnabler.enable_delete_and_edit_buttons([delete_entity_button,
                                                               edit_entity_button,
                                                               view_demographics_button],
                                                              students_table_model)

        SpecificButtonsEnabler.enable_save_button(save_changes_button, students_table_model)

    @staticmethod
    def open_delete_entity_dialog_for_programs(programs_table_view, programs_table_model, students_table_model,
                                               colleges_table_model, delete_entity_button, edit_entity_button,
                                               save_changes_button, view_demographics_button,
                                               reset_item_delegates_func, horizontal_header):

        delete_program_dialog = DeleteProgramDialog(programs_table_view,
                                                    programs_table_model,
                                                    students_table_model,
                                                    colleges_table_model,
                                                    reset_item_delegates_func,
                                                    horizontal_header)
        delete_program_dialog.exec()

        SpecificButtonsEnabler.enable_delete_and_edit_buttons([delete_entity_button,
                                                               edit_entity_button,
                                                               view_demographics_button],
                                                              students_table_model)

        SpecificButtonsEnabler.enable_save_button(save_changes_button, programs_table_model)

    @staticmethod
    def open_delete_entity_dialog_for_colleges(colleges_table_view, colleges_table_model, students_table_model,
                                               programs_table_model, delete_entity_button, edit_entity_button,
                                               save_changes_button, view_demographics_button,
                                               reset_item_delegates_func, horizontal_header):

        delete_college_dialog = DeleteCollegeDialog(colleges_table_view, colleges_table_model,
                                                    students_table_model, programs_table_model,
                                                    reset_item_delegates_func, horizontal_header)

        delete_college_dialog.exec()

        SpecificButtonsEnabler.enable_delete_and_edit_buttons([delete_entity_button,
                                                               edit_entity_button,
                                                               view_demographics_button],
                                                              students_table_model)

        SpecificButtonsEnabler.enable_save_button(save_changes_button, colleges_table_model)

    @staticmethod
    def open_confirm_save_dialog(entity_type, students_table_model, programs_table_model, colleges_table_model,
                                 save_changes_button=None):
        confirm_save_dialog = ConfirmSaveDialog()
        confirm_save_dialog.exec()

        if confirm_save_dialog.get_confirm_edit_decision():
            save_all_changes = SaveAllChanges(entity_type, students_table_model, programs_table_model,
                                              colleges_table_model)

            save_all_changes.to_csv()

            if entity_type == "student" and save_changes_button:
                SpecificButtonsEnabler.enable_save_button(save_changes_button, students_table_model)
            elif entity_type == "program" and save_changes_button:
                SpecificButtonsEnabler.enable_save_button(save_changes_button, programs_table_model)
            elif entity_type == "college" and save_changes_button:
                SpecificButtonsEnabler.enable_save_button(save_changes_button, colleges_table_model)

            success_save_changes = SuccessSaveChangesDialog()
            success_save_changes.exec()

    @staticmethod
    def open_students_demographic_dialog(students_table_model, programs_table_model, colleges_table_model):
        students_demographic_dialog = StudentsDemographicDialog(students_table_model, programs_table_model,
                                                                colleges_table_model)

        students_demographic_dialog.exec()

    @staticmethod
    def open_programs_demographic_dialog(students_table_model, programs_table_model, colleges_table_model):
        programs_demographic_dialog = ProgramsDemographicDialog(students_table_model, programs_table_model,
                                                                colleges_table_model)

        programs_demographic_dialog.exec()

    @staticmethod
    def open_colleges_demographic_dialog(students_table_model, programs_table_model, colleges_table_model):
        colleges_demographic_dialog = CollegesDemographicDialog(students_table_model, programs_table_model,
                                                                colleges_table_model)

        colleges_demographic_dialog.exec()
