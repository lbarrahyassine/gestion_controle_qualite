from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QDialogButtonBox
from connexion import connection
from mysql.connector import Error


class ModifyCategoryDialog(QDialog):
    def __init__(self, parent=None, row=None, categorie_table=None):
        super().__init__(parent)
        self.categorie_table = categorie_table
        self.setWindowTitle("Modifier une Catégorie")
        self.row = row
        self.parent = parent
        self.layout = QFormLayout()

        self.category_id = parent.categorie_table.item(self.row, 0).text()
        self.libelle_input = QLineEdit(parent.categorie_table.item(row, 1).text())

        self.layout.addRow("Libelle:", self.libelle_input)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.modify_category)
        self.buttons.rejected.connect(self.reject)

        self.layout.addWidget(self.buttons)
        self.setLayout(self.layout)

    def modify_category(self):
        libelle = self.libelle_input.text()
        try:
            cursor = connection.cursor()
            cursor.execute("UPDATE categorie SET libele = %s WHERE id_cat = %s", (libelle, self.category_id))
            connection.commit()
            cursor.close()
            self.accept()
        except Error as e:
            print(f"The error '{e}' occurred")
