from PyQt6.QtWidgets import QMenu

from helper_dialogs.delete_item_state.confirm_delete import ConfirmDeleteDialog
from helper_dialogs.delete_item_state.success_delete_item import SuccessDeleteItemDialog

from operation_dialogs.students.edit_student import EditStudentDialog
from operation_dialogs.programs.edit_program import EditProgramDialog
from operation_dialogs.colleges.edit_college import EditCollegeDialog


class ContextMenuSetup:
    def __init__(self, table_view, students_table_model, programs_table_model, colleges_table_model,
                 reset_item_delegates_func, save_changes_button, undo_all_changes_button, entity_type):

        self.table_view = table_view

        self.students_table_model = students_table_model
        self.programs_table_model = programs_table_model
        self.colleges_table_model = colleges_table_model
        self.reset_item_delegates_func = reset_item_delegates_func
        self.save_changes_button = save_changes_button
        self.undo_all_changes_button = undo_all_changes_button

        self.entity_type = entity_type

        if self.entity_type == "student":
            self.current_model = self.students_table_model
        elif self.entity_type == "program":
            self.current_model = self.programs_table_model
        else:
            self.current_model = self.colleges_table_model

    # pos is automatically passed on by QTableView
    def show_context_menu(self, pos):

        index = self.table_view.indexAt(pos)
        if not index.isValid():
            # Do nothing if no cell is clicked
            return

        selected_indexes = self.table_view.selectionModel().selectedIndexes()

        selected_rows = list(set(index.row() for index in selected_indexes))
        selected_rows.sort()

        menu = QMenu(self.table_view)

        if self.entity_type != "college" or (self.entity_type == "college" and len(selected_rows) == 1):
            edit_action = menu.addAction("Edit")
            edit_action.triggered.connect(self.edit_entity)

        delete_action = menu.addAction("Delete")
        delete_action.triggered.connect(self.delete_entity)

        # Execute menu and get selected action
        menu.exec(self.table_view.viewport().mapToGlobal(pos))

    def edit_entity(self):
        selected_indexes = self.table_view.selectionModel().selectedIndexes()

        selected_rows = list(set(index.row() for index in selected_indexes))
        selected_rows.sort()

        identifiers = self.current_model.get_identifiers_of_selected_rows(selected_rows)

        if self.entity_type == "student":

            edit_student_dialog = EditStudentDialog(self.table_view, self.students_table_model,
                                                    self.reset_item_delegates_func, self.save_changes_button,
                                                    self.undo_all_changes_button, identifiers, selected_rows)
            edit_student_dialog.exec()

        elif self.entity_type == "program":
            edit_program_dialog = EditProgramDialog(self.table_view, self.programs_table_model,
                                                    self.reset_item_delegates_func, self.save_changes_button,
                                                    self.undo_all_changes_button, identifiers, selected_rows)
            edit_program_dialog.exec()

        elif self.entity_type == "college":
            edit_college_dialog = EditCollegeDialog(self.table_view, self.colleges_table_model,
                                                    self.reset_item_delegates_func, self.save_changes_button,
                                                    self.undo_all_changes_button, identifiers, selected_rows)
            edit_college_dialog.exec()

    def delete_entity(self):
        selected_indexes = self.table_view.selectionModel().selectedIndexes()

        selected_rows = list(set(index.row() for index in selected_indexes))
        selected_rows.sort()

        identifiers = self.current_model.get_identifiers_of_selected_rows(selected_rows)

        # Probably put in another file for better organization

        self.confirm_to_delete_dialog = ConfirmDeleteDialog(self.entity_type, identifiers)
        self.confirm_to_delete_dialog.exec()

        confirm_delete_decision = self.confirm_to_delete_dialog.get_confirm_delete_decision()

        if confirm_delete_decision:

            for selected_row in selected_rows:
                self.current_model.delete_entity_from_db(selected_row, 'student')

            self.current_model.update_data_from_db_after_deleting(selected_rows)

            self.table_view.clearSelection()
            self.current_model.update_page_view(self.table_view)

            self.success_delete_item_dialog = SuccessDeleteItemDialog("student")
            self.success_delete_item_dialog.exec()
