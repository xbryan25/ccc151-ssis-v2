from PyQt6.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt
import csv

from landing_page.landing_page_design import Ui_MainWindow as LandingPageUI


class LandingPage(QMainWindow, LandingPageUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.add_from_database()

    def add_from_database(self):
        with open("databases/students.csv", 'r') as from_students_csv:
            reader = csv.reader(from_students_csv)

            for row in reader:
                rowPosition = self.tableWidget.rowCount()
                self.tableWidget.insertRow(rowPosition)

                # item = QTableWidgetItem()
                # item.setData(Qt.ItemDataRole.DisplayRole, row[0])

                self.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(row[0]))
                self.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(row[1]))
                self.tableWidget.setItem(rowPosition, 2, QTableWidgetItem(row[2]))
                self.tableWidget.setItem(rowPosition, 3, QTableWidgetItem(row[3]))
                self.tableWidget.setItem(rowPosition, 4, QTableWidgetItem(row[4]))
                self.tableWidget.setItem(rowPosition, 5, QTableWidgetItem(row[5]))

            # self.tableWidget.sortItems(0, Qt.SortOrder.DescendingOrder)
            self.tableWidget.setSortingEnabled(True)