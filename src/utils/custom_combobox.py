from PyQt6.QtWidgets import QComboBox
from PyQt6.QtCore import Qt


class CustomComboBox(QComboBox):
    def __init__(self, parent):
        super().__init__(parent)

    def keyPressEvent(self, event):
        # If Enter or Return key is pressed, the event is ignored, the items won't be added
        if event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return:
            event.ignore()
        else:
            super().keyPressEvent(event)
