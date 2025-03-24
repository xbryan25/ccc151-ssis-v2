

class TableViewPageControls:

    @staticmethod
    def go_to_previous_page(model, current_page_lineedit):
        model.set_previous_page()

        current_page_lineedit.setPlaceholderText(str(model.current_page_number))

    @staticmethod
    def go_to_next_page(model, current_page_lineedit):
        model.set_next_page()

        current_page_lineedit.setPlaceholderText(str(model.current_page_number))

    @staticmethod
    def get_max_visible_rows(table_view):
        row_height = 30  # Get actual row height

        print(table_view.viewport().height())

        if row_height <= 0:
            return 0

        visible_rows = table_view.viewport().height() // row_height
        return visible_rows

