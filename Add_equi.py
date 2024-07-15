"""from connexion import *
from show_tables import *
import sys
from PyQt5.QtWidgets import *
from add_cat import *
from Add_equi import *"""
from modify import *

class AddEquipementDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ajouter un Equipement")

        self.layout = QFormLayout()

        self.libelle_input = QLineEdit()
        self.id_sous_cat_input = QLineEdit()
        self.date_service_input = QLineEdit()
        #self.actif_input = QLineEdit()
        #self.rebut_input = QLineEdit()
        self.actif_checkbox = QCheckBox("Actif")
        self.rebut_checkbox = QCheckBox("Rebut")
        self.id_energie_input = QLineEdit()

        self.layout.addRow("Libelle:", self.libelle_input)
        self.layout.addRow("ID Sous Cat:", self.id_sous_cat_input)
        self.layout.addRow("Date Service:", self.date_service_input)
        #self.layout.addRow("Actif:", self.actif_input)
        #self.layout.addRow("Rebut:", self.rebut_input)
        self.layout.addRow("Actif: ", self.actif_checkbox)
        self.layout.addRow("Rebut: ", self.rebut_checkbox)
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
        #actif = self.actif_input.text()
        #rebut = self.rebut_input.text()
        actif = "oui" if self.actif_checkbox.isChecked() else "non"
        rebut = "oui" if self.actif_checkbox.isChecked() else "non"
        id_energie = self.id_energie_input.text()


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
