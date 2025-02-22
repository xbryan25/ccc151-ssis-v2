from PyQt6.QtCore import QRegularExpression


class SearchHeader:

    @staticmethod
    def change_contents(entity_type, search_type_combobox):
        search_type_combobox.clear()

        if entity_type == "student":
            search_type_combobox.addItem("ID Number")
            search_type_combobox.addItem("First Name")
            search_type_combobox.addItem("Last Name")
            search_type_combobox.addItem("Year Level")
            search_type_combobox.addItem("Gender")
            search_type_combobox.addItem("Program Code")

        elif entity_type == "program":
            search_type_combobox.addItem("Program Code")
            search_type_combobox.addItem("Program Name")
            search_type_combobox.addItem("College Code")

        elif entity_type == "college":
            search_type_combobox.addItem("College Code")
            search_type_combobox.addItem("College Name")

    @staticmethod
    def change_search_lineedit_placeholder(search_type_combobox, search_input_lineedit):
        search_input_lineedit.setPlaceholderText(f"Input {search_type_combobox.currentText()}")

    @staticmethod
    def search_using_lineedit(search_type_combobox, search_input_lineedit, model, sort_filter_proxy_model,
                              reset_item_delegates_func):

        search_type = search_type_combobox.currentIndex()

        model.layoutAboutToBeChanged.emit()

        sort_filter_proxy_model.setFilterKeyColumn(search_type)

        sort_filter_proxy_model.setFilterRegularExpression(
            QRegularExpression('^' + search_input_lineedit.text(),
                               QRegularExpression.PatternOption.CaseInsensitiveOption))

        model.layoutChanged.emit()

        reset_item_delegates_func()

