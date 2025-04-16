from PyQt6.QtCore import QTimer, QModelIndex


class TableViewPageControls:

    @staticmethod
    def go_to_previous_page(table_view, model, current_page_lineedit, previous_page_button, next_page_button):
        table_view.clearSelection()
        table_view.setCurrentIndex(QModelIndex())

        model.set_previous_page(previous_page_button, next_page_button)

        current_page_lineedit.blockSignals(True)
        current_page_lineedit.setText(str(model.current_page_number))
        current_page_lineedit.blockSignals(False)

    @staticmethod
    def go_to_next_page(table_view, model, current_page_lineedit, previous_page_button, next_page_button):
        table_view.clearSelection()
        table_view.setCurrentIndex(QModelIndex())

        model.set_next_page(previous_page_button, next_page_button)

        current_page_lineedit.blockSignals(True)
        current_page_lineedit.setText(str(model.current_page_number))
        current_page_lineedit.blockSignals(False)

    @staticmethod
    def go_to_specific_page(table_view, model, current_page_lineedit, previous_page_button, next_page_button):

        table_view.clearSelection()
        table_view.setCurrentIndex(QModelIndex())

        str_page_number = current_page_lineedit.text().strip()

        if not str_page_number.isdigit() and str_page_number != "":
            current_page_lineedit.setText("1")
            return

        if str_page_number == "":
            page_number = 1
        else:
            page_number = int(current_page_lineedit.text())

        model.set_specific_page(page_number, current_page_lineedit, previous_page_button, next_page_button)

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
