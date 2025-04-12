from helper_dialogs.input_prerequisite.input_prerequisite import InputPrerequisiteDialog
from helper_dialogs.save_or_undo_state.confirm_save_or_undo import ConfirmSaveOrUndoDialog
from helper_dialogs.save_or_undo_state.success_save_changes import SuccessSaveChangesDialog

from operation_dialogs.add_entity.add_student import AddStudentDialog
from operation_dialogs.add_entity.add_program import AddProgramDialog
from operation_dialogs.add_entity.add_college import AddCollegeDialog

from utils.specific_buttons_enabler import SpecificButtonsEnabler


class OpenDialogs:

    def __init__(self, students_table_view, students_table_model, programs_table_view, programs_table_model,
                 colleges_table_view, colleges_table_model, save_changes_button,  undo_all_changes_button,
                 reset_item_delegates_func):

        self.students_table_view = students_table_view
        self.students_table_model = students_table_model

        self.programs_table_view = programs_table_view
        self.programs_table_model = programs_table_model

        self.colleges_table_view = colleges_table_view
        self.colleges_table_model = colleges_table_model

        self.save_changes_button = save_changes_button
        self.undo_all_changes_button = undo_all_changes_button

        self.reset_item_delegates_func = reset_item_delegates_func

    def open_add_entity_dialog_for_students(self):

        if len(self.students_table_model.db_handler.get_all_entities('program')) > 0:

            add_student_dialog = AddStudentDialog(self.students_table_view, self.students_table_model,
                                                  self.save_changes_button, self.undo_all_changes_button,
                                                  self.reset_item_delegates_func)
            add_student_dialog.exec()

        else:
            input_programs_dialog = InputPrerequisiteDialog("programs")
            input_programs_dialog.exec()

    def open_add_entity_dialog_for_programs(self):

        if len(self.programs_table_model.db_handler.get_all_entities('college')) > 0:
            # Note: reset_item_delegates is a function

            add_program_dialog = AddProgramDialog(self.programs_table_view, self.programs_table_model,
                                                  self.save_changes_button, self.undo_all_changes_button,
                                                  self.reset_item_delegates_func)
            add_program_dialog.exec()


        else:
            input_college_dialog = InputPrerequisiteDialog("college")
            input_college_dialog.exec()

    def open_add_entity_dialog_for_colleges(self):

        add_college_dialog = AddCollegeDialog(self.colleges_table_view, self.colleges_table_model,
                                              self.save_changes_button, self.undo_all_changes_button,
                                              self.reset_item_delegates_func)
        add_college_dialog.exec()

    def open_confirm_save_or_undo_dialog(self, button_type):

        confirm_save_or_undo_dialog = ConfirmSaveOrUndoDialog(button_type)
        confirm_save_or_undo_dialog.exec()

        if confirm_save_or_undo_dialog.get_confirm_edit_decision():

            db_handler = self.students_table_model.db_handler

            if button_type == "save":
                db_handler.commit_changes()

                self.students_table_model.set_has_changes(False)
                self.programs_table_model.set_has_changes(False)
                self.colleges_table_model.set_has_changes(False)
            elif button_type == "undo":
                db_handler.rollback_changes()

                self.students_table_model.set_has_changes(False)
                self.programs_table_model.set_has_changes(False)
                self.colleges_table_model.set_has_changes(False)

                self.students_table_model.initialize_data()
                self.programs_table_model.initialize_data()
                self.colleges_table_model.initialize_data()



            SpecificButtonsEnabler.enable_save_and_undo_buttons(self.save_changes_button,
                                                                self.undo_all_changes_button,
                                                                self.students_table_model,
                                                                self.programs_table_model,
                                                                self.colleges_table_model)

            success_save_changes = SuccessSaveChangesDialog(button_type)
            success_save_changes.exec()

