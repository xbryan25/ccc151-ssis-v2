from PyQt6.QtCore import QTimer

from operation_dialogs.edit_entity.edit_student import EditStudentDialog
from operation_dialogs.edit_entity.edit_program import EditProgramDialog
from operation_dialogs.edit_entity.edit_college import EditCollegeDialog

from utils.specific_buttons_enabler import SpecificButtonsEnabler


# This class will be called by the edit button of the context menu
class EditEntityHandler:
    def __init__(self, selected_rows, identifiers, current_model, table_view, entity_type, save_changes_button,
                 undo_all_changes_button, reset_item_delegates_func):

        self.selected_rows = selected_rows
        self.identifiers = identifiers
        self.current_model = current_model
        self.table_view = table_view
        self.entity_type = entity_type

        self.save_changes_button = save_changes_button
        self.undo_all_changes_button = undo_all_changes_button

        self.reset_item_delegates_func = reset_item_delegates_func

    def edit_entities(self):

        if self.entity_type == "student":

            edit_student_dialog = EditStudentDialog(self.table_view, self.current_model,
                                                    self.save_changes_button, self.undo_all_changes_button,
                                                    self.reset_item_delegates_func, self.identifiers, self.selected_rows)
            edit_student_dialog.exec()

        elif self.entity_type == "program":
            edit_program_dialog = EditProgramDialog(self.table_view, self.current_model,
                                                    self.save_changes_button, self.undo_all_changes_button,
                                                    self.reset_item_delegates_func, self.identifiers, self.selected_rows)
            edit_program_dialog.exec()

        elif self.entity_type == "college":
            edit_college_dialog = EditCollegeDialog(self.table_view, self.current_model,
                                                    self.save_changes_button, self.undo_all_changes_button,
                                                    self.reset_item_delegates_func, self.identifiers, self.selected_rows)
            edit_college_dialog.exec()
