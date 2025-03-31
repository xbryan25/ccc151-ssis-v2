from PyQt6.QtWidgets import QMenu


class ContextMenuSetup:
    def __init__(self, table_view, students_table_model, programs_table_model, colleges_table_model, save_changes_button,
                 reset_item_delegates_func):
        self.table_view = table_view

        self.students_table_model = students_table_model
        self.programs_table_model = programs_table_model
        self.colleges_table_model = colleges_table_model
        self.save_changes_button = save_changes_button
        self.reset_item_delegates_func = reset_item_delegates_func

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

        print("Edit:", end=" ")
        print(list(set(index.row() for index in selected_indexes)))

    def delete_entity(self):
        selected_indexes = self.table_view.selectionModel().selectedIndexes()

        print("Delete:", end=" ")
        print(list(set(index.row() for index in selected_indexes)))