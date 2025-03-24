from PyQt6.QtCore import QRegularExpression, Qt


class SearchAndSortHeader:

    @staticmethod
    def change_contents(entity_type, combobox):
        combobox.clear()

        if entity_type == "student":
            combobox.addItem("All")
            combobox.addItem("ID Number")
            combobox.addItem("First Name")
            combobox.addItem("Last Name")
            combobox.addItem("Year Level")
            combobox.addItem("Gender")
            combobox.addItem("Program Code")

        elif entity_type == "program":
            combobox.addItem("All")
            combobox.addItem("Program Code")
            combobox.addItem("Program Name")
            combobox.addItem("College Code")

        elif entity_type == "college":
            combobox.addItem("All")
            combobox.addItem("College Code")
            combobox.addItem("College Name")

    @staticmethod
    def change_search_lineedit_placeholder(search_type_combobox, search_input_lineedit):
        search_input_lineedit.setPlaceholderText(f"Input {search_type_combobox.currentText()}")

    @staticmethod
    def search_using_lineedit(entity_type, search_type_combobox, search_input_lineedit, model, sort_filter_proxy_model,
                              reset_item_delegates_func):

        search_type = search_type_combobox.currentIndex() - 1

        model.layoutAboutToBeChanged.emit()

        sort_filter_proxy_model.setFilterKeyColumn(search_type)

        sort_filter_proxy_model.setFilterRegularExpression(
            QRegularExpression('^' + search_input_lineedit.text(),
                               QRegularExpression.PatternOption.CaseInsensitiveOption))

        model.layoutChanged.emit()

        reset_item_delegates_func(entity_type)

    @staticmethod
    def change_sort_type(entity_type, sort_order_combobox, model,
                         sort_filter_proxy_model, reset_item_delegates_func):

        sort_order_combobox.setCurrentIndex(0)

        model.layoutAboutToBeChanged.emit()
        sort_filter_proxy_model.sort(-1)
        model.layoutChanged.emit()

        reset_item_delegates_func(entity_type)

    @staticmethod
    def sort_using_combobox(entity_type, sort_type_combobox, sort_order_combobox, model,
                            sort_filter_proxy_model, reset_item_delegates_func):

        column_to_sort = sort_type_combobox.currentIndex()

        sort_order = sort_order_combobox.currentText()

        model.layoutAboutToBeChanged.emit()

        if sort_order == "Ascending":
            sort_filter_proxy_model.sort(column_to_sort, Qt.SortOrder.AscendingOrder)
        elif sort_order == "Descending":
            sort_filter_proxy_model.sort(column_to_sort, Qt.SortOrder.DescendingOrder)
        else:
            sort_filter_proxy_model.sort(-1)

        model.layoutChanged.emit()

        reset_item_delegates_func(entity_type)
