from PyQt6.QtWidgets import QMenu

from operation_dialogs.delete_entity.delete_entity_handler import DeleteEntityHandler
from operation_dialogs.edit_entity.edit_entity_handler import EditEntityHandler


class ContextMenuSetup:
    def __init__(self, table_view, students_table_model, programs_table_model, colleges_table_model,
                 save_changes_button, undo_all_changes_button, reset_item_delegates_func, entity_type):

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
            edit_action.triggered.connect(lambda: self.delete_or_edit_entity("edit"))

        delete_action = menu.addAction("Delete")
        delete_action.triggered.connect(lambda: self.delete_or_edit_entity("delete"))

        # Execute menu and get selected action
        menu.exec(self.table_view.viewport().mapToGlobal(pos))

    def delete_or_edit_entity(self, delete_or_edit):

        selected_indexes = self.table_view.selectionModel().selectedIndexes()

        selected_rows = list(set(index.row() for index in selected_indexes))
        selected_rows.sort()

        identifiers = self.current_model.get_identifiers_of_selected_rows(selected_rows)

        if delete_or_edit == "delete":
            delete_entity_handler = DeleteEntityHandler(selected_rows, identifiers, self.current_model, self.table_view,
                                                        self.entity_type, self.save_changes_button,
                                                        self.undo_all_changes_button)
            delete_entity_handler.delete_entities()

        elif delete_or_edit == "edit":
            edit_entity_handler = EditEntityHandler(selected_rows, identifiers, self.current_model, self.table_view,
                                                    self.entity_type, self.save_changes_button,
                                                    self.undo_all_changes_button, self.reset_item_delegates_func)
            edit_entity_handler.edit_entities()
