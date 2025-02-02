from PyQt6.QtCore import QAbstractTableModel, Qt

from utils.reset_sorting_state import ResetSortingState

import operator

# Where I discovered QTableView:
# https://stackoverflow.com/questions/6785481/how-to-implement-a-filter-option-in-qtablewidget

# MVC PyQT6 Tutorial: https://www.pythonguis.com/tutorials/modelview-architecture/
# https://www.pythonguis.com/tutorials/pyqt6-qtableview-modelviews-numpy-pandas/


class CustomTableModel(QAbstractTableModel):
    def __init__(self, data_from_csv, columns):
        super().__init__()

        self.data_from_csv = data_from_csv
        self.columns = columns

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            return self.data_from_csv[index.row()][index.column()]

        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignCenter

    def rowCount(self, index=None):
        # The length of the outer list.
        return len(self.data_from_csv)

    def columnCount(self, index=None):
        return len(self.data_from_csv[0])

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.columns[section]

        return super().headerData(section, orientation, role)

    # def sort(self, column, order):
    #     if self.data_from_csv and self.data_from_csv[0]:
    #         self.layoutAboutToBeChanged.emit()
    #
    #         if isinstance(self.tableData[0][col], str):
    #             sortkey = lambda row: row[col].lower()
    #         else:
    #             sortkey = operator.itemgetter(col)
    #
    #         self.data_from_csv = sorted(
    #             self.data_from_csv, key=sortkey,
    #             reverse=(order != Qt.AscendingOrder))
    #
    #         self.layoutChanged.emit()
