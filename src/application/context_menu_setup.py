from PyQt6.QtWidgets import QMenu

from helper_dialogs.delete_item_state.confirm_delete import ConfirmDeleteDialog
from helper_dialogs.delete_item_state.success_delete_item import SuccessDeleteItemDialog

from operation_dialogs.students.edit_student import EditStudentDialog


class ContextMenuSetup:
    def __init__(self, table_view, students_table_model, programs_table_model, colleges_table_model, save_changes_button,
                 reset_item_delegates_func, entity_type):

        self.table_view = table_view

        self.students_table_model = students_table_model
        self.programs_table_model = programs_table_model
        self.colleges_table_model = colleges_table_model
        self.save_changes_button = save_changes_button
        self.reset_item_delegates_func = reset_item_delegates_func
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

        menu = QMenu(self.table_view)
        action1 = menu.addAction("Edit")
        action2 = menu.addAction("Delete")

        action1.triggered.connect(self.edit_entity)
        action2.triggered.connect(self.delete_entity)

        # Execute menu and get selected action
        menu.exec(self.table_view.viewport().mapToGlobal(pos))

    def edit_entity(self):
        selected_indexes = self.table_view.selectionModel().selectedIndexes()

        selected_rows = list(set(index.row() for index in selected_indexes))
        selected_rows.sort()

        identifiers = self.current_model.get_identifiers_of_selected_rows(selected_rows)

        edit_student_dialog = EditStudentDialog(self.table_view, self.students_table_model, self.programs_table_model,
                                                self.colleges_table_model, self.reset_item_delegates_func, identifiers,
                                                selected_rows)
        edit_student_dialog.exec()



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
