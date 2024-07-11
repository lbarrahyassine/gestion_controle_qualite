import sys
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import QDate
from modify import ModifyEquipementDialog
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)


# Mock connection and data fetching for testing purposes
class MockConnection:
    def cursor(self):
        return self

    def execute(self, query, params=None):
        print(f"Executing query: {query} with params: {params}")

    def commit(self):
        print("Committing transaction")

    def close(self):
        print("Closing cursor")


connection = MockConnection()


class TestApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Test Modify Equipement Dialog")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.equipements_table = QTableWidget()
        self.equipements_table.setRowCount(1)
        self.equipements_table.setColumnCount(7)
        headers = ["id", "Libelle", "id_sous_cat", "date_service", "actif", "rebut", "id_energie"]
        self.equipements_table.setHorizontalHeaderLabels(headers)

        data = [1, "Equipement 1", 8, "2023-01-01", "True", "False", 2]
        for i, item in enumerate(data):
            self.equipements_table.setItem(0, i, QTableWidgetItem(str(item)))

        layout.addWidget(self.equipements_table)

        modify_button = QPushButton("Modify")
        modify_button.clicked.connect(self.open_modify_dialog)
        layout.addWidget(modify_button)

        self.setLayout(layout)

    def open_modify_dialog(self):
        dialog = ModifyEquipementDialog(self, row=0)
        dialog.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TestApp()
    ex.show()
    sys.exit(app.exec_())
