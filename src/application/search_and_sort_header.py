from PyQt6.QtCore import QRegularExpression, Qt


class SearchAndSortHeader:

    @staticmethod
    def change_contents(entity_type, combobox, combobox_type):
        combobox.clear()

        if combobox_type == "search":
            combobox.addItem("All")

        if entity_type == "student":
            combobox.addItem("ID Number")
            combobox.addItem("First Name")
            combobox.addItem("Last Name")
            combobox.addItem("Year Level")
            combobox.addItem("Gender")
            combobox.addItem("Program Code")

        elif entity_type == "program":
            combobox.addItem("Program Code")
            combobox.addItem("Program Name")
            combobox.addItem("College Code")

        elif entity_type == "college":
            combobox.addItem("College Code")
            combobox.addItem("College Name")

    @staticmethod
    def change_search_lineedit_placeholder(search_type_combobox, search_input_lineedit):
        search_input_lineedit.setPlaceholderText(f"Input {search_type_combobox.currentText()}")

    @staticmethod
    def search_using_lineedit(entity_type, search_type_combobox, search_input_lineedit, model,
                              reset_item_delegates_func, table_view, current_page_lineedit,
                              max_pages_label, prev_button, next_button):

        search_type = search_type_combobox.currentText().lower().replace(" ", "_")

        search_text = search_input_lineedit.text()

        model.layoutAboutToBeChanged.emit()

        model.search_entities(search_type, search_text)

        model.update_page_view(table_view)

        max_pages_label.setText(f"/ {model.max_pages}")

        current_page_lineedit.setText("")
        current_page_lineedit.setPlaceholderText("1")

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
                            reset_item_delegates_func, table_view, current_page_lineedit,
                            max_pages_label):

        sort_column = sort_type_combobox.currentText().lower().replace(" ", "_")

        sort_order = sort_order_combobox.currentText().lower()

        model.layoutAboutToBeChanged.emit()

        if model.get_is_data_currently_filtered():
            model.sort_filtered_entities(sort_column, sort_order)
        else:
            model.sort_entities(sort_column, sort_order)

        model.update_page_view(table_view)

        max_pages_label.setText(f"/ {model.max_pages}")

        current_page_lineedit.setText("")
        current_page_lineedit.setPlaceholderText("1")

        model.layoutChanged.emit()

        reset_item_delegates_func(entity_type)
