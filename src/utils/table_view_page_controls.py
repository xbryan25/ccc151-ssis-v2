from PyQt6.QtCore import QTimer, QModelIndex


class TableViewPageControls:

    @staticmethod
    def go_to_previous_page(table_view, model, current_page_lineedit):
        table_view.clearSelection()
        table_view.setCurrentIndex(QModelIndex())

        model.set_previous_page()

        current_page_lineedit.setPlaceholderText(str(model.current_page_number))

    @staticmethod
    def go_to_next_page(table_view, model, current_page_lineedit):
        table_view.clearSelection()
        table_view.setCurrentIndex(QModelIndex())

        model.set_next_page()

        current_page_lineedit.setPlaceholderText(str(model.current_page_number))

    @staticmethod
    def get_max_visible_rows(table_view):
        row_height = 30  # Get actual row height

        if row_height <= 0:
            return 0

        table_view_height = table_view.viewport().height()

        visible_rows = table_view_height // row_height
        return visible_rows

    @staticmethod
    def update_max_pages_label(model, max_pages_label):
        max_pages_label.setText(model.max_pages)

    @staticmethod
    def update_navigation_buttons_state(model, prev_button, next_button):
        print("Yo")
