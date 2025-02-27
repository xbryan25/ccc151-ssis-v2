from PyQt6.QtWidgets import QItemDelegate
from PyQt6.QtCore import Qt

from utils.custom_combobox import CustomComboBox

# https://stackoverflow.com/questions/51945016/pyqt-qcombobox-in-qtableview


class ComboboxItemDelegate(QItemDelegate):

    def __init__(self, parent, items):
        self.items = items

        QItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):
        combobox = CustomComboBox(parent)

        if index.row() % 2 == 0:
            combobox.setStyleSheet("background-color: rgb(176, 137, 104);")
        else:
            combobox.setStyleSheet("background-color: rgb(221, 184, 146);")

        combobox.view().setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        choices = []
        for item in self.items:
            choices.append(item)

        combobox.addItems(choices)

        combobox.currentIndexChanged.connect(self.change_combobox_value)

        return combobox

    def setEditorData(self, editor, index):
        editor.blockSignals(True)

        text = index.model().data(index, Qt.ItemDataRole.DisplayRole)

        try:
            i = self.items.index(text)
        except ValueError:
            i = 0

        editor.setCurrentIndex(i)
        editor.blockSignals(False)

    def setModelData(self, editor, sort_filter_proxy_model, index):
        old_value = sort_filter_proxy_model.get_model_data()[index.row()][index.column()]

        if (sort_filter_proxy_model.data(index) != editor.currentText() and
                not sort_filter_proxy_model.setData(index, editor.currentText())):
            editor.setCurrentText(old_value)

    def change_combobox_value(self):
        self.commitData.emit(self.sender())
