from PyQt6.QtCore import QTimer, QModelIndex


class TableViewPageControls:

    @staticmethod
    def go_to_previous_page(table_view, model, current_page_lineedit, page_buttons):
        table_view.clearSelection()
        table_view.setCurrentIndex(QModelIndex())

        model.set_previous_page(page_buttons)

        current_page_lineedit.blockSignals(True)
        current_page_lineedit.setText(str(model.current_page_number))
        current_page_lineedit.blockSignals(False)

    @staticmethod
    def go_to_next_page(table_view, model, current_page_lineedit, page_buttons):
        table_view.clearSelection()
        table_view.setCurrentIndex(QModelIndex())

        model.set_next_page(page_buttons)

        current_page_lineedit.blockSignals(True)
        current_page_lineedit.setText(str(model.current_page_number))
        current_page_lineedit.blockSignals(False)

    @staticmethod
    def go_to_first_page(table_view, model, current_page_lineedit, page_buttons):
        table_view.clearSelection()
        table_view.setCurrentIndex(QModelIndex())

        model.set_first_page(page_buttons)

        current_page_lineedit.blockSignals(True)
        current_page_lineedit.setText(str(model.current_page_number))
        current_page_lineedit.blockSignals(False)

    @staticmethod
    def go_to_last_page(table_view, model, current_page_lineedit, page_buttons):
        table_view.clearSelection()
        table_view.setCurrentIndex(QModelIndex())

        model.set_last_page(page_buttons)

        current_page_lineedit.blockSignals(True)
        current_page_lineedit.setText(str(model.current_page_number))
        current_page_lineedit.blockSignals(False)

    @staticmethod
    def go_to_specific_page(table_view, model, current_page_lineedit, page_buttons):

        table_view.clearSelection()
        table_view.setCurrentIndex(QModelIndex())

        str_page_number = current_page_lineedit.text().strip()

        if not str_page_number.isdigit() and str_page_number != "":
            current_page_lineedit.setText("1")
            return

        if str_page_number == "":
            page_number = -1
        else:
            page_number = int(current_page_lineedit.text())

        model.set_specific_page(page_number, current_page_lineedit, page_buttons)

    @staticmethod
    def get_max_visible_rows(table_view):
        row_height = 30  # Get actual row height

        if row_height <= 0:
            return 0

        table_view_height = table_view.viewport().height()

        visible_rows = table_view_height // row_height
        return visible_rows
