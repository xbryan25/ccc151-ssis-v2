from helper_dialogs.input_prerequisite.input_prerequisite import InputPrerequisiteDialog
from helper_dialogs.save_or_undo_state.confirm_save_or_undo import ConfirmSaveOrUndoDialog
from helper_dialogs.save_or_undo_state.success_save_changes import SuccessSaveChangesDialog

from operation_dialogs.add_entity.add_student import AddStudentDialog
from operation_dialogs.add_entity.add_program import AddProgramDialog
from operation_dialogs.add_entity.add_college import AddCollegeDialog

from utils.specific_buttons_enabler import SpecificButtonsEnabler


class OpenDialogs:

    @staticmethod
    def open_add_entity_dialog_for_students(students_table_view, students_table_model, save_changes_button,
                                            undo_all_changes_button, reset_item_delegates_func):

        if len(students_table_model.db_handler.get_all_entities('program')) > 0:

            add_student_dialog = AddStudentDialog(students_table_view, students_table_model, save_changes_button,
                                                  undo_all_changes_button, reset_item_delegates_func)
            add_student_dialog.exec()

        else:
            input_programs_dialog = InputPrerequisiteDialog("programs")
            input_programs_dialog.exec()

    @staticmethod
    def open_add_entity_dialog_for_programs(programs_table_view, programs_table_model, save_changes_button,
                                            undo_all_changes_button, reset_item_delegates_func):

        if len(programs_table_model.db_handler.get_all_entities('college')) > 0:
            # Note: reset_item_delegates is a function

            add_program_dialog = AddProgramDialog(programs_table_view, programs_table_model, save_changes_button,
                                                  undo_all_changes_button, reset_item_delegates_func)
            add_program_dialog.exec()


        else:
            input_college_dialog = InputPrerequisiteDialog("college")
            input_college_dialog.exec()

    @staticmethod
    def open_add_entity_dialog_for_colleges(colleges_table_view, colleges_table_model, save_changes_button,
                                            undo_all_changes_button, reset_item_delegates_func):

        add_college_dialog = AddCollegeDialog(colleges_table_view, colleges_table_model, save_changes_button,
                                              undo_all_changes_button, reset_item_delegates_func)
        add_college_dialog.exec()

    @staticmethod
    def open_confirm_save_or_undo_dialog(save_changes_button, undo_button, students_table_model, programs_table_model,
                                         colleges_table_model, button_type):

        confirm_save_or_undo_dialog = ConfirmSaveOrUndoDialog(button_type)
        confirm_save_or_undo_dialog.exec()

        if confirm_save_or_undo_dialog.get_confirm_edit_decision():

            db_handler = students_table_model.db_handler

            if button_type == "save":
                db_handler.commit_changes()

                students_table_model.set_has_changes(False)
                programs_table_model.set_has_changes(False)
                colleges_table_model.set_has_changes(False)
            elif button_type == "undo":
                db_handler.rollback_changes()

                students_table_model.set_has_changes(False)
                programs_table_model.set_has_changes(False)
                colleges_table_model.set_has_changes(False)

                students_table_model.initialize_data()
                programs_table_model.initialize_data()
                colleges_table_model.initialize_data()

            SpecificButtonsEnabler.enable_save_and_undo_buttons(save_changes_button,
                                                                undo_button,
                                                                students_table_model,
                                                                programs_table_model,
                                                                colleges_table_model)

            success_save_changes = SuccessSaveChangesDialog(button_type)
            success_save_changes.exec()

