from show_tables import *
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget, QTableWidget, QTableWidgetItem

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'controle qualité'
        self.left = 100
        self.top = 100
        self.width = 800
        self.height = 600
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        layout = QVBoxLayout()

        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.create_table(fetch_categories(), ["id", "Libelle"]), "Categories")
        self.tab_widget.addTab(self.create_table(fetch_sous_categories(), ["id", "Libelle", "id_cat"]), "Sous Categories")
        self.tab_widget.addTab(self.create_table(fetch_equipements(), ["id", "Libelle", "dernier controle", "id_cat", "id_sous_cat"]), "Equipements")

        layout.addWidget(self.tab_widget)
        self.setLayout(layout)

    def create_table(self, data, headers):
        table = QTableWidget()
        table.setRowCount(len(data))
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)

        for i, row in enumerate(data):
            for j, item in enumerate(row):
                table.setItem(i, j, QTableWidgetItem(str(item)))

        return table

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
