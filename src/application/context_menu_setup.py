from PyQt6.QtWidgets import QMenu
from PyQt6.QtCore import QTimer, QMetaObject, Qt

from operation_dialogs.delete_entity.delete_entity_handler import DeleteEntityHandler
from operation_dialogs.edit_entity.edit_entity_handler import EditEntityHandler


class ContextMenuSetup:
    def __init__(self, table_view, students_table_model, programs_table_model, colleges_table_model,
                 current_page_lineedit, max_pages_label, save_changes_button, undo_all_changes_button,
                 reset_item_delegates_func, entity_type):

        self.table_view = table_view

        self.students_table_model = students_table_model
        self.programs_table_model = programs_table_model
        self.colleges_table_model = colleges_table_model

        self.current_page_lineedit = current_page_lineedit
        self.max_pages_label = max_pages_label

        self.save_changes_button = save_changes_button
        self.undo_all_changes_button = undo_all_changes_button

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

        selected_indexes = self.table_view.selectionModel().selectedIndexes()

        selected_rows = list(set(index.row() for index in selected_indexes))
        selected_rows.sort()

        context_menu = QMenu(self.table_view)

        if self.entity_type != "college" or (self.entity_type == "college" and len(selected_rows) == 1):
            edit_action = context_menu.addAction("Edit")
            edit_action.setData("edit")
            # edit_action.triggered.connect(self.edit_entity)
            edit_action.triggered.connect(lambda: QTimer.singleShot(10, self.edit_entity))

        delete_action = context_menu.addAction("Delete")
        delete_action.setData("edit")
        # delete_action.triggered.connect(self.delete_entity)
        delete_action.triggered.connect(lambda: QTimer.singleShot(10, self.delete_entity))
        # Execute context menu and get selected action
        context_menu.exec(self.table_view.viewport().mapToGlobal(pos))

        context_menu.deleteLater()

    # Can't combine the two methods because lambda functions can't be used because of weird
    # event issues that will affect the QMenu

    # It delays execution, and when used inside a QMenu.exec() call, it runs after the menu closes, which eventually
    # results in the QMenu popping up again

    def delete_entity(self):

        selected_indexes = self.table_view.selectionModel().selectedIndexes()

        selected_rows = list(set(index.row() for index in selected_indexes))
        selected_rows.sort()

        identifiers = self.current_model.get_identifiers_of_selected_rows(selected_rows)

        delete_entity_handler = DeleteEntityHandler(selected_rows, identifiers, self.current_model, self.table_view,
                                                    self.entity_type, self.current_page_lineedit, self.max_pages_label,
                                                    self.save_changes_button, self.undo_all_changes_button)
        delete_entity_handler.delete_entities()

    def edit_entity(self):

        selected_indexes = self.table_view.selectionModel().selectedIndexes()

        selected_rows = list(set(index.row() for index in selected_indexes))
        selected_rows.sort()

        identifiers = self.current_model.get_identifiers_of_selected_rows(selected_rows)

        edit_entity_handler = EditEntityHandler(selected_rows, identifiers, self.current_model, self.table_view,
                                                self.entity_type, self.save_changes_button,
                                                self.undo_all_changes_button, self.reset_item_delegates_func)

        edit_entity_handler.edit_entities()

