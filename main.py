from show_tables import *
import sys
from PyQt5.QtWidgets import *
from add_cat import *
from modify import *
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'controle qualité'
        self.left = 100
        self.top = 100
        self.width = 1100
        self.height = 600
        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        layout = QVBoxLayout()

        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.equipement_win(), "Equipements")
        self.tab_widget.addTab(self.categ_win(), "Categories")
        self.tab_widget.addTab(self.create_table(fetch_sous_categories(), ["id", "Libelle", "id_cat"]), "Sous Categories")


        layout.addWidget(self.tab_widget)

        self.setLayout(layout)

    def create_table(self, data, headers):
        table = QTableWidget()
        table.setRowCount(len(data))
        table.setColumnCount(len(headers)+2)
        table.setHorizontalHeaderLabels(headers+["modify"]+["delete"])

        for i, row in enumerate(data):
            for j, item in enumerate(row):
                table.setItem(i, j, QTableWidgetItem(str(item)))
            modify_button = QPushButton("Modify")
            modify_button.clicked.connect(lambda _, r=i: self.modify_row(r))  # Connect to your modify function
            table.setCellWidget(i, len(headers), modify_button)

            # Create Delete button
            delete_button = QPushButton("Delete")
            #delete_button.clicked.connect(self.delete_row)  # Connect to your delete function
            table.setCellWidget(i, len(headers) + 1, delete_button)
        return table

    def modify_row(self, row):
        try:
            dialog = ModifyEquipementDialog(self, row)
            dialog.exec_()
            self.refresh_equipements()
        except Exception as e:
            print(f"Error in modify_row: {e}")

    def refresh_equipements(self):
        data = fetch_equipements()
        self.equipements_table.setRowCount(0)  # Clear existing rows
        self.equipements_table.setRowCount(len(fetch_equipements()))  # Set new row count

        for i, row in enumerate(data):
            for j, item in enumerate(row):
                self.equipements_table.setItem(i, j, QTableWidgetItem(str(item)))
            modify_button = QPushButton("Modify")
            modify_button.clicked.connect(lambda _, r=i: self.modify_row(r))  # Connect to your modify function
            self.equipements_table.setCellWidget(i, len(["id", "Libelle", "id_sous_cat","date_service","actif","rebut","id_energie"]), modify_button)

            # Create Delete button
            delete_button = QPushButton("Delete")
            # delete_button.clicked.connect(self.delete_row)  # Connect to your delete function
            self.equipements_table.setCellWidget(i, len(["id", "Libelle", "id_sous_cat","date_service","actif","rebut","id_energie"]) + 1, delete_button)

    def equipement_win(self):
        widget = QWidget()
        layout = QVBoxLayout()

        self.equipements_table = self.create_table(fetch_equipements(), ["id", "Libelle", "id_sous_cat","date_service","actif","rebut","id_energie"])
        layout.addWidget(self.equipements_table)

        ajouter_button = QPushButton("Ajouter")
        ajouter_button.clicked.connect(self.open_add_dialog)  # Connect the button to a function
        layout.addWidget(ajouter_button)

        widget.setLayout(layout)
        return widget


    def open_add_dialog(self):
        dialog = AddEquipementDialog(self)
        dialog.exec_()

    def show_add_cat_dialog(self):
        dialog = QDialog(self)
        ui = Ui_Dialog()
        ui.setupUi(dialog)
        dialog.exec_()

    def categ_win(self):
        widget = QWidget()
        layout = QVBoxLayout()

        self.categorie_table = self.create_table(fetch_categories(), ["id", "Libelle"])
        layout.addWidget(self.categorie_table)

        ajouter_button2 = QPushButton("Ajouter")
        ajouter_button2.clicked.connect(self.show_add_cat_dialog)  # Connect the button to a function
        layout.addWidget(ajouter_button2)

        widget.setLayout(layout)
        return widget



class AddEquipementDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ajouter un Equipement")

        self.layout = QFormLayout()

        self.libelle_input = QLineEdit()
        self.id_sous_cat_input = QLineEdit()
        self.date_service_input = QLineEdit()
        self.actif_input = QLineEdit()
        self.rebut_input = QLineEdit()
        self.id_energie_input = QLineEdit()

        self.layout.addRow("Libelle:", self.libelle_input)
        self.layout.addRow("ID Sous Cat:", self.id_sous_cat_input)
        self.layout.addRow("Date Service:", self.date_service_input)
        self.layout.addRow("Actif:", self.actif_input)
        self.layout.addRow("Rebut:", self.rebut_input)
        self.layout.addRow("ID Energie:", self.id_energie_input)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.add_equipement)
        self.buttons.rejected.connect(self.reject)

        self.layout.addWidget(self.buttons)
        self.setLayout(self.layout)

    def add_equipement(self):
        libelle = self.libelle_input.text()
        id_sous_cat = self.id_sous_cat_input.text()
        date_service = self.date_service_input.text()
        actif = self.actif_input.text()
        rebut = self.rebut_input.text()
        id_energie = self.id_energie_input.text()

        # Here you should add the code to insert this data into your database
        # Example:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO equipement (Libele, id_sous_cat, date_service, actif, rebut, id_energie) VALUES (%s, %s, %s, %s, %s, %s)",
                (libelle, id_sous_cat, date_service, actif, rebut, id_energie))
            connection.commit()
            cursor.close()
        except Error as e:
            print(f"The error '{e}' occurred")

        self.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
