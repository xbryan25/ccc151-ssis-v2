# This function determines if a column header has been clicked 3 times consecutively
# If so, then the sort order for that particular column will be removed
# Under the hood, the 'Order ID' column, which is hidden, will just be sorted
# in ascending order

from PyQt6.QtCore import Qt


class ResetSortingState:
    def __init__(self, table_model, table_view):
        self.table_model = table_model
        self.table_view = table_view

        self.prev_clicked = [None, None]

        # self.table_view.horizontalHeader().setSortIndicatorClearable(True)
        self.table_view.horizontalHeader().setSortIndicatorShown(False)


    def reset_sorting_state(self, column_number):
        column_header = self.table_model.headerData(column_number, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole)

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

        print(self.prev_clicked)
