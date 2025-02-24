
from PyQt6.QtWidgets import QComboBox
from PyQt6.QtCore import Qt


class CustomComboBox(QComboBox):
    def __init__(self, parent, is_delegate=False):
        super().__init__(parent)

        if is_delegate:
            self.setEditable(True)
            self.lineEdit().setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.lineEdit().setReadOnly(True)
            self.setCursor(Qt.CursorShape.PointingHandCursor)

    def add_items_for_delegate(self, texts):
        for text in texts:
            self.addItem(text)
            print(texts.index(text))

            self.setItemData(texts.index(text), Qt.AlignmentFlag.AlignCenter, role=Qt.ItemDataRole.TextAlignmentRole)

    def keyPressEvent(self, event):
        # If Enter or Return key is pressed, ignore the event (stop adding items)
        if event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return:
            event.ignore()  # Ignore the Enter key event, preventing the item from being added
        else:
            super().keyPressEvent(event)  # Handle all other keys normally
