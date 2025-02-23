
from PyQt6.QtWidgets import QComboBox
from PyQt6.QtCore import Qt


class CustomComboBox(QComboBox):
    def __init__(self, parent):
        super().__init__(parent)

    def keyPressEvent(self, event):
        # If Enter or Return key is pressed, ignore the event (stop adding items)
        if event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return:
            event.ignore()  # Ignore the Enter key event, preventing the item from being added
        else:
            super().keyPressEvent(event)  # Handle all other keys normally
