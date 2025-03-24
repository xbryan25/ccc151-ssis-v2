from PyQt6.QtCore import QSortFilterProxyModel, Qt


class CustomSortFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, source_model):
        super().__init__()

        self.source_model = source_model

        self.setSourceModel(self.source_model)
        self.setSortCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)

    def get_model_data(self):
        return self.source_model.get_data()

    def get_source_model(self):
        return self.source_model

    def update_pagination_after_search(self):
        self.source_model.update_after_search(self.rowCount())

        self.source_model.layoutChanged.emit()
