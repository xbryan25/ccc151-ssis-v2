

# This function determines if a column header has been clicked 3 times consecutively
# If so, then the sort order for that particular column will be removed
# Under the hood, the 'Order ID' column, which is hidden, will just be sorted
# in ascending order

class ResetSortingState:
    def __init__(self, current_table, ascending_order):
        self.current_table = current_table
        self.ascending_order = ascending_order
        self.prev_clicked = [None, None]

    def reset_sorting_state(self, column_number):
        column_header = self.current_table.horizontalHeaderItem(column_number)

        if not self.prev_clicked[0] and not self.prev_clicked[1]:
            self.prev_clicked[0] = column_header

        elif column_header != self.prev_clicked[0]:
            self.prev_clicked[0] = column_header
            self.prev_clicked[1] = None

        elif column_header == self.prev_clicked[0] and not self.prev_clicked[1]:
            self.prev_clicked[1] = column_header

        elif column_header == self.prev_clicked[1]:
            self.current_table.sortItems(0, self.ascending_order)
            self.prev_clicked = [None, None]

