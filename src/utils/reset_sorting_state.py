# This function determines if a column header has been clicked 3 times consecutively
# If so, then the sort order of the table will be reset

from PyQt6.QtCore import Qt, QModelIndex
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QComboBox


class ResetSortingState:
    def __init__(self, sort_filter_proxy_model, table_view, information_type):

        self.sort_filter_proxy_model = sort_filter_proxy_model
        self.table_view = table_view

        self.information_type = information_type

        self.prev_clicked = [None, None]

        self.table_view.horizontalHeader().setSortIndicatorShown(False)

    def reset_sorting_state(self, column_number):
        column_header = self.sort_filter_proxy_model.headerData(column_number, Qt.Orientation.Horizontal,
                                                                Qt.ItemDataRole.DisplayRole)

        if self.information_type != "college":
            self.update_children_combobox_colors()

        if not self.prev_clicked[0] and not self.prev_clicked[1]:
            self.prev_clicked[0] = column_header

            self.table_view.horizontalHeader().setSortIndicatorShown(True)
            self.table_view.horizontalHeader().setSortIndicatorClearable(True)

        elif column_header != self.prev_clicked[0]:
            self.prev_clicked[0] = column_header
            self.prev_clicked[1] = None

        elif column_header == self.prev_clicked[0] and not self.prev_clicked[1]:
            self.prev_clicked[1] = column_header

        elif column_header == self.prev_clicked[1]:
            self.prev_clicked = [None, None]

    def force_reset_sort(self):
        self.prev_clicked = [None, None]
        self.table_view.horizontalHeader().setSortIndicator(-1, Qt.SortOrder.AscendingOrder)

    def group_comboboxes_by_key(self):
        num_of_data = self.sort_filter_proxy_model.rowCount()
        model_data = self.sort_filter_proxy_model.get_model_data()

        connections = {}

        combobox_children = self.table_view.findChildren(QComboBox)

        for row in model_data:

            if self.information_type == "student":
                connections.update({row[0]: [combobox_children[model_data.index(row)],
                                             combobox_children[model_data.index(row) + num_of_data],
                                             combobox_children[model_data.index(row) + (2 * num_of_data)]]})
            elif self.information_type == "program":
                connections.update({row[0]: [combobox_children[model_data.index(row)]]})

        return connections

    def update_children_combobox_colors(self):
        num_of_data = self.sort_filter_proxy_model.rowCount()
        connections = self.group_comboboxes_by_key()

        # print(connections)

        for row in range(num_of_data):
            # Map the row in the proxy model to the source model

            # This is the original index of model, the unsorted index
            # ID number for students, program code for programs
            source_index_key = self.sort_filter_proxy_model.mapToSource(self.sort_filter_proxy_model.index(row, 0))

            orig_key_value = self.sort_filter_proxy_model.source_model.data(source_index_key,
                                                                            Qt.ItemDataRole.DisplayRole)

            if self.information_type == "student":
                if row % 2 == 1:
                    connections[orig_key_value][0].setStyleSheet("background-color: rgb(221, 184, 146)")
                    connections[orig_key_value][1].setStyleSheet("background-color: rgb(221, 184, 146)")
                    connections[orig_key_value][2].setStyleSheet("background-color: rgb(221, 184, 146)")
                else:
                    connections[orig_key_value][0].setStyleSheet("background-color: rgb(176, 137, 104)")
                    connections[orig_key_value][1].setStyleSheet("background-color: rgb(176, 137, 104)")
                    connections[orig_key_value][2].setStyleSheet("background-color: rgb(176, 137, 104)")
            else:
                if row % 2 == 1:
                    connections[orig_key_value][0].setStyleSheet("background-color: rgb(221, 184, 146)")
                else:
                    connections[orig_key_value][0].setStyleSheet("background-color: rgb(176, 137, 104)")
