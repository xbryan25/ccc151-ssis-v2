from PyQt6.QtCore import QSortFilterProxyModel, Qt


class CustomSortFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, source_model):
        super().__init__()

        self.setSourceModel(source_model)
        self.setSortCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)